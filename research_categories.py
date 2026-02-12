"""
SoTA Research via Anthropic Batch API
======================================

Groups extracted paper sections by framework category or tool type, submits
them as batch API requests (50% cost savings), polls for completion, and
collects structured synthesis results.

Pipeline:
  1. extract_sections.py -> smart extraction (Abstract + Intro + Results +
     Discussion + Conclusion + Limitations) at ~17% of original text
  2. This script -> batch API calls for per-group synthesis
  3. Results -> JSON + Markdown reports

Usage (framework categories — default):
    uv run research_categories.py                    # Submit batches for all categories
    uv run research_categories.py --dry-run          # Preview what would be submitted
    uv run research_categories.py --category 2.3     # Only process one category

Usage (tool types):
    uv run research_categories.py --tool-types --dry-run   # Preview tool-type batches
    uv run research_categories.py --tool-types             # Submit tool-type batches
    uv run research_categories.py --tool-types -c ai_tutor # Only AI Tutors

Common flags:
    uv run research_categories.py --status           # Check status of pending batches
    uv run research_categories.py --collect          # Collect completed batch results
    uv run research_categories.py --realtime         # Use standard API (no batch discount)
    uv run research_categories.py --write-reports    # Generate narrative reports from JSONs
    uv run research_categories.py --write-reports --tool-types  # Reports for tool types
    uv run research_categories.py --collect-reports  # Collect narrative report results
"""

import argparse
import json
import os
import re
import time
from pathlib import Path
from dataclasses import dataclass, field

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

from config import FRAMEWORK, TOOL_TYPES, CONCERNS
from extract_sections import load_and_extract_all, ExtractedPaper, PROFILES

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────

OUTPUT_DIR = Path("output/research")
BATCH_STATE_FILE = OUTPUT_DIR / "batch_state.json"

MODEL = "claude-sonnet-4-5-20250929"           # Analysis (large volume, structured JSON)
REPORT_MODEL = "claude-opus-4-6"               # Report writing (narrative quality)
MAX_TOKENS_PER_BATCH_REQUEST = 180_000   # Leave room for prompt + response in 200K context
MAX_OUTPUT_TOKENS = 8192                  # Max response tokens per request
MAX_PAPERS_PER_REQUEST = 60              # Safety cap

console = Console()

# ── Prompt construction ───────────────────────────────────────────────────────

def _build_system_prompt() -> str:
    return (
        "You are a senior education research analyst specializing in AI/LLM applications "
        "in K-12 education (ages 5-18). You have deep expertise in learning science, "
        "cognitive load theory, educational measurement, and the impact of AI tools on "
        "student learning outcomes.\n\n"
        "Your task is to synthesize a collection of research papers within a specific "
        "education framework category and produce a structured State-of-the-Art analysis.\n\n"
        "IMPORTANT: Focus your analysis on what the papers in THIS category actually cover. "
        "Note any learning science concerns (cognitive offloading, over-reliance, productive "
        "struggle, metacognition) IF the papers address them, but do not force this lens onto "
        "categories where it is not the primary focus. For pedagogical interaction categories "
        "(e.g. 2.3), cognitive offloading is a key concern; for other categories (e.g. "
        "multilingual, content knowledge, scoring), focus on what those papers actually measure "
        "and what gaps exist within their own domain.\n\n"
        "You must respond with ONLY valid JSON -- no markdown fences, no commentary."
    )


def _build_user_prompt(
    category_id: str,
    category_info: dict,
    papers: list[ExtractedPaper],
) -> str:
    """Build the synthesis prompt for a batch of papers in one category."""
    # Combine paper extracts
    paper_texts = []
    for i, ep in enumerate(papers, 1):
        paper_texts.append(
            f"--- Paper {i} (relevance: {ep.relevance_score}/10) ---\n"
            f"{ep.to_text()}\n"
        )
    combined = "\n\n".join(paper_texts)

    return (
        f"## Category: {category_id} - {category_info['name']}\n"
        f"Area: {category_info['area']}\n"
        f"Description: {category_info['description']}\n\n"
        f"## Papers in this category ({len(papers)} papers)\n\n"
        f"{combined}\n\n"
        f"## Analysis Instructions\n\n"
        f"Synthesize ALL {len(papers)} papers above into a structured SoTA analysis for "
        f"category '{category_id} - {category_info['name']}'. Produce a JSON object with:\n\n"
        '{\n'
        '  "category_id": "<str>",\n'
        '  "category_name": "<str>",\n'
        '  "paper_count": <int>,\n'
        '  "executive_summary": "<2-3 paragraph overview of the state of the art>",\n'
        '  "key_themes": [\n'
        '    {\n'
        '      "theme": "<theme name>",\n'
        '      "description": "<1-2 sentences>",\n'
        '      "paper_count": <int>,\n'
        '      "representative_papers": ["<paper title>", ...]\n'
        '    }\n'
        '  ],\n'
        '  "what_is_measured": [\n'
        '    "<specific thing being measured/evaluated>"\n'
        '  ],\n'
        '  "what_is_not_measured": [\n'
        '    "<identified gap - what SHOULD be measured but is not>"\n'
        '  ],\n'
        '  "cognitive_offloading_coverage": {  // ONLY include this if papers in this category\n'
        '    "papers_addressing_it": <int>,  // actually discuss cognitive offloading, over-reliance,\n'
        '    "summary": "<str>",             // or learning science concerns. Omit for categories\n'
        '    "specific_findings": ["..."]    // where it is not relevant.\n'
        '  },\n'
        '  "methodological_trends": [\n'
        '    "<common methodology or approach>"\n'
        '  ],\n'
        '  "notable_benchmarks": [\n'
        '    {\n'
        '      "name": "<benchmark/dataset name>",\n'
        '      "paper_title": "<source paper>",\n'
        '      "what_it_measures": "<brief description>",\n'
        '      "strength": "<why it is notable>"\n'
        '    }\n'
        '  ],\n'
        '  "recommendations": [\n'
        '    "<actionable recommendation for the field>"\n'
        '  ],\n'
        '  "top_papers": [\n'
        '    {\n'
        '      "title": "<paper title>",\n'
        '      "why_important": "<1 sentence>"\n'
        '    }\n'
        '  ]\n'
        '}'
    )


def _build_concern_system_prompt() -> str:
    return (
        "You are a senior education research analyst specialising in the risks and "
        "unintended consequences of AI/LLM use in K-12 education (ages 5-18). You "
        "have deep expertise in learning science, cognitive psychology, educational "
        "technology, and the evidence on how AI tools affect genuine student learning.\n\n"
        "Your task is to synthesise a collection of research papers related to a "
        "specific concern or risk theme and produce a structured analysis of what "
        "the literature says about this risk, how well it is understood, and what "
        "gaps remain.\n\n"
        "IMPORTANT: Focus on what the papers actually say about this concern. "
        "Include both papers that directly study the risk AND papers where the risk "
        "is a secondary finding. Distinguish between empirical evidence and "
        "theoretical/opinion pieces.\n\n"
        "You must respond with ONLY valid JSON -- no markdown fences, no commentary."
    )


def _build_concern_user_prompt(
    concern_id: str,
    concern_info: dict,
    papers: list[ExtractedPaper],
) -> str:
    """Build the synthesis prompt for papers matched to a concern theme."""
    paper_texts = []
    for i, ep in enumerate(papers, 1):
        paper_texts.append(
            f"--- Paper {i} (relevance: {ep.relevance_score}/10) ---\n"
            f"{ep.to_text()}\n"
        )
    combined = "\n\n".join(paper_texts)

    return (
        f"## Concern Theme: {concern_info['name']}\n"
        f"Description: {concern_info['description']}\n\n"
        f"## Papers mentioning this concern ({len(papers)} papers)\n\n"
        f"{combined}\n\n"
        f"## Analysis Instructions\n\n"
        f"These {len(papers)} papers were found by keyword-matching for terms "
        f"related to '{concern_info['name']}'. Some may address the concern "
        f"directly; others may mention it tangentially. Synthesise what the "
        f"literature tells us about this concern.\n\n"
        f"Produce a JSON object with:\n\n"
        '{\n'
        '  "concern_id": "<str>",\n'
        '  "concern_name": "<str>",\n'
        '  "paper_count": <int>,\n'
        '  "papers_directly_addressing": <int>,\n'
        '  "executive_summary": "<2-3 paragraph overview of what research says about this risk>",\n'
        '  "key_findings": [\n'
        '    {\n'
        '      "finding": "<clear statement of finding>",\n'
        '      "evidence_type": "<empirical|theoretical|review|opinion>",\n'
        '      "paper_count": <int>,\n'
        '      "representative_papers": ["<paper title>", ...]\n'
        '    }\n'
        '  ],\n'
        '  "evidence_for_risk": [\n'
        '    "<specific evidence that this risk is real and significant>"\n'
        '  ],\n'
        '  "evidence_against_or_mitigating": [\n'
        '    "<evidence that the risk is overstated, or effective mitigations exist>"\n'
        '  ],\n'
        '  "what_is_measured": [\n'
        '    "<specific metrics or measures used to study this concern>"\n'
        '  ],\n'
        '  "what_is_not_measured": [\n'
        '    "<gaps — what SHOULD be studied about this concern but is not>"\n'
        '  ],\n'
        '  "context_factors": [\n'
        '    "<factors that influence whether the risk manifests — age, subject, tool type, etc.>"\n'
        '  ],\n'
        '  "notable_studies": [\n'
        '    {\n'
        '      "title": "<paper title>",\n'
        '      "design": "<brief method description>",\n'
        '      "key_result": "<main finding relevant to this concern>",\n'
        '      "sample": "<who was studied — age, context, N>"\n'
        '    }\n'
        '  ],\n'
        '  "implications_for_lmics": "<how this concern specifically manifests in low- and middle-income country contexts>",\n'
        '  "recommendations": [\n'
        '    "<actionable recommendation for mitigating this risk>"\n'
        '  ],\n'
        '  "top_papers": [\n'
        '    {\n'
        '      "title": "<paper title>",\n'
        '      "why_important": "<1 sentence>"\n'
        '    }\n'
        '  ]\n'
        '}'
    )


# ── Batching logic ────────────────────────────────────────────────────────────

def _resolve_group_info(group_id: str, mode: str = "framework") -> dict:
    """Lookup display info for a framework category or tool type."""
    if mode == "concern":
        c = CONCERNS.get(group_id, {})
        return {
            "name": c.get("name", group_id),
            "area": "Concern / Risk Theme",
            "description": c.get("description", f"Papers related to concern '{group_id}'."),
        }
    if mode == "tool_type":
        tt = TOOL_TYPES.get(group_id, {})
        return {
            "name": tt.get("name", group_id),
            "area": "Tool Type",
            "description": tt.get("description", f"Papers classified under tool type '{group_id}'."),
        }
    # Default: framework
    return FRAMEWORK.get(group_id, {
        "name": group_id,
        "area": "Unknown",
        "description": "Uncategorized papers",
    })


@dataclass
class BatchRequest:
    """A single request within a batch, corresponding to a group sub-batch."""
    custom_id: str               # e.g. "cat_2-3_batch_1" or "tt_ai_tutor_batch_1"
    category_id: str             # group key (framework id or tool type key)
    papers: list[ExtractedPaper]
    estimated_tokens: int
    mode: str = "framework"      # "framework" or "tool_type"

    def to_api_request(self) -> dict:
        """Convert to the Anthropic batch API request format."""
        group_info = _resolve_group_info(self.category_id, self.mode)
        if self.mode == "concern":
            system = _build_concern_system_prompt()
            user_content = _build_concern_user_prompt(
                self.category_id, group_info, self.papers
            )
        else:
            system = _build_system_prompt()
            user_content = _build_user_prompt(
                self.category_id, group_info, self.papers
            )
        return {
            "custom_id": self.custom_id,
            "params": {
                "model": MODEL,
                "max_tokens": MAX_OUTPUT_TOKENS,
                "system": system,
                "messages": [
                    {
                        "role": "user",
                        "content": user_content,
                    }
                ],
            },
        }


def create_batch_requests(
    category_papers: dict[str, list[ExtractedPaper]],
    target_categories: list[str] | None = None,
    mode: str = "framework",
) -> list[BatchRequest]:
    """
    Split papers into batch requests that fit within context windows.

    Each group is split into sub-batches of ~180K input tokens max.
    mode: "framework" uses "cat_" prefix, "tool_type" uses "tt_" prefix.
    """
    requests: list[BatchRequest] = []
    prefix = "cn" if mode == "concern" else ("tt" if mode == "tool_type" else "cat")

    for gid in sorted(category_papers.keys()):
        if target_categories and gid not in target_categories:
            continue

        papers = category_papers[gid]
        if not papers:
            continue

        # Split into sub-batches by token count
        current_batch: list[ExtractedPaper] = []
        current_tokens = 0
        batch_idx = 1

        # Reserve tokens for system prompt + response structure (~2K)
        prompt_overhead = 2000

        # Sanitize group ID for custom_id (batch API only allows alphanumeric + _-)
        safe_gid = gid.replace(".", "-")

        for ep in papers:
            paper_tokens = ep.extracted_tokens
            if paper_tokens == 0:
                continue

            # Would this paper push us over the limit?
            if current_tokens + paper_tokens > (MAX_TOKENS_PER_BATCH_REQUEST - prompt_overhead - MAX_OUTPUT_TOKENS):
                if current_batch:
                    requests.append(BatchRequest(
                        custom_id=f"{prefix}_{safe_gid}_batch_{batch_idx}",
                        category_id=gid,
                        papers=list(current_batch),
                        estimated_tokens=current_tokens + prompt_overhead,
                        mode=mode,
                    ))
                    batch_idx += 1
                    current_batch = []
                    current_tokens = 0

            current_batch.append(ep)
            current_tokens += paper_tokens

        # Final sub-batch
        if current_batch:
            requests.append(BatchRequest(
                custom_id=f"{prefix}_{safe_gid}_batch_{batch_idx}",
                category_id=gid,
                papers=list(current_batch),
                estimated_tokens=current_tokens + prompt_overhead,
                mode=mode,
            ))

    return requests


# ── Markdown rendering ────────────────────────────────────────────────────────

def render_concern_markdown(data: dict) -> str:
    """Convert a concern analysis JSON object to a readable Markdown document."""
    concern_id = data.get("concern_id", "?")
    concern_name = data.get("concern_name", "Unknown")
    paper_count = data.get("paper_count", 0)
    direct = data.get("papers_directly_addressing", 0)

    lines: list[str] = []
    lines.append(f"# {concern_name}")
    lines.append("")
    lines.append(f"**{paper_count} papers matched** ({direct} directly addressing this concern)")
    lines.append("")

    if data.get("executive_summary"):
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(data["executive_summary"])
        lines.append("")

    findings = data.get("key_findings", [])
    if findings:
        lines.append("## Key Findings")
        lines.append("")
        for f in findings:
            etype = f.get("evidence_type", "")
            lines.append(f"### {f.get('finding', '')}")
            lines.append("")
            lines.append(f"*Evidence type: {etype} | {f.get('paper_count', 0)} papers*")
            papers = f.get("representative_papers", [])
            if papers:
                lines.append("")
                for p in papers:
                    lines.append(f"- {p}")
            lines.append("")

    for_risk = data.get("evidence_for_risk", [])
    if for_risk:
        lines.append("## Evidence For This Risk")
        lines.append("")
        for item in for_risk:
            lines.append(f"- {item}")
        lines.append("")

    against = data.get("evidence_against_or_mitigating", [])
    if against:
        lines.append("## Mitigating Evidence")
        lines.append("")
        for item in against:
            lines.append(f"- {item}")
        lines.append("")

    measured = data.get("what_is_measured", [])
    if measured:
        lines.append("## What Is Being Measured")
        lines.append("")
        for item in measured:
            lines.append(f"- {item}")
        lines.append("")

    not_measured = data.get("what_is_not_measured", [])
    if not_measured:
        lines.append("## Gaps — What Is NOT Being Measured")
        lines.append("")
        for item in not_measured:
            lines.append(f"- {item}")
        lines.append("")

    context = data.get("context_factors", [])
    if context:
        lines.append("## Context Factors")
        lines.append("")
        for item in context:
            lines.append(f"- {item}")
        lines.append("")

    studies = data.get("notable_studies", [])
    if studies:
        lines.append("## Notable Studies")
        lines.append("")
        for s in studies:
            lines.append(f"### {s.get('title', '')}")
            lines.append("")
            if s.get("design"):
                lines.append(f"**Design:** {s['design']}")
            if s.get("sample"):
                lines.append(f"**Sample:** {s['sample']}")
            if s.get("key_result"):
                lines.append(f"**Key result:** {s['key_result']}")
            lines.append("")

    lmics = data.get("implications_for_lmics", "")
    if lmics:
        lines.append("## Implications for LMICs")
        lines.append("")
        lines.append(lmics)
        lines.append("")

    recs = data.get("recommendations", [])
    if recs:
        lines.append("## Recommendations")
        lines.append("")
        for item in recs:
            lines.append(f"- {item}")
        lines.append("")

    top = data.get("top_papers", [])
    if top:
        lines.append("## Top Papers")
        lines.append("")
        for i, p in enumerate(top, 1):
            lines.append(f"{i}. **{p.get('title', '')}**")
            lines.append(f"   {p.get('why_important', '')}")
            lines.append("")

    return "\n".join(lines)


def render_analysis_markdown(data: dict) -> str:
    """
    Convert a category analysis JSON object to a readable Markdown document.
    """
    cat_id = data.get("category_id", "?")
    cat_name = data.get("category_name", "Unknown")
    paper_count = data.get("paper_count", 0)

    lines: list[str] = []

    # Title
    lines.append(f"# {cat_id} — {cat_name}")
    lines.append("")
    lines.append(f"**{paper_count} papers analysed**")
    lines.append("")

    # Executive summary
    if data.get("executive_summary"):
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(data["executive_summary"])
        lines.append("")

    # Key themes
    themes = data.get("key_themes", [])
    if themes:
        lines.append("## Key Themes")
        lines.append("")
        for t in themes:
            name = t.get("theme", "")
            desc = t.get("description", "")
            count = t.get("paper_count", 0)
            papers = t.get("representative_papers", [])
            lines.append(f"### {name}")
            lines.append("")
            lines.append(f"{desc} ({count} papers)")
            lines.append("")
            if papers:
                lines.append("Representative papers:")
                for p in papers:
                    lines.append(f"- {p}")
                lines.append("")

    # What is measured
    measured = data.get("what_is_measured", [])
    if measured:
        lines.append("## What Is Being Measured")
        lines.append("")
        for item in measured:
            lines.append(f"- {item}")
        lines.append("")

    # What is NOT measured (gaps)
    not_measured = data.get("what_is_not_measured", [])
    if not_measured:
        lines.append("## Gaps — What Is NOT Being Measured")
        lines.append("")
        for item in not_measured:
            lines.append(f"- {item}")
        lines.append("")

    # Cognitive offloading
    co = data.get("cognitive_offloading_coverage", {})
    if co:
        lines.append("## Cognitive Offloading Coverage")
        lines.append("")
        co_count = co.get("papers_addressing_it", 0)
        co_summary = co.get("summary", "")
        lines.append(f"**Papers addressing cognitive offloading: {co_count}/{paper_count}**")
        lines.append("")
        if co_summary:
            lines.append(co_summary)
            lines.append("")
        findings = co.get("specific_findings", [])
        if findings:
            lines.append("Specific findings:")
            lines.append("")
            for f in findings:
                lines.append(f"- {f}")
            lines.append("")

    # Methodological trends
    methods = data.get("methodological_trends", [])
    if methods:
        lines.append("## Methodological Trends")
        lines.append("")
        for item in methods:
            lines.append(f"- {item}")
        lines.append("")

    # Notable benchmarks
    benchmarks = data.get("notable_benchmarks", [])
    if benchmarks:
        lines.append("## Notable Benchmarks")
        lines.append("")
        for b in benchmarks:
            name = b.get("name", "")
            paper = b.get("paper_title", "")
            measures = b.get("what_it_measures", "")
            strength = b.get("strength", "")
            lines.append(f"### {name}")
            lines.append("")
            if paper:
                lines.append(f"*From: {paper}*")
                lines.append("")
            if measures:
                lines.append(f"**Measures:** {measures}")
                lines.append("")
            if strength:
                lines.append(f"**Why notable:** {strength}")
                lines.append("")

    # Top papers
    top = data.get("top_papers", [])
    if top:
        lines.append("## Top Papers")
        lines.append("")
        for i, p in enumerate(top, 1):
            title = p.get("title", "")
            why = p.get("why_important", "")
            lines.append(f"{i}. **{title}**")
            lines.append(f"   {why}")
            lines.append("")

    # Recommendations
    recs = data.get("recommendations", [])
    if recs:
        lines.append("## Recommendations")
        lines.append("")
        for item in recs:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines)


def save_analysis(cat_id: str, data: dict, output_dir: Path, file_prefix: str = "category"):
    """Save an analysis as both JSON and Markdown."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    json_path = output_dir / f"{file_prefix}_{cat_id}_analysis.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        if isinstance(existing, list):
            existing.append(data)
        else:
            existing = [existing, data]
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
    else:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # Markdown — use concern renderer for concern analyses
    md_path = output_dir / f"{file_prefix}_{cat_id}_analysis.md"
    if file_prefix == "concern":
        md_content = render_concern_markdown(data)
    else:
        md_content = render_analysis_markdown(data)
    if md_path.exists():
        # Append for multi-batch groups
        with open(md_path, "a", encoding="utf-8") as f:
            f.write("\n\n---\n\n")
            f.write(md_content)
    else:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

    return json_path, md_path


def regenerate_markdown():
    """Regenerate all Markdown files from existing JSON analysis files."""
    # Find category, tool_type, and concern analysis files
    json_files = sorted(
        list(OUTPUT_DIR.glob("category_*_analysis.json"))
        + list(OUTPUT_DIR.glob("tool_type_*_analysis.json"))
        + list(OUTPUT_DIR.glob("concern_*_analysis.json"))
    )
    if not json_files:
        console.print("[yellow]No JSON analysis files found.[/yellow]")
        return

    for json_path in json_files:
        stem = json_path.stem  # e.g. "category_2.3_analysis" or "tool_type_ai_tutor_analysis"
        md_path = json_path.with_suffix(".md")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle single object or list of sub-batch results
        is_concern = json_path.name.startswith("concern_")
        renderer = render_concern_markdown if is_concern else render_analysis_markdown
        if isinstance(data, list):
            parts = [renderer(d) for d in data]
            md_content = "\n\n---\n\n".join(parts)
        else:
            md_content = renderer(data)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        console.print(f"  [green]OK[/green] {md_path.name}")

    console.print(f"\n[bold]Regenerated {len(json_files)} Markdown files.[/bold]")


# ── Report writing (LLM-powered narrative reports) ───────────────────────────

STYLE_GUIDE_PATH = Path(".claude/fab_inc_style_guide.md")
REPORTS_DIR = OUTPUT_DIR / "reports"

REPORT_SYSTEM_PROMPT = (
    "You are a senior education research analyst and expert writer at Fab AI "
    "(ai-for-education.org). You produce authoritative, well-structured research "
    "reports for development sector stakeholders, funders, and education policymakers.\n\n"
    "You write in British English, following the organisation's style guide precisely."
)


def _load_style_guide() -> str:
    """Load the Fab Inc writing style guide."""
    if not STYLE_GUIDE_PATH.exists():
        console.print(f"[yellow]Warning: Style guide not found at {STYLE_GUIDE_PATH}[/yellow]")
        return ""
    return STYLE_GUIDE_PATH.read_text(encoding="utf-8")


def _merge_sub_batch_analyses(data: dict | list) -> dict:
    """
    Merge multiple sub-batch analysis results into a single consolidated analysis.

    When a category has multiple sub-batches, each sub-batch produces its own
    analysis JSON. This function merges them into one combined object.
    """
    if isinstance(data, dict):
        return data  # Already a single result

    if not data:
        return {}

    # Start with the first sub-batch as a base
    merged = {
        "category_id": data[0].get("category_id", ""),
        "category_name": data[0].get("category_name", ""),
        "paper_count": sum(d.get("paper_count", 0) for d in data),
        "executive_summary": "",
        "key_themes": [],
        "what_is_measured": [],
        "what_is_not_measured": [],
        "cognitive_offloading_coverage": {
            "papers_addressing_it": 0,
            "summary": "",
            "specific_findings": [],
        },
        "methodological_trends": [],
        "notable_benchmarks": [],
        "recommendations": [],
        "top_papers": [],
    }

    # Collect all sub-batch content
    summaries = []
    theme_names_seen: set[str] = set()
    measured_seen: set[str] = set()
    not_measured_seen: set[str] = set()
    methods_seen: set[str] = set()
    recs_seen: set[str] = set()
    benchmark_names_seen: set[str] = set()
    paper_titles_seen: set[str] = set()
    co_findings_seen: set[str] = set()

    for d in data:
        if d.get("executive_summary"):
            summaries.append(d["executive_summary"])

        for theme in d.get("key_themes", []):
            tname = theme.get("theme", "")
            if tname and tname not in theme_names_seen:
                theme_names_seen.add(tname)
                merged["key_themes"].append(theme)

        for item in d.get("what_is_measured", []):
            if item not in measured_seen:
                measured_seen.add(item)
                merged["what_is_measured"].append(item)

        for item in d.get("what_is_not_measured", []):
            if item not in not_measured_seen:
                not_measured_seen.add(item)
                merged["what_is_not_measured"].append(item)

        co = d.get("cognitive_offloading_coverage", {})
        merged["cognitive_offloading_coverage"]["papers_addressing_it"] += co.get("papers_addressing_it", 0)
        if co.get("summary"):
            if merged["cognitive_offloading_coverage"]["summary"]:
                merged["cognitive_offloading_coverage"]["summary"] += " " + co["summary"]
            else:
                merged["cognitive_offloading_coverage"]["summary"] = co["summary"]
        for finding in co.get("specific_findings", []):
            if finding not in co_findings_seen:
                co_findings_seen.add(finding)
                merged["cognitive_offloading_coverage"]["specific_findings"].append(finding)

        for item in d.get("methodological_trends", []):
            if item not in methods_seen:
                methods_seen.add(item)
                merged["methodological_trends"].append(item)

        for bench in d.get("notable_benchmarks", []):
            bname = bench.get("name", "")
            if bname and bname not in benchmark_names_seen:
                benchmark_names_seen.add(bname)
                merged["notable_benchmarks"].append(bench)

        for rec in d.get("recommendations", []):
            if rec not in recs_seen:
                recs_seen.add(rec)
                merged["recommendations"].append(rec)

        for paper in d.get("top_papers", []):
            ptitle = paper.get("title", "")
            if ptitle and ptitle not in paper_titles_seen:
                paper_titles_seen.add(ptitle)
                merged["top_papers"].append(paper)

    # Combine executive summaries
    merged["executive_summary"] = "\n\n".join(summaries)

    return merged


def _build_report_prompt(analysis: dict, style_guide: str) -> str:
    """Build the prompt to convert a JSON analysis into a narrative report."""
    analysis_json = json.dumps(analysis, indent=2, ensure_ascii=False)

    return (
        "## Task\n\n"
        "Convert the following structured JSON research analysis into a polished, "
        "narrative research report. This report is part of a series covering how "
        "AI and LLMs are being benchmarked in K-12 education (ages 5-18) across "
        "low- and middle-income countries (LMICs) and globally.\n\n"
        "The audience is education sector funders, policymakers, and development "
        "partners who need to understand what research exists, what is being measured, "
        "what the gaps are, and what should happen next.\n\n"
        "## Writing Style Guide\n\n"
        "Follow this style guide precisely:\n\n"
        f"{style_guide}\n\n"
        "## Report Structure\n\n"
        "Write the report with these sections:\n\n"
        "1. **Title** - Category name as a clear heading\n"
        "2. **Executive Summary** - 2-3 paragraphs providing an authoritative overview. "
        "Lead with the most important finding. Include specific numbers.\n"
        "3. **Key Themes** - Each theme gets its own subsection with a descriptive heading. "
        "Weave in paper references naturally (not as bullet lists). Use bold for key terms.\n"
        "4. **What Is Being Measured** - Narrative description of what the field is evaluating, "
        "with specific metrics and benchmarks highlighted.\n"
        "5. **Critical Gaps** - What is NOT being measured. Frame as opportunities, "
        "not just criticisms. This is where the field needs investment.\n"
        "6. **Cognitive Offloading** (ONLY if the source data includes meaningful "
        "cognitive_offloading_coverage) - How well this area addresses whether AI helps or "
        "hinders genuine learning. If the source data has little or no cognitive offloading "
        "content, SKIP this section entirely — do not fabricate or stretch thin findings.\n"
        "7. **Notable Benchmarks and Datasets** - Highlight the most important evaluation "
        "tools, with what they measure and why they matter.\n"
        "8. **Methodological Trends** - How researchers are approaching this area.\n"
        "9. **Recommendations** - Actionable next steps framed using 'we recommend', "
        "'the field should', with clear agency. Include timeline suggestions where appropriate.\n"
        "10. **Key Papers** - Brief annotated list of the most important papers to read.\n\n"
        "## Model Recency Context\n\n"
        "Today's date is February 2026. Many papers in this analysis were published in "
        "2023-2025 and used models that were current at the time but are now dated. "
        "Use this reference timeline when writing — do NOT describe older models as "
        "'new', 'recent', 'latest', or 'state-of-the-art' unless they genuinely are "
        "as of February 2026.\n\n"
        "Key model release dates (approximate):\n"
        "- GPT-3.5 / ChatGPT: Nov 2022\n"
        "- GPT-4: Mar 2023\n"
        "- GPT-4 Turbo: Nov 2023\n"
        "- GPT-4o: May 2024\n"
        "- GPT-4.5: Feb 2025\n"
        "- Claude 2: Jul 2023\n"
        "- Claude 3 (Haiku/Sonnet/Opus): Mar 2024\n"
        "- Claude 3.5 Sonnet: Jun 2024\n"
        "- Claude 4 Sonnet: May 2025\n"
        "- Gemini 1.0: Dec 2023\n"
        "- Gemini 1.5 Pro: Feb 2024\n"
        "- Gemini 2.0 Flash: Dec 2024\n"
        "- Llama 2: Jul 2023\n"
        "- Llama 3: Apr 2024\n"
        "- Llama 3.1: Jul 2024\n"
        "- Llama 4: Apr 2025\n"
        "- Mistral 7B: Sep 2023\n"
        "- Mixtral 8x7B: Dec 2023\n"
        "- BLOOM/BLOOMZ: Jul 2022\n"
        "- PaLM 2: May 2023\n\n"
        "When referencing models, use phrasing like:\n"
        "- 'GPT-4, which was the leading commercial model at the time of these studies'\n"
        "- 'models available in 2023, including GPT-4 and Claude 2'\n"
        "- 'earlier-generation models such as GPT-3.5'\n"
        "Do NOT say 'state-of-the-art models like GPT-4' — instead contextualise the "
        "model within its era and note where findings may need re-evaluation with "
        "current-generation models.\n\n"
        "## Key Instructions\n\n"
        "- Write in narrative prose, not bullet lists (except for the key papers section)\n"
        "- Use British spelling throughout (programme, organisation, focussed, realise, centre)\n"
        "- Bold key terms and striking statistics\n"
        "- Use em-dashes for parenthetical information\n"
        "- Reference specific papers and benchmarks by name within the narrative\n"
        "- Include specific numbers, percentages, and paper counts\n"
        "- The total report should be approximately 1500-2500 words\n"
        "- Write in Markdown format\n"
        "- Do NOT wrap the output in code fences\n\n"
        "## Source Analysis Data\n\n"
        f"{analysis_json}"
    )


def write_reports(
    target_category: str | None = None,
    dry_run: bool = False,
    realtime: bool = False,
    mode: str = "framework",
):
    """
    Generate narrative reports from collected analysis JSONs.

    Reads each analysis JSON, merges sub-batches if needed,
    and sends to Claude to write a polished report following the style guide.
    """
    style_guide = _load_style_guide()
    if not style_guide:
        console.print("[red]Cannot write reports without the style guide.[/red]")
        return

    # Find analysis JSONs based on mode
    if mode == "concern":
        glob_pattern = "concern_*_analysis.json"
        file_prefix = "concern"
    elif mode == "tool_type":
        glob_pattern = "tool_type_*_analysis.json"
        file_prefix = "tool_type"
    else:
        glob_pattern = "category_*_analysis.json"
        file_prefix = "category"
    json_files = sorted(OUTPUT_DIR.glob(glob_pattern))
    if not json_files:
        console.print(f"[yellow]No {file_prefix} analysis JSON files found. Run --collect first.[/yellow]")
        return

    # Build requests
    report_requests: list[dict] = []
    for json_path in json_files:
        group_id = json_path.stem.replace(f"{file_prefix}_", "").replace("_analysis", "")

        if target_category and group_id != target_category:
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Merge sub-batches
        merged = _merge_sub_batch_analyses(data)
        if not merged:
            continue

        prompt = _build_report_prompt(merged, style_guide)
        token_est = len(prompt) // 4

        report_requests.append({
            "cat_id": group_id,
            "cat_name": merged.get("category_name", group_id),
            "paper_count": merged.get("paper_count", 0),
            "prompt": prompt,
            "tokens": token_est,
            "file_prefix": file_prefix,
        })

    if not report_requests:
        console.print(f"[yellow]No {file_prefix} groups to write reports for.[/yellow]")
        return

    # Summary
    total_tokens = sum(r["tokens"] for r in report_requests)
    label = "Concerns" if mode == "concern" else ("Tool Types" if mode == "tool_type" else "Categories")
    console.print(f"\n[bold]Report Writing ({label})[/bold]")
    console.print(f"  Groups:      {len(report_requests)}")
    console.print(f"  Input tokens: ~{total_tokens:,}")
    console.print(f"  Style guide: {len(style_guide):,} chars\n")

    table = Table(title="Reports to Generate")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Papers", justify="right")
    table.add_column("~Tokens", justify="right")
    for r in report_requests:
        table.add_row(r["cat_id"], r["cat_name"], str(r["paper_count"]), f"{r['tokens']:,}")
    console.print(table)

    if dry_run:
        console.print("\n[yellow]Dry run -- no API calls made.[/yellow]")
        return

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if realtime:
        _write_reports_realtime(report_requests)
    else:
        _write_reports_batch(report_requests, mode=mode)


def _write_reports_realtime(report_requests: list[dict]):
    """Write reports using the standard Messages API (immediate results)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set.[/red]")
        return

    client = anthropic.Anthropic(api_key=api_key)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("{task.completed}/{task.total}"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Writing reports", total=len(report_requests))

        for req in report_requests:
            progress.update(task, description=f"Writing {req['cat_id']} - {req['cat_name']}")

            try:
                resp = client.messages.create(
                    model=REPORT_MODEL,
                    max_tokens=MAX_OUTPUT_TOKENS,
                    system=REPORT_SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": req["prompt"]}],
                )

                report_text = resp.content[0].text.strip()

                # Save as Markdown
                fp = req.get("file_prefix", "category")
                md_path = REPORTS_DIR / f"{fp}_{req['cat_id']}_report.md"
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(report_text)

                console.print(f"  [green]OK[/green] {req['cat_id']} -> {md_path.name} "
                              f"({len(report_text):,} chars)")

            except Exception as exc:
                console.print(f"  [red]Error[/red] {req['cat_id']}: {exc}")

            progress.advance(task)

    console.print(f"\n[bold green]Done! Reports in {REPORTS_DIR}/[/bold green]")


def _write_reports_batch(report_requests: list[dict], mode: str = "framework"):
    """Write reports using the Batch API (50% cost savings)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set.[/red]")
        return

    client = anthropic.Anthropic(api_key=api_key)

    # Build batch requests (plain dicts — same format as the analysis batches)
    report_prefix = "cn-report" if mode == "concern" else ("tt-report" if mode == "tool_type" else "report")
    batch_api_requests = []
    for req in report_requests:
        safe_id = req["cat_id"].replace(".", "-")
        custom_id = f"{report_prefix}_{safe_id}"

        batch_api_requests.append({
            "custom_id": custom_id,
            "params": {
                "model": REPORT_MODEL,
                "max_tokens": MAX_OUTPUT_TOKENS,
                "system": REPORT_SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": req["prompt"]}],
            },
        })

    try:
        batch = client.messages.batches.create(requests=batch_api_requests)
        console.print(f"\n[green]Report batch submitted![/green]")
        console.print(f"  Batch ID:   [cyan]{batch.id}[/cyan]")
        console.print(f"  Requests:   [cyan]{len(batch_api_requests)}[/cyan]")
        console.print(f"  Status:     [yellow]{batch.processing_status}[/yellow]")

        # Save batch state for later collection
        state = BatchState(
            batch_id=batch.id,
            status=batch.processing_status,
            request_count=len(batch_api_requests),
            created_at=batch.created_at.isoformat() if batch.created_at else "",
            custom_ids=[r["custom_id"] for r in batch_api_requests],
        )
        existing_states = load_batch_states()
        existing_states.append(state)
        save_batch_states(existing_states)

        console.print(f"\n  Collect with: [cyan]uv run research_categories.py --collect-reports[/cyan]")

    except anthropic.APIError as e:
        console.print(f"[red]Batch submission failed: {e}[/red]")
        if hasattr(e, "body"):
            console.print(e.body)


def collect_reports():
    """Collect report results from completed batch API calls."""
    states = load_batch_states()
    if not states:
        console.print("[yellow]No batches found.[/yellow]")
        return

    # Find report batches (custom_ids starting with "report_" or "tt-report_")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set.[/red]")
        return

    client = anthropic.Anthropic(api_key=api_key)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    collected = 0

    for state in states:
        if state.status == "collected":
            continue

        # Check if this is a report batch by trying to retrieve and inspect results
        try:
            batch = client.messages.batches.retrieve(state.batch_id)
        except Exception as exc:
            console.print(f"  [red]Failed to retrieve batch {state.batch_id[:16]}...: {exc}[/red]")
            continue

        if batch.processing_status != "ended":
            continue

        # Peek at results to see if they're report batches
        try:
            results_iter = client.messages.batches.results(state.batch_id)
        except Exception as exc:
            console.print(f"  [red]Failed to get results: {exc}[/red]")
            continue

        is_report_batch = False
        for result in results_iter:
            is_cn_report = result.custom_id.startswith("cn-report_")
            is_tt_report = result.custom_id.startswith("tt-report_")
            is_cat_report = result.custom_id.startswith("report_") and not is_tt_report and not is_cn_report

            if is_cn_report or is_tt_report or is_cat_report:
                is_report_batch = True
            else:
                break  # Not a report batch, skip

            if result.result.type == "succeeded":
                msg = result.result.message
                report_text = ""
                for block in msg.content:
                    if hasattr(block, "text"):
                        report_text += block.text

                if is_cn_report:
                    group_id = result.custom_id.replace("cn-report_", "")
                    file_prefix = "concern"
                elif is_tt_report:
                    # tt-report_ai_tutor -> ai_tutor
                    group_id = result.custom_id.replace("tt-report_", "")
                    file_prefix = "tool_type"
                else:
                    # report_2-3 -> 2.3
                    group_id = result.custom_id.replace("report_", "").replace("-", ".")
                    file_prefix = "category"

                md_path = REPORTS_DIR / f"{file_prefix}_{group_id}_report.md"
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(report_text.strip())

                console.print(f"  [green]OK[/green] {group_id} -> {md_path.name} ({len(report_text):,} chars)")
            else:
                console.print(f"  [red]Error[/red] {result.custom_id}: {result.result.type}")

        if is_report_batch:
            state.status = "collected"
            collected += 1

    save_batch_states(states)
    if collected:
        console.print(f"\n[bold green]Collected {collected} report batch(es) -> {REPORTS_DIR}/[/bold green]")
    else:
        console.print("[yellow]No report batches ready to collect.[/yellow]")


# ── Batch state management ────────────────────────────────────────────────────

@dataclass
class BatchState:
    """Tracks submitted batch jobs."""
    batch_id: str = ""
    status: str = "pending"       # pending | submitted | ended | collected
    request_count: int = 0
    created_at: str = ""
    custom_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "batch_id": self.batch_id,
            "status": self.status,
            "request_count": self.request_count,
            "created_at": self.created_at,
            "custom_ids": self.custom_ids,
        }

    @staticmethod
    def from_dict(d: dict) -> "BatchState":
        return BatchState(**d)


def load_batch_states() -> list[BatchState]:
    """Load saved batch states."""
    if not BATCH_STATE_FILE.exists():
        return []
    with open(BATCH_STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [BatchState.from_dict(d) for d in data]


def save_batch_states(states: list[BatchState]):
    """Save batch states to disk."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(BATCH_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in states], f, indent=2)


# ── Batch API operations ─────────────────────────────────────────────────────

def submit_batches(
    batch_requests: list[BatchRequest],
    dry_run: bool = False,
) -> list[BatchState]:
    """Submit batch requests to the Anthropic Batch API."""
    if not batch_requests:
        console.print("[yellow]No requests to submit.[/yellow]")
        return []

    console.print(f"\n[bold]Submitting {len(batch_requests)} requests as batch...[/bold]")

    # Show preview
    table = Table(title="Batch requests")
    table.add_column("ID", style="cyan")
    table.add_column("Category")
    table.add_column("Papers", justify="right")
    table.add_column("Est. tokens", justify="right")
    for req in batch_requests:
        table.add_row(
            req.custom_id,
            req.category_id,
            str(len(req.papers)),
            f"{req.estimated_tokens:,}",
        )
    console.print(table)

    total_tokens = sum(r.estimated_tokens for r in batch_requests)
    console.print(f"\n  Total input tokens: ~{total_tokens:,}")
    console.print(f"  Total output tokens: ~{len(batch_requests) * MAX_OUTPUT_TOKENS:,} (max)")

    # Estimate cost (Sonnet: $3/M input, $15/M output; batch = 50% off)
    input_cost = total_tokens / 1_000_000 * 3.0 * 0.5
    output_cost = len(batch_requests) * MAX_OUTPUT_TOKENS / 1_000_000 * 15.0 * 0.5
    console.print(f"  Estimated cost: ~${input_cost + output_cost:.2f} "
                  f"(input: ${input_cost:.2f}, output: ${output_cost:.2f})")

    if dry_run:
        console.print("\n[yellow]Dry run -- no API calls made.[/yellow]")
        # Save a sample request for inspection
        sample_path = OUTPUT_DIR / "sample_request.json"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(sample_path, "w", encoding="utf-8") as f:
            json.dump(batch_requests[0].to_api_request(), f, indent=2, ensure_ascii=False)
        console.print(f"  Sample request saved to: {sample_path}")
        return []

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set. Add it to .env[/red]")
        return []

    client = anthropic.Anthropic(api_key=api_key)

    # Build API request list
    api_requests = [req.to_api_request() for req in batch_requests]

    console.print("\n[bold]Submitting to Batch API...[/bold]")
    try:
        batch = client.messages.batches.create(requests=api_requests)
    except Exception as exc:
        console.print(f"[red]Batch submission failed: {exc}[/red]")
        return []

    created = ""
    if hasattr(batch, "created_at") and batch.created_at:
        created = str(batch.created_at)

    state = BatchState(
        batch_id=batch.id,
        status="submitted",
        request_count=len(api_requests),
        created_at=created,
        custom_ids=[r.custom_id for r in batch_requests],
    )

    console.print(f"\n  [green]Batch submitted![/green]")
    console.print(f"  Batch ID:      [cyan]{batch.id}[/cyan]")
    console.print(f"  Requests:      {len(api_requests)}")
    console.print(f"  Status:        {batch.processing_status}")
    expires = str(batch.expires_at) if hasattr(batch, "expires_at") and batch.expires_at else "N/A"
    console.print(f"  Expires at:    {expires}")

    # Save state
    states = load_batch_states()
    states.append(state)
    save_batch_states(states)

    return [state]


def check_batch_status():
    """Check and display status of all submitted batches."""
    states = load_batch_states()
    if not states:
        console.print("[yellow]No batches submitted yet.[/yellow]")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set.[/red]")
        return

    client = anthropic.Anthropic(api_key=api_key)

    table = Table(title="Batch Status")
    table.add_column("Batch ID", style="cyan")
    table.add_column("Status")
    table.add_column("Requests", justify="right")
    table.add_column("Succeeded", justify="right", style="green")
    table.add_column("Failed", justify="right", style="red")
    table.add_column("Processing", justify="right", style="yellow")

    for state in states:
        if state.status == "collected":
            table.add_row(
                state.batch_id[:20] + "...",
                "[dim]collected[/dim]",
                str(state.request_count),
                "-", "-", "-",
            )
            continue

        try:
            batch = client.messages.batches.retrieve(state.batch_id)
            counts = batch.request_counts
            table.add_row(
                state.batch_id[:20] + "...",
                batch.processing_status,
                str(state.request_count),
                str(counts.succeeded),
                str(counts.errored + counts.canceled + counts.expired),
                str(counts.processing),
            )
            # Update local state
            if batch.processing_status == "ended":
                state.status = "ended"
        except Exception as exc:
            table.add_row(
                state.batch_id[:20] + "...",
                f"[red]error: {exc}[/red]",
                str(state.request_count),
                "-", "-", "-",
            )

    console.print(table)
    save_batch_states(states)


def collect_results():
    """Collect results from completed batches."""
    states = load_batch_states()
    if not states:
        console.print("[yellow]No batches to collect.[/yellow]")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set.[/red]")
        return

    client = anthropic.Anthropic(api_key=api_key)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    collected_count = 0
    for state in states:
        if state.status == "collected":
            continue

        console.print(f"\n[bold]Collecting batch: {state.batch_id}[/bold]")

        # Check if ended
        try:
            batch = client.messages.batches.retrieve(state.batch_id)
        except Exception as exc:
            console.print(f"  [red]Failed to retrieve batch: {exc}[/red]")
            continue

        if batch.processing_status != "ended":
            console.print(f"  [yellow]Batch still processing ({batch.processing_status}). "
                          f"Skipping.[/yellow]")
            continue

        # Collect results
        try:
            results_iter = client.messages.batches.results(state.batch_id)
        except Exception as exc:
            console.print(f"  [red]Failed to get results: {exc}[/red]")
            continue

        batch_results = {}
        errors = 0
        for result in results_iter:
            custom_id = result.custom_id

            if result.result.type == "succeeded":
                # Extract text response
                msg = result.result.message
                raw_text = ""
                for block in msg.content:
                    if hasattr(block, "text"):
                        raw_text += block.text

                # Try to parse JSON
                try:
                    # Strip markdown fences if present
                    clean = raw_text.strip()
                    if clean.startswith("```"):
                        clean = re.sub(r"^```(?:json)?\s*", "", clean)
                        clean = re.sub(r"\s*```$", "", clean)
                    parsed = json.loads(clean)
                    batch_results[custom_id] = {
                        "status": "success",
                        "data": parsed,
                    }
                    console.print(f"  [green]OK[/green] {custom_id}")
                except json.JSONDecodeError:
                    batch_results[custom_id] = {
                        "status": "parse_error",
                        "raw_text": raw_text[:2000],
                    }
                    errors += 1
                    console.print(f"  [yellow]JSON parse error[/yellow] {custom_id}")
            else:
                batch_results[custom_id] = {
                    "status": "api_error",
                    "error_type": result.result.type,
                }
                errors += 1
                console.print(f"  [red]Error[/red] {custom_id}: {result.result.type}")

        # Save results
        results_path = OUTPUT_DIR / f"batch_{state.batch_id[:16]}_results.json"
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(batch_results, f, indent=2, ensure_ascii=False)

        # Save individual group results (JSON + Markdown)
        for custom_id, result_data in batch_results.items():
            if result_data["status"] == "success":
                # Determine prefix and reverse ID sanitization
                if custom_id.startswith("cn_"):
                    group_id = custom_id.split("_batch_")[0].replace("cn_", "")
                    file_prefix = "concern"
                elif custom_id.startswith("tt_"):
                    group_id = custom_id.split("_batch_")[0].replace("tt_", "")
                    file_prefix = "tool_type"
                else:
                    group_id = custom_id.split("_batch_")[0].replace("cat_", "").replace("-", ".")
                    file_prefix = "category"
                json_path, md_path = save_analysis(group_id, result_data["data"], OUTPUT_DIR, file_prefix=file_prefix)
                console.print(f"    -> {json_path.name}, {md_path.name}")

        state.status = "collected"
        collected_count += 1
        console.print(f"  Results: {len(batch_results) - errors} success, {errors} errors")
        console.print(f"  Saved to: {results_path}")

    save_batch_states(states)
    console.print(f"\n[bold]Collected {collected_count} batches.[/bold]")


# ── Realtime mode (standard API, no batch discount) ──────────────────────────

def run_realtime(
    batch_requests: list[BatchRequest],
    dry_run: bool = False,
):
    """
    Process requests using the standard Messages API (no batch discount,
    but results are immediate). Useful for testing or urgent analysis.
    """
    if not batch_requests:
        console.print("[yellow]No requests to process.[/yellow]")
        return

    if dry_run:
        console.print("[yellow]Dry run -- showing what would be processed:[/yellow]")
        for req in batch_requests:
            console.print(f"  {req.custom_id}: {len(req.papers)} papers, "
                          f"~{req.estimated_tokens:,} tokens")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set.[/red]")
        return

    client = anthropic.Anthropic(api_key=api_key)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("{task.completed}/{task.total}"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Processing categories", total=len(batch_requests))

        for req in batch_requests:
            progress.update(task, description=f"Processing {req.custom_id}")

            api_req = req.to_api_request()
            params = api_req["params"]

            try:
                resp = client.messages.create(
                    model=params["model"],
                    max_tokens=params["max_tokens"],
                    system=params["system"],
                    messages=params["messages"],
                )

                raw = resp.content[0].text.strip()
                if raw.startswith("```"):
                    raw = re.sub(r"^```(?:json)?\s*", "", raw)
                    raw = re.sub(r"\s*```$", "", raw)

                result = json.loads(raw)

                # Save result (JSON + Markdown)
                fp = "concern" if req.mode == "concern" else ("tool_type" if req.mode == "tool_type" else "category")
                json_path, md_path = save_analysis(req.category_id, result, OUTPUT_DIR, file_prefix=fp)
                console.print(f"  [green]OK[/green] {req.custom_id} -> {json_path.name}, {md_path.name}")

            except json.JSONDecodeError:
                console.print(f"  [yellow]JSON parse error[/yellow] for {req.custom_id}")
                # Save raw text for debugging
                err_path = OUTPUT_DIR / f"error_{req.custom_id}.txt"
                with open(err_path, "w", encoding="utf-8") as f:
                    f.write(raw)

            except Exception as exc:
                console.print(f"  [red]Error[/red] {req.custom_id}: {exc}")

            progress.advance(task)

    console.print(f"\n[bold green]Done! Results in {OUTPUT_DIR}/[/bold green]")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Run SoTA research analysis by category or tool type using the Anthropic Batch API."
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check status of submitted batches.",
    )
    parser.add_argument(
        "--collect",
        action="store_true",
        help="Collect results from completed batches.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be submitted without making API calls.",
    )
    parser.add_argument(
        "--category", "-c",
        type=str,
        default=None,
        help="Only process a specific group (e.g. '2.3' or 'ai_tutor').",
    )
    parser.add_argument(
        "--min-relevance",
        type=int,
        default=7,
        help="Minimum relevance score for papers to include (default: 7).",
    )
    parser.add_argument(
        "--profile", "-p",
        choices=list(PROFILES.keys()),
        default="standard",
        help="Extraction profile: lean, standard, deep, full (default: standard).",
    )
    parser.add_argument(
        "--sections",
        type=str,
        default=None,
        help="Comma-separated list of sections to extract (overrides profile).",
    )
    parser.add_argument(
        "--realtime",
        action="store_true",
        help="Use standard API instead of batch API (immediate results, full price).",
    )
    parser.add_argument(
        "--regenerate-md",
        action="store_true",
        help="Regenerate Markdown files from existing JSON analysis files.",
    )
    parser.add_argument(
        "--write-reports",
        action="store_true",
        help="Generate narrative reports from collected analysis JSONs using LLM.",
    )
    parser.add_argument(
        "--collect-reports",
        action="store_true",
        help="Collect narrative report results from completed batch API calls.",
    )
    parser.add_argument(
        "--tool-types",
        action="store_true",
        help="Group papers by tool type (ai_tutor, pal, teacher_support) instead of framework category.",
    )
    parser.add_argument(
        "--concerns",
        action="store_true",
        help="Group papers by concern/risk theme (cognitive offloading, productive struggle, etc.).",
    )
    args = parser.parse_args()

    if args.concerns:
        mode = "concern"
    elif args.tool_types:
        mode = "tool_type"
    else:
        mode = "framework"

    # Regenerate markdown mode
    if args.regenerate_md:
        regenerate_markdown()
        return

    # Write reports mode
    if args.write_reports:
        write_reports(
            target_category=args.category,
            dry_run=args.dry_run,
            realtime=args.realtime,
            mode=mode,
        )
        return

    # Collect reports mode
    if args.collect_reports:
        collect_reports()
        return

    # Status check mode
    if args.status:
        check_batch_status()
        return

    # Collect mode
    if args.collect:
        collect_results()
        return

    # Parse custom sections
    custom_sections = None
    if args.sections:
        custom_sections = {s.strip() for s in args.sections.split(",")}

    # Extraction + submission mode
    group_label = "tool types" if mode == "tool_type" else "framework categories"
    profile_label = f"custom ({args.sections})" if custom_sections else args.profile
    console.print(f"[bold]Loading and extracting paper sections...[/bold]  "
                  f"group_by=[cyan]{group_label}[/cyan]  profile=[cyan]{profile_label}[/cyan]")
    grouped_papers, stats = load_and_extract_all(
        min_relevance=args.min_relevance,
        profile=args.profile,
        target_sections=custom_sections,
        group_by=mode,
    )

    console.print(f"  Papers: {stats['total_papers']}")
    console.print(f"  Groups: {stats['groups']}")
    console.print(f"  Extracted tokens: {stats['total_extracted_tokens']:,}")
    console.print(f"  Compression: {stats['compression_ratio']:.1%} of original\n")

    # Target filter
    target = [args.category] if args.category else None

    # Create batch requests
    batch_requests = create_batch_requests(grouped_papers, target_categories=target, mode=mode)

    if not batch_requests:
        console.print("[yellow]No batch requests to submit.[/yellow]")
        return

    if args.realtime:
        run_realtime(batch_requests, dry_run=args.dry_run)
    else:
        submit_batches(batch_requests, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
