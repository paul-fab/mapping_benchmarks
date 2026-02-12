"""
Rank parsed papers for K-12 education relevance using Claude Sonnet 4.5.

Reads full text from JSONL, sends each paper (truncated) to the LLM, and
produces a relevance score (1-10) plus reclassified framework/tool mappings.

Features:
  - Parallel LLM calls (configurable concurrency)
  - Progress bar with ETA (rich)
  - Resume support: skips already-scored papers
  - Incremental save every N completions
  - Cross-references papers_manifest.json for metadata

Usage:
    uv run rank_papers.py                        # Score all papers
    uv run rank_papers.py --workers 5            # Fewer concurrent calls
    uv run rank_papers.py --limit 100            # Only first 100 pending
    uv run rank_papers.py --model claude-haiku-4-5-20251001  # Use a different model
    uv run rank_papers.py --dry-run              # Show what would be scored
"""

import argparse
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
    SpinnerColumn,
)

from config import FRAMEWORK, TOOL_TYPES

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────

JSONL_PATH = Path("output/all_papers.jsonl")
MANIFEST_PATH = Path("output/papers_manifest.json")
SCORES_PATH = Path("output/paper_scores.json")

DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
MAX_TEXT_CHARS = 6000  # Truncate paper text to this length (~1,500 tokens)
MAX_RETRIES = 3
SAVE_EVERY = 50  # Save scores to disk every N completions

console = Console()
_save_lock = Lock()

# ── Prompt construction ───────────────────────────────────────────────────────

def _build_framework_desc() -> str:
    lines = []
    for fid, info in FRAMEWORK.items():
        lines.append(f"  {fid} -- {info['name']}: {info['description']}")
    return "\n".join(lines)


def _build_tool_desc() -> str:
    lines = []
    for tid, info in TOOL_TYPES.items():
        lines.append(f"  {tid} -- {info['name']}: {info['description']}")
    return "\n".join(lines)


_FRAMEWORK_DESC = _build_framework_desc()
_TOOL_DESC = _build_tool_desc()

_SYSTEM_PROMPT = (
    "You are an expert in AI for K-12 education research, with deep knowledge of "
    "learning science, cognitive load theory, and the impact of AI on student learning.\n\n"
    "Your task is to read a paper's full text and assess its relevance to evaluating "
    "AI systems used in K-12 education (ages 5-18).\n\n"
    "SCOPE: We care about benchmarks, evaluation suites, test sets, curated datasets, "
    "AND research papers that directly evaluate AI's impact on K-12 student learning "
    "(e.g. cognitive offloading studies, Socratic reasoning evaluations, learning "
    "transfer experiments). University-level work is relevant only if it also covers "
    "secondary/high-school content.\n\n"
    "KEY CONCERN -- COGNITIVE OFFLOADING: We are especially interested in work that "
    "measures whether AI tools promote genuine learning vs. cognitive offloading "
    "(students letting AI do the thinking). This includes: Socratic reasoning, "
    "productive struggle, desirable difficulties, metacognition, self-regulated "
    "learning, critical thinking, student over-reliance/dependency, learning transfer, "
    "cognitive load management, and student agency/autonomy.\n\n"
    "You must respond with ONLY valid JSON -- no markdown fences, no commentary."
)


def _build_user_prompt(title: str, text: str) -> str:
    """Build the user prompt for scoring a single paper."""
    truncated = text[:MAX_TEXT_CHARS]
    if len(text) > MAX_TEXT_CHARS:
        truncated += "\n\n[... text truncated ...]"

    return (
        f"## Education Framework Categories\n{_FRAMEWORK_DESC}\n\n"
        f"## Education Tool Types\n{_TOOL_DESC}\n\n"
        f"## Paper to Assess\n\n"
        f"Title: {title}\n\n"
        f"Text:\n{truncated}\n\n"
        "## Scoring Rubric\n"
        "Rate relevance_score from 1 to 10:\n"
        "  10 = Purpose-built K-12 education AI benchmark or evaluation suite\n"
        "   9 = Directly evaluates AI tools in K-12 classroom settings\n"
        "   8 = Strong K-12 education focus, measures learning outcomes with AI\n"
        "   7 = Clear education focus, relevant evaluation methodology\n"
        "   6 = Partially relevant -- education adjacent or covers some K-12 aspects\n"
        "   5 = General AI benchmark that includes education-relevant tasks\n"
        "   4 = Tangentially related -- mostly about other domains but touches education\n"
        "   3 = Weak relevance -- general NLP/AI with possible education applications\n"
        "   2 = Barely relevant -- no direct education connection\n"
        "   1 = Not relevant to K-12 education at all\n\n"
        "## Instructions\n"
        "1. Read the paper text carefully.\n"
        "2. Assign framework_ids (only those DIRECTLY relevant).\n"
        "3. Assign tool_types (only those DIRECTLY relevant).\n"
        "4. Write a concise 1-2 sentence summary of what this paper does/measures.\n"
        "5. Score relevance 1-10 using the rubric above.\n\n"
        "## Required Response Format\n"
        "Return a single JSON object:\n"
        '{"relevance_score": <int 1-10>, '
        '"framework_ids": [<str>, ...], '
        '"tool_types": [<str>, ...], '
        '"summary": "<1-2 sentences>", '
        '"reasoning": "<one sentence explaining the score>"}'
    )


# ── LLM call ─────────────────────────────────────────────────────────────────

def _call_llm(
    client: anthropic.Anthropic,
    model: str,
    title: str,
    text: str,
) -> dict | None:
    """Call the LLM for a single paper. Returns parsed dict or None on failure."""
    prompt = _build_user_prompt(title, text)

    for attempt in range(MAX_RETRIES):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=512,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()

            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)

            result = json.loads(raw)
            if isinstance(result, dict) and "relevance_score" in result:
                # Validate framework_ids and tool_types
                result["framework_ids"] = [
                    f for f in (result.get("framework_ids") or []) if f in FRAMEWORK
                ]
                result["tool_types"] = [
                    t for t in (result.get("tool_types") or []) if t in TOOL_TYPES
                ]
                # Clamp score
                score = result.get("relevance_score", 1)
                result["relevance_score"] = max(1, min(10, int(score)))
                return result

        except json.JSONDecodeError:
            pass
        except anthropic.RateLimitError:
            wait = min(2 ** (attempt + 2), 60)
            time.sleep(wait)
        except anthropic.APIError as exc:
            if attempt == MAX_RETRIES - 1:
                console.print(f"[red]    API error for '{title[:50]}': {exc}[/red]")
        except Exception as exc:
            if attempt == MAX_RETRIES - 1:
                console.print(f"[red]    Error for '{title[:50]}': {exc}[/red]")

        if attempt < MAX_RETRIES - 1:
            time.sleep(2 ** attempt)

    return None


# ── Score a single paper (worker function) ────────────────────────────────────

def _score_paper(
    paper: dict,
    client: anthropic.Anthropic,
    model: str,
) -> dict:
    """Score a single paper. Returns a result dict for the manifest."""
    paper_id = paper["paper_id"]
    title = paper["title"]
    text = paper["text"]

    result = _call_llm(client, model, title, text)

    if result:
        return {
            "paper_id": paper_id,
            "title": title,
            "relevance_score": result["relevance_score"],
            "framework_ids": result["framework_ids"],
            "tool_types": result["tool_types"],
            "summary": result.get("summary", ""),
            "reasoning": result.get("reasoning", ""),
            "status": "scored",
        }
    else:
        return {
            "paper_id": paper_id,
            "title": title,
            "relevance_score": 0,
            "framework_ids": [],
            "tool_types": [],
            "summary": "",
            "reasoning": "",
            "status": "failed",
        }


# ── Data loading ──────────────────────────────────────────────────────────────

def load_papers() -> list[dict]:
    """Load parsed papers from JSONL."""
    papers = []
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                papers.append(json.loads(line))
    return papers


def load_existing_scores() -> dict[str, dict]:
    """Load previously saved scores. Returns {paper_id: score_dict}."""
    if SCORES_PATH.exists():
        try:
            with open(SCORES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return {s["paper_id"]: s for s in data if s.get("paper_id")}
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_scores(scores: dict[str, dict]):
    """Save all scores to disk."""
    SCORES_PATH.parent.mkdir(parents=True, exist_ok=True)
    items = list(scores.values())
    with open(SCORES_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_ranking(
    max_workers: int = 10,
    limit: int | None = None,
    model: str = DEFAULT_MODEL,
    dry_run: bool = False,
):
    """Run the full ranking pipeline."""
    console.print("[bold]Loading data...[/bold]")
    papers = load_papers()
    existing_scores = load_existing_scores()

    # Filter to only papers that need scoring
    pending = [p for p in papers if p["paper_id"] not in existing_scores]
    already_done = len(papers) - len(pending)

    # Also skip papers with very little text
    pending = [p for p in pending if p.get("char_count", 0) >= 100]

    if limit:
        pending = pending[:limit]

    console.print(f"\n[bold]Ranking plan:[/bold]")
    console.print(f"  Total papers:       [cyan]{len(papers)}[/cyan]")
    console.print(f"  Already scored:     [green]{already_done}[/green]")
    console.print(f"  To score:           [yellow]{len(pending)}[/yellow]")
    console.print(f"  Workers:            [yellow]{max_workers}[/yellow]")
    console.print(f"  Model:              [cyan]{model}[/cyan]")
    console.print(f"  Text truncation:    [dim]{MAX_TEXT_CHARS:,} chars[/dim]")
    console.print(f"  Output:             [dim]{SCORES_PATH}[/dim]\n")

    if dry_run:
        console.print("[yellow]Dry run -- no LLM calls will be made.[/yellow]")
        for p in pending[:10]:
            console.print(f"  [dim]{p['paper_id'][:8]}[/dim]  {p['title'][:80]}")
        if len(pending) > 10:
            console.print(f"  ... and {len(pending) - 10} more")
        return

    if not pending:
        console.print("[green]All papers already scored![/green]")
        _print_summary(existing_scores)
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set. Add it to .env[/red]")
        return

    client = anthropic.Anthropic(api_key=api_key)
    scores = dict(existing_scores)  # mutable copy
    scored = 0
    failed = 0
    completed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        MofNCompleteColumn(),
        TextColumn("*"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scoring papers", total=len(pending))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_score_paper, paper, client, model): paper
                for paper in pending
            }

            for future in as_completed(futures):
                result = future.result()
                completed += 1

                # Store result
                with _save_lock:
                    scores[result["paper_id"]] = result

                if result["status"] == "scored":
                    scored += 1
                else:
                    failed += 1

                progress.update(task, advance=1)

                # Incremental save
                if completed % SAVE_EVERY == 0:
                    with _save_lock:
                        save_scores(scores)

    # Final save
    save_scores(scores)

    console.print(f"\n[bold]Scoring complete![/bold]")
    console.print(f"  Scored:  [green]{scored}[/green]")
    console.print(f"  Failed:  [red]{failed}[/red]")
    console.print(f"  Total:   [cyan]{len(scores)}[/cyan] in {SCORES_PATH}")

    _print_summary(scores)


def _print_summary(scores: dict[str, dict]):
    """Print a distribution summary of relevance scores."""
    score_vals = [s["relevance_score"] for s in scores.values() if s.get("status") == "scored"]
    if not score_vals:
        return

    console.print(f"\n[bold]Score distribution:[/bold]")
    from collections import Counter
    dist = Counter(score_vals)
    for s in range(10, 0, -1):
        count = dist.get(s, 0)
        bar = "#" * min(count // 10, 50)
        console.print(f"  {s:2d}/10: {count:5d}  {bar}")

    avg = sum(score_vals) / len(score_vals)
    high = sum(1 for v in score_vals if v >= 7)
    console.print(f"\n  Average: {avg:.1f} | High relevance (>=7): {high}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Rank parsed papers for K-12 education relevance using an LLM."
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=10,
        help="Number of parallel LLM workers (default: 10).",
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Only score the first N pending papers.",
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Anthropic model to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be scored without making LLM calls.",
    )
    args = parser.parse_args()

    run_ranking(
        max_workers=args.workers,
        limit=args.limit,
        model=args.model,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
