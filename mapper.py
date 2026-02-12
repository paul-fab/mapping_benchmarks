"""
Benchmark Mapper — two-stage classification pipeline.

Stage 1: Heuristic scoring with word-boundary keyword matching
Stage 2: LLM classification via Anthropic Claude (uses S2 TLDRs for context)

Falls back to heuristic-only if no ANTHROPIC_API_KEY is set or --no-llm is used.
"""

import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    MofNCompleteColumn,
    TimeRemainingColumn,
)

from config import FRAMEWORK, TOOL_TYPES
from scraper import BenchmarkEntry

console = Console()


# ── Keyword → framework-id mapping ──────────────────────────────────────────
# Each key is a framework ID; its value is a list of keywords/phrases.
# Single words use word-boundary matching; multi-word phrases use substring.

FRAMEWORK_KEYWORDS: dict[str, list[str]] = {
    "1": [
        "general reasoning", "reasoning", "commonsense", "logic",
        "problem solving", "critical thinking", "cognitive", "GPQA",
        "BIG-Bench", "HellaSwag", "Winogrande", "ARC-Challenge",
        "abstract reasoning", "analogical", "inference",
        "natural language inference", "causal reasoning",
        "higher order thinking", "Socratic reasoning",
        "metacognition", "self-regulated learning",
        "critical thinking skills", "analytical reasoning",
        "deep thinking", "cognitive skills",
    ],
    "2.1": [
        "pedagogical knowledge", "teaching knowledge", "instructional design",
        "curriculum design", "learning theory", "pedagogy knowledge",
        "teacher knowledge", "PCK", "TPACK", "educational psychology",
        "lesson planning", "pedagogical content knowledge",
        "teacher competency", "teaching strategy",
    ],
    "2.2": [
        "explanation quality", "generated explanation", "instructional text",
        "hint generation", "step-by-step explanation", "pedagogical output",
        "teaching quality", "educational generation", "worked example",
        "instructional content generation", "explanation generation",
        "educational text quality",
        "cognitive load", "germane load", "extraneous load",
        "age-appropriate", "productive failure",
    ],
    "2.3": [
        "tutoring", "tutor", "Socratic", "scaffolding", "dialogue",
        "interactive teaching", "conversational tutor", "student interaction",
        "adaptive dialogue", "TutorChat", "TutorEval", "multi-turn education",
        "intelligent tutoring system", "ITS", "educational dialogue",
        "tutoring system evaluation",
        "cognitive offloading", "over-scaffolding", "productive struggle",
        "desirable difficulties", "zone of proximal development", "ZPD",
        "student autonomy", "student agency", "learning transfer",
        "over-reliance", "dependency", "Socratic questioning",
    ],
    "3.1": [
        "content knowledge", "subject knowledge", "MMLU", "STEM",
        "math", "science", "history", "biology", "chemistry", "physics",
        "reading comprehension", "SciQ", "OpenBookQA", "MathBench",
        "MAmmoTH", "GSM8K", "MATH benchmark",
        "computer science", "humanities", "social science",
        "programming", "code education", "coding",
        "K-12", "elementary", "middle school", "high school",
        "grade school", "primary school", "secondary school",
    ],
    "3.2": [
        "content alignment", "curriculum alignment", "learning objective",
        "standards alignment", "bloom taxonomy", "learning outcome",
        "course material", "syllabus", "content mapping",
        "difficulty level", "grade level", "reading level",
        "text complexity", "Bloom's taxonomy",
        "Common Core", "state standards", "age-appropriate",
        "curriculum standards", "learning progression",
    ],
    "4.1": [
        "scoring", "grading", "rubric", "automated essay scoring",
        "AES", "ASAP", "essay scoring", "short answer grading",
        "mark scheme", "assessment scoring", "AI grading",
        "exam scoring", "marking",
    ],
    "4.2": [
        "feedback", "feedback generation", "formative feedback",
        "reasoning feedback", "error analysis", "misconception",
        "diagnostic feedback", "corrective feedback", "actionable feedback",
        "student error", "misconception detection", "formative assessment",
        "error correction", "student mistake",
    ],
    "5": [
        "bias", "fairness", "ethics", "toxicity", "safety",
        "stereotype", "discrimination", "equity", "BBQ",
        "FairEval", "TruthfulQA", "harmful", "responsible AI",
        "cultural sensitivity", "trustworthiness", "alignment",
        "child safety", "age-appropriate content", "student privacy",
        "COPPA", "child-safe",
        "AI over-reliance", "cognitive offloading risk",
        "student dependency", "academic integrity",
        "learning harm", "deskilling",
    ],
    "6.1": [
        "multimodal", "vision", "image understanding", "diagram",
        "figure", "chart understanding", "OCR", "visual question",
        "MathVista", "MMMU", "multi-modal education", "video understanding",
        "audio", "speech", "visual reasoning", "chart QA",
    ],
    "6.2": [
        "multilingual", "cross-lingual", "translation", "EXAMS",
        "language diversity", "non-English", "low-resource language",
        "multilingual education", "polyglot", "cross-language",
        "bilingual", "multilingual assessment",
    ],
}

# ── Keyword → tool-type mapping ──────────────────────────────────────────────

TOOL_KEYWORDS: dict[str, list[str]] = {
    "ai_tutor": [
        "tutor", "tutoring", "Socratic", "dialogue", "conversational",
        "1-to-1", "one-on-one", "student interaction", "chat-based",
        "scaffolding", "hint", "explanation", "worked example",
        "educational dialogue", "student-facing", "interactive learning",
        "Socratic reasoning", "productive struggle", "cognitive offloading",
        "student autonomy", "metacognition", "zone of proximal development",
    ],
    "pal": [
        "adaptive", "personalised", "personalized", "adaptive learning",
        "learning path", "difficulty adaptation", "student model",
        "knowledge tracing", "learner model", "ITS", "intelligent tutoring",
        "mastery", "spaced repetition", "learner proficiency",
        "difficulty level", "grade level",
    ],
    "teacher_support": [
        "teacher", "grading", "scoring", "rubric", "lesson plan",
        "curriculum", "content generation", "question generation",
        "assessment creation", "analytics", "learning analytics",
        "classroom", "instructor", "marking", "exam generation",
        "item generation", "test authoring",
    ],
}


# ── Stage 1: Heuristic scoring ──────────────────────────────────────────────

def _text_blob(entry: BenchmarkEntry) -> str:
    """Combine searchable text fields into one lowercase string."""
    parts = [entry.name, entry.description] + entry.tags
    return " ".join(parts).lower()


def _score_keywords(blob: str, keywords: list[str]) -> float:
    """
    Score keyword matches against a text blob.

    Multi-word phrases use substring matching (weight 2.0 — more specific).
    Single words use word-boundary regex (weight 1.0 — avoids false positives).
    """
    score = 0.0
    for kw in keywords:
        kw_lower = kw.lower()
        if " " in kw_lower:
            # Multi-word phrase → substring match is sufficiently specific
            if kw_lower in blob:
                score += 2.0
        else:
            # Single word → word-boundary match to avoid "math" in "aftermath"
            if re.search(r"\b" + re.escape(kw_lower) + r"\b", blob):
                score += 1.0
    return score


def score_framework(entry: BenchmarkEntry) -> dict[str, float]:
    """Return {framework_id: score} for all matching categories."""
    blob = _text_blob(entry)
    return {
        fid: score
        for fid, keywords in FRAMEWORK_KEYWORDS.items()
        if (score := _score_keywords(blob, keywords)) > 0
    }


def score_tools(entry: BenchmarkEntry) -> dict[str, float]:
    """Return {tool_type: score} for all matching tool types."""
    blob = _text_blob(entry)
    return {
        tid: score
        for tid, keywords in TOOL_KEYWORDS.items()
        if (score := _score_keywords(blob, keywords)) > 0
    }


# ── S2 paper details lookup ─────────────────────────────────────────────────

def _build_s2_lookup(s2_details: list[dict]) -> dict[str, dict]:
    """Build a lookup dict from S2 paper details, indexed by various IDs."""
    lookup: dict[str, dict] = {}
    for paper in s2_details:
        if not paper:
            continue
        pid = paper.get("paperId", "")
        if pid:
            lookup[pid] = paper
        ext_ids = paper.get("externalIds") or {}
        arxiv_id = ext_ids.get("ArXiv", "")
        if arxiv_id:
            lookup[f"arxiv:{arxiv_id.lower()}"] = paper
            lookup[arxiv_id.lower()] = paper
    return lookup


def _find_s2_detail(entry: BenchmarkEntry, s2_lookup: dict) -> Optional[dict]:
    """Try to find the S2 paper detail for a BenchmarkEntry."""
    url = entry.source_url
    if "semanticscholar.org/paper/" in url:
        pid = url.split("/paper/")[-1].split("/")[0].split("?")[0]
        if pid in s2_lookup:
            return s2_lookup[pid]
    if "arxiv.org/abs/" in url:
        arxiv_id = url.split("/abs/")[-1].split("?")[0]
        # Strip version suffix (e.g., v1, v2)
        arxiv_id = re.sub(r"v\d+$", "", arxiv_id).lower()
        for key in [arxiv_id, f"arxiv:{arxiv_id}"]:
            if key in s2_lookup:
                return s2_lookup[key]
    return None


def _get_entry_context(entry: BenchmarkEntry, s2_lookup: dict) -> str:
    """Build rich context string for an entry (used by the LLM prompt)."""
    parts = [f"Name: {entry.name}", f"Type: {entry.source_type}"]

    # S2 TLDR is the best single-line summary available
    s2 = _find_s2_detail(entry, s2_lookup)
    tldr = ""
    if s2:
        tldr_data = s2.get("tldr")
        if isinstance(tldr_data, dict):
            tldr = tldr_data.get("text", "")
        elif isinstance(tldr_data, str):
            tldr = tldr_data
    if tldr:
        parts.append(f"AI Summary: {tldr}")

    if entry.description:
        parts.append(f"Description: {entry.description[:300]}")

    # Extra S2 metadata
    if s2:
        fields = s2.get("fieldsOfStudy") or []
        if fields:
            parts.append(f"Fields: {', '.join(fields)}")
        pub_types = s2.get("publicationTypes") or []
        if pub_types:
            parts.append(f"Publication types: {', '.join(pub_types)}")

    return "\n  ".join(parts)


# ── Stage 2: LLM classification via Anthropic ───────────────────────────────

_SYSTEM_PROMPT = (
    "You are an expert in AI for K-12 education research, with deep knowledge of "
    "learning science, cognitive load theory, and the impact of AI on student learning.\n\n"
    "Your task is to classify entries (benchmarks, evaluations, datasets, papers) "
    "into a structured education technology framework.\n\n"
    "IMPORTANT SCOPE: We care ONLY about K-12 education (ages 5-18, primary and "
    "secondary school). Entries that are only relevant to medical/clinical, legal, "
    "financial, or other professional domains should be marked is_benchmark=false "
    "unless they also clearly apply to K-12 contexts. University-level benchmarks "
    "are acceptable only if they also cover content taught in secondary/high school.\n\n"
    "KEY CONCERN — COGNITIVE OFFLOADING: We are especially interested in benchmarks "
    "and evaluations that measure whether AI tools promote genuine learning vs. "
    "cognitive offloading (students letting AI do the thinking). This includes work on: "
    "Socratic reasoning, productive struggle, desirable difficulties, metacognition, "
    "self-regulated learning, critical thinking, student over-reliance/dependency, "
    "learning transfer, cognitive load management, and student agency/autonomy. "
    "Flag these as highly relevant even if they are research papers rather than formal "
    "benchmark suites.\n\n"
    "You must respond with ONLY a valid JSON array — no markdown fences, "
    "no commentary, no extra text."
)


def _build_framework_desc() -> str:
    """Format framework categories for the LLM prompt."""
    lines = []
    for fid, info in FRAMEWORK.items():
        lines.append(f"  {fid} — {info['name']}: {info['description']}")
    return "\n".join(lines)


def _build_tool_desc() -> str:
    """Format tool types for the LLM prompt."""
    lines = []
    for tid, info in TOOL_TYPES.items():
        lines.append(f"  {tid} — {info['name']}: {info['description']}")
    return "\n".join(lines)


def _build_prompt(entries_with_context: list[tuple[int, str]]) -> str:
    """Build the full user prompt for a batch of entries."""
    fw_desc = _build_framework_desc()
    tool_desc = _build_tool_desc()
    entries_block = "\n\n".join(
        f"Entry {idx}:\n  {ctx}" for idx, ctx in entries_with_context
    )
    return (
        f"## Education Framework Categories\n{fw_desc}\n\n"
        f"## Education Tool Types\n{tool_desc}\n\n"
        "## Classification Rules\n"
        "1. Only assign framework categories that are DIRECTLY relevant.\n"
        "2. An entry can belong to multiple categories and tool types.\n"
        '3. Set "is_benchmark" to true if the entry is a benchmark, '
        "evaluation suite, test set, curated dataset, OR a study/paper that "
        "directly evaluates AI's impact on K-12 student learning outcomes "
        "(e.g. cognitive offloading studies, Socratic reasoning evaluations, "
        "learning transfer experiments). These are valuable even if not a "
        "formal benchmark suite.\n"
        "4. Entries focused on medical, clinical, legal, or narrow professional "
        "domains with no K-12 relevance should be is_benchmark=false.\n"
        "5. Prefer precision over recall — when unsure, leave a category out.\n"
        "6. Carefully read the AI Summary / Description to understand what "
        "the entry actually measures or evaluates.\n\n"
        f"## Entries to Classify\n\n{entries_block}\n\n"
        "## Required Response Format\n"
        "Return a JSON array. Each element:\n"
        '{"index": <int>, "is_benchmark": <bool>, '
        '"framework_ids": [<str>, ...], "tool_types": [<str>, ...], '
        '"reasoning": "<one sentence>"}'
    )


def _call_anthropic(
    prompt: str,
    client,
    model: str,
    max_retries: int = 3,
) -> list[dict]:
    """Call Anthropic API, parse JSON response, retry on failure."""
    for attempt in range(max_retries):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=4096,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text.strip()

            # Strip markdown fences if the model added them
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\s*", "", text)
                text = re.sub(r"\s*```$", "", text)

            results = json.loads(text)
            if isinstance(results, list):
                return results
            console.print("[yellow]    LLM returned non-list, retrying...[/yellow]")
        except json.JSONDecodeError as exc:
            console.print(
                f"[yellow]    JSON parse error (attempt {attempt + 1}/{max_retries}): "
                f"{exc}[/yellow]"
            )
        except Exception as exc:
            console.print(
                f"[red]    API error (attempt {attempt + 1}/{max_retries}): {exc}[/red]"
            )
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)

    return []  # all retries exhausted


def _classify_batch(
    batch: list[tuple[int, BenchmarkEntry, str]],
    client,
    model: str,
) -> list[dict]:
    """Classify one batch of entries via Anthropic Claude."""
    entries_with_context = [(idx, ctx) for idx, _entry, ctx in batch]
    prompt = _build_prompt(entries_with_context)
    return _call_anthropic(prompt, client, model)


def _run_llm_classification(
    entries: list[BenchmarkEntry],
    s2_details: list[dict] | None,
    model: str,
    batch_size: int,
    max_workers: int,
) -> dict[int, dict]:
    """
    Run LLM classification in parallel batches with progress tracking.

    Returns {entry_index: classification_result_dict}.
    """
    try:
        import anthropic  # noqa: F811
    except ImportError:
        console.print(
            "[red]  'anthropic' package not installed. Run: uv add anthropic[/red]"
        )
        return {}

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print(
            "[yellow]  No ANTHROPIC_API_KEY set — skipping LLM classification.[/yellow]"
        )
        console.print(
            "[dim]  Add ANTHROPIC_API_KEY to your .env for AI-powered classification.[/dim]"
        )
        return {}

    client = anthropic.Anthropic(api_key=api_key)

    # ── Build S2 lookup ───────────────────────────────────────────────────
    s2_lookup = _build_s2_lookup(s2_details) if s2_details else {}
    s2_hits = 0

    # Build context for every entry
    indexed: list[tuple[int, BenchmarkEntry, str]] = []
    for i, entry in enumerate(entries):
        ctx = _get_entry_context(entry, s2_lookup)
        if _find_s2_detail(entry, s2_lookup):
            s2_hits += 1
        indexed.append((i, entry, ctx))

    if s2_lookup:
        console.print(
            f"  S2 enrichment: {s2_hits}/{len(entries)} entries have TLDR/metadata "
            f"(from {len(s2_details or [])} paper details)"
        )

    # ── Chunk into batches ────────────────────────────────────────────────
    batches = [
        indexed[i : i + batch_size]
        for i in range(0, len(indexed), batch_size)
    ]
    n_batches = len(batches)

    console.print(
        f"  {len(entries)} entries -> {n_batches} batches "
        f"(size={batch_size}, workers={max_workers}, model={model})"
    )

    # ── Parallel classification with progress bar ─────────────────────────
    all_results: dict[int, dict] = {}
    failed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task("LLM classifying", total=n_batches)

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(_classify_batch, batch, client, model): bi
                for bi, batch in enumerate(batches)
            }

            for future in as_completed(futures):
                bi = futures[future]
                try:
                    batch_results = future.result()
                    for r in batch_results:
                        idx = r.get("index")
                        if idx is not None:
                            all_results[idx] = r
                except Exception as exc:
                    console.print(f"[red]  Batch {bi} failed: {exc}[/red]")
                    failed += 1

                progress.advance(task_id)

    console.print(
        f"  LLM classified {len(all_results)}/{len(entries)} entries"
        + (f" ([red]{failed} batch failures[/red])" if failed else "")
    )

    return all_results


# ── Main pipeline ────────────────────────────────────────────────────────────

def map_all(
    entries: list[BenchmarkEntry],
    s2_details: list[dict] | None = None,
    use_llm: bool = True,
    model: str = "claude-haiku-4-5-20251001",
    batch_size: int = 20,
    max_workers: int = 5,
) -> list[BenchmarkEntry]:
    """
    Full two-stage mapping pipeline.

    Stage 1 — Heuristic keyword scoring (word-boundary matching).
              Provides a baseline classification for every entry.
    Stage 2 — LLM classification via Anthropic Claude.
              Uses S2 TLDRs + abstracts for rich context.
              Runs in parallel batches with a progress bar.

    Hand-curated entries (those with pre-set framework_ids/tool_types from
    known_benchmarks.py) are preserved — both stages only augment them.
    """
    # Track which entries were hand-curated before we touch anything
    hand_curated: set[int] = {
        i for i, e in enumerate(entries) if e.framework_ids or e.tool_types
    }
    if hand_curated:
        console.print(
            f"  {len(hand_curated)} entries have hand-curated mappings (preserved)"
        )

    # ── Stage 1: Heuristic scoring ───────────────────────────────────────
    console.print("\n[bold]Stage 1:[/bold] Heuristic keyword scoring ...")

    # Threshold: require a multi-word phrase match (2.0) or 2+ single words
    MIN_SCORE = 2.0
    heuristic_mapped = 0

    for i, entry in enumerate(entries):
        fw_scores = score_framework(entry)
        tool_scores = score_tools(entry)

        new_fw = [fid for fid, s in fw_scores.items() if s >= MIN_SCORE]
        new_tools = [tid for tid, s in tool_scores.items() if s >= MIN_SCORE]

        if i in hand_curated:
            # Augment hand-curated entries — never remove their mappings
            existing_fw = set(entry.framework_ids)
            existing_tools = set(entry.tool_types)
            entry.framework_ids += [f for f in new_fw if f not in existing_fw]
            entry.tool_types += [t for t in new_tools if t not in existing_tools]
        else:
            entry.framework_ids = new_fw
            entry.tool_types = new_tools

        if entry.framework_ids:
            heuristic_mapped += 1

    console.print(
        f"  Heuristic: {heuristic_mapped}/{len(entries)} entries -> >=1 category"
    )

    # ── Stage 2: LLM classification ──────────────────────────────────────
    if use_llm:
        console.print("\n[bold]Stage 2:[/bold] LLM classification (Anthropic Claude) ...")

        llm_results = _run_llm_classification(
            entries, s2_details, model, batch_size, max_workers,
        )

        benchmarks_found = 0
        for i, entry in enumerate(entries):
            result = llm_results.get(i)
            if not result:
                continue

            # ── Benchmark relevance flag ──────────────────────────────────
            is_bench = result.get("is_benchmark", True)
            if is_bench:
                benchmarks_found += 1
            else:
                if "not-a-benchmark" not in entry.tags:
                    entry.tags.append("not-a-benchmark")

            # ── Validate IDs against known framework/tool keys ────────────
            llm_fw = [f for f in (result.get("framework_ids") or []) if f in FRAMEWORK]
            llm_tools = [
                t for t in (result.get("tool_types") or []) if t in TOOL_TYPES
            ]

            # ── Merge strategy ────────────────────────────────────────────
            if i in hand_curated:
                # Hand-curated: augment only
                existing_fw = set(entry.framework_ids)
                existing_tools = set(entry.tool_types)
                entry.framework_ids += [f for f in llm_fw if f not in existing_fw]
                entry.tool_types += [t for t in llm_tools if t not in existing_tools]
            else:
                # LLM result replaces heuristic result for non-curated entries
                entry.framework_ids = llm_fw
                entry.tool_types = llm_tools

            # Store LLM reasoning as a tag for transparency
            reasoning = result.get("reasoning", "")
            if reasoning:
                entry.tags.append(f"llm:{reasoning}")

        console.print(
            f"  {benchmarks_found} entries identified as benchmarks/evaluations/datasets"
        )

    # ── Summary ──────────────────────────────────────────────────────────
    final_mapped = sum(1 for e in entries if e.framework_ids)
    not_bench = sum(1 for e in entries if "not-a-benchmark" in e.tags)
    console.print(
        f"\n[bold green]Done:[/bold green] "
        f"{final_mapped}/{len(entries)} entries mapped to >=1 framework category"
    )
    if not_bench:
        console.print(
            f"  ({not_bench} entries flagged as not-a-benchmark by LLM)"
        )

    return entries
