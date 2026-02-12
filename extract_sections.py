"""
Smart Section Extractor for Academic Papers
============================================

Extracts configurable sections from parsed academic papers, with automatic
fallback when papers have sparse or missing sections.

## Extraction Profiles

Choose how much of each paper to keep:

  Profile   | Sections kept                                        | ~Tokens | Compression
  ----------|------------------------------------------------------|---------|------------
  lean      | Abstract + Conclusion                                |   ~900  | 94% reduction
  standard  | Abstract + Intro + Results + Discussion + Conclusion |  ~2,500 | 83% reduction
  deep      | standard + Methods + Related Work + Limitations      |  ~4,500 | 69% reduction
  full      | Everything (no extraction)                           | ~14,500 | 0%

Or pass --sections to pick exactly which sections to keep.

## Fallback Strategy

When a paper doesn't have enough of the requested sections, we don't send a
tiny stub. Instead:

  1. Try extracting the requested sections.
  2. If extracted text < MIN_EXTRACT_CHARS, progressively add more sections
     (methods, related work, experiments, evaluation, etc.) until we reach
     the minimum.
  3. If we STILL don't have enough (e.g. paper has no detectable headings,
     or is a very short paper), fall back to a head/tail slice:
     - First ~60% of MIN_EXTRACT_CHARS from the start of the paper
     - Last ~40% from the end (usually contains conclusion/discussion)

This guarantees every paper contributes a useful amount of context.

## Section Detection

We detect sections via numbered headings (e.g. "1 Introduction", "2. Methods")
which are present in 99.8% of our parsed papers. Fallback to keyword matching
for unnumbered papers.

Usage:
    # CLI — preview stats with different profiles
    uv run extract_sections.py                       # standard profile
    uv run extract_sections.py --profile deep        # include methods/related work
    uv run extract_sections.py --profile lean        # just abstract + conclusion
    uv run extract_sections.py --sections abstract,results,conclusion  # custom

    # Python API
    from extract_sections import extract_key_sections, load_and_extract_all, PROFILES

    # Single paper with standard profile
    paper = extract_key_sections(text, title="...", profile="standard")

    # Custom section selection
    paper = extract_key_sections(text, title="...", target_sections={"abstract", "methods"})

    # All high-relevance papers, grouped by category
    batches, stats = load_and_extract_all(min_relevance=7, profile="standard")
"""

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

JSONL_PATH = Path("output/all_papers.jsonl")
SCORES_PATH = Path("output/paper_scores.json")
BENCHMARKS_PATH = Path("website/static/benchmarks.json")

# Minimum extracted chars before triggering fallback.
# ~2000 chars ≈ 500 tokens — anything less is too sparse to be useful.
MIN_EXTRACT_CHARS = 2000

# ── Section definitions ──────────────────────────────────────────────────────

# Canonical section names and their common variants in papers.
# Each key is the canonical name; values are strings the heading might match.
SECTION_VARIANTS: dict[str, set[str]] = {
    "abstract": {
        "abstract",
    },
    "introduction": {
        "introduction", "overview",
    },
    "related work": {
        "related work", "literature review", "background",
        "prior work", "related studies",
    },
    "methods": {
        "methodology", "methods", "method", "approach",
        "proposed method", "proposed approach", "system design",
        "system overview", "architecture", "materials and methods",
        "procedure", "design", "implementation",
    },
    "results": {
        "results", "findings", "experimental results",
        "experiment", "experiments", "evaluation",
    },
    "discussion": {
        "discussion",
    },
    "conclusion": {
        "conclusion", "conclusions", "concluding remarks",
        "summary", "summary and conclusion", "summary and conclusions",
        "conclusion and future work", "conclusions and future work",
        "discussion and conclusion", "discussion and conclusions",
    },
    "limitations": {
        "limitations", "limitation", "future work",
        "limitations and future work",
    },
    "dataset": {
        "dataset", "data collection", "data", "corpus",
        "benchmark", "setup", "experimental setup",
    },
    "analysis": {
        "analysis", "error analysis", "case study", "case studies",
        "ablation", "ablation study",
    },
}

# Sections to always skip (never useful for synthesis)
ALWAYS_SKIP: set[str] = {
    "references", "bibliography",
    "acknowledgement", "acknowledgements", "acknowledgment", "acknowledgments",
    "appendix", "supplementary", "supplementary material",
    "author contributions", "funding", "conflicts of interest",
    "data availability", "ethics statement", "compliance with ethical standards",
}

# Build reverse lookup: variant -> canonical name
_VARIANT_TO_CANONICAL: dict[str, str] = {}
for canonical, variants in SECTION_VARIANTS.items():
    for v in variants:
        _VARIANT_TO_CANONICAL[v] = canonical

# All known section keywords for heading detection
ALL_SECTION_KEYWORDS: list[str] = sorted(
    set(_VARIANT_TO_CANONICAL.keys()) | ALWAYS_SKIP | {
        "framework", "model", "case study", "case studies",
    },
    key=lambda x: -len(x),  # Match longer phrases first
)

# ── Profiles ──────────────────────────────────────────────────────────────────

PROFILES: dict[str, set[str]] = {
    "lean": {"abstract", "conclusion"},
    "standard": {"abstract", "introduction", "results", "discussion", "conclusion", "limitations"},
    "deep": {"abstract", "introduction", "related work", "methods", "results", "discussion", "conclusion", "limitations"},
    "full": set(SECTION_VARIANTS.keys()),  # everything
}

# Fallback priority: when extracted text is too small, add sections in this order
FALLBACK_PRIORITY: list[str] = [
    "abstract", "introduction", "conclusion", "results", "discussion",
    "limitations", "methods", "related work", "dataset", "analysis",
]


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class ExtractedPaper:
    """A paper with only its key sections extracted."""
    paper_id: str
    title: str
    sections: dict[str, str]       # section_name -> text
    total_chars: int               # original full text length
    extracted_chars: int           # extracted text length
    section_count: int             # how many target sections found
    used_fallback: bool = False    # True if fallback was triggered
    year: int | None = None
    relevance_score: int = 0
    framework_ids: list[str] = field(default_factory=list)
    tool_types: list[str] = field(default_factory=list)
    summary: str = ""

    @property
    def compression_ratio(self) -> float:
        if self.total_chars == 0:
            return 0.0
        return self.extracted_chars / self.total_chars

    @property
    def extracted_tokens(self) -> int:
        """Rough token estimate (4 chars per token)."""
        return self.extracted_chars // 4

    def to_text(self) -> str:
        """Render extracted sections as readable text for LLM input."""
        parts = [f"# {self.title}"]
        if self.summary:
            parts.append(f"\n**Summary**: {self.summary}")
        for sec_name, sec_text in self.sections.items():
            parts.append(f"\n## {sec_name.title()}\n{sec_text}")
        return "\n".join(parts)


# ── Heading detection ─────────────────────────────────────────────────────────

_NUMBERED_HEADING = re.compile(
    r"^(\d+\.?\d*\.?\s+)(.+)$"
)

_ROMAN_HEADING = re.compile(
    r"^((?:I{1,3}|IV|V(?:I{0,3})?|IX|X(?:I{0,3})?)\.?\s+)(.+)$"
)


def _detect_headings(lines: list[str]) -> list[tuple[int, str, str]]:
    """
    Detect section headings in paper text.

    Returns list of (line_index, normalized_heading, raw_heading).
    """
    headings: list[tuple[int, str, str]] = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or len(stripped) > 120:
            continue

        heading_text = None

        # Pattern 1: Numbered heading (e.g. "1 Introduction", "3.2 Results")
        m = _NUMBERED_HEADING.match(stripped)
        if m and len(stripped) < 100:
            heading_text = m.group(2).strip()

        # Pattern 2: Roman numeral heading (e.g. "III. METHODS")
        if not heading_text:
            m = _ROMAN_HEADING.match(stripped)
            if m and len(stripped) < 100:
                heading_text = m.group(2).strip()

        # Pattern 3: Known keyword on its own line (ALL CAPS or Title Case)
        if not heading_text:
            lower = stripped.lower()
            for kw in ALL_SECTION_KEYWORDS:
                if lower == kw or lower == kw + "." or lower == kw + ":":
                    heading_text = kw
                    break
                if stripped.isupper() and lower.startswith(kw):
                    heading_text = kw
                    break

        if heading_text:
            normalized = heading_text.lower().strip().rstrip(".:;")
            headings.append((i, normalized, stripped))

    return headings


def _normalize_heading(heading: str) -> str | None:
    """Map a detected heading to its canonical section name, or None if unknown."""
    lower = heading.lower()
    # Try exact match first
    if lower in _VARIANT_TO_CANONICAL:
        return _VARIANT_TO_CANONICAL[lower]
    # Try prefix match (for compound headings like "3.1 Experimental Setup")
    for variant in sorted(_VARIANT_TO_CANONICAL.keys(), key=lambda x: -len(x)):
        if lower.startswith(variant):
            return _VARIANT_TO_CANONICAL[variant]
    # Check if it's a skip section
    for skip in sorted(ALWAYS_SKIP, key=lambda x: -len(x)):
        if lower == skip or lower.startswith(skip):
            return None  # Signal to skip
    return None


def _is_skip_heading(heading: str) -> bool:
    """Check if a heading should always be skipped."""
    lower = heading.lower()
    for skip in ALWAYS_SKIP:
        if lower == skip or lower.startswith(skip):
            return True
    return False


# ── Main extraction ──────────────────────────────────────────────────────────

def _extract_all_sections(
    lines: list[str],
    headings: list[tuple[int, str, str]],
    max_section_chars: int,
) -> dict[str, str]:
    """
    Extract ALL identifiable sections from the paper (keyed by canonical name).
    This is the raw material — filtering by profile happens after.
    """
    all_sections: dict[str, str] = {}

    for idx, (line_no, normalized, raw) in enumerate(headings):
        if _is_skip_heading(normalized):
            continue

        canonical = _normalize_heading(normalized)
        if canonical is None:
            # Unknown section — keep under raw name for fallback use
            canonical = normalized

        # Get text from this heading to the next heading
        start = line_no
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        section_text = "\n".join(lines[start:end]).strip()

        # Cap section length
        if len(section_text) > max_section_chars:
            section_text = section_text[:max_section_chars] + "\n[... section truncated ...]"

        # Keep first occurrence of each canonical section
        if canonical not in all_sections:
            all_sections[canonical] = section_text

    return all_sections


def extract_key_sections(
    text: str,
    title: str = "",
    profile: str = "standard",
    target_sections: set[str] | None = None,
    max_section_chars: int = 8000,
    min_extract_chars: int = MIN_EXTRACT_CHARS,
) -> ExtractedPaper:
    """
    Extract key sections from a parsed paper's full text.

    Args:
        text: Full paper text.
        title: Paper title (for output).
        profile: One of "lean", "standard", "deep", "full".
        target_sections: Explicit set of canonical section names to extract.
                         Overrides profile if provided.
        max_section_chars: Cap per section to avoid runaway extraction.
        min_extract_chars: Minimum total extracted chars before fallback kicks in.

    Returns:
        ExtractedPaper with extracted sections.
    """
    total_chars = len(text)
    lines = text.split("\n")
    headings = _detect_headings(lines)

    # Determine which sections we want
    wanted = target_sections if target_sections else PROFILES.get(profile, PROFILES["standard"])

    # ── Case 1: No headings detected at all ──
    if not headings:
        return _fallback_head_tail(text, title, total_chars, min_extract_chars)

    # ── Case 2: Normal extraction ──
    # Extract all available sections
    all_sections = _extract_all_sections(lines, headings, max_section_chars)

    # Also grab pre-heading header (title, authors, sometimes abstract before "1 Introduction")
    first_heading_line = headings[0][0]
    header_text = "\n".join(lines[:min(first_heading_line, 20)]).strip()

    # Select the wanted sections (preserve order of FALLBACK_PRIORITY for readability)
    sections: dict[str, str] = {}

    # Add header if no abstract found
    if header_text and "abstract" not in all_sections and len(header_text) > 50:
        sections["header"] = header_text[:1000]

    for sec_name in FALLBACK_PRIORITY:
        if sec_name in wanted and sec_name in all_sections:
            sections[sec_name] = all_sections[sec_name]

    # Also add any wanted sections not in FALLBACK_PRIORITY order
    for sec_name in wanted:
        if sec_name in all_sections and sec_name not in sections:
            sections[sec_name] = all_sections[sec_name]

    extracted_chars = sum(len(v) for v in sections.values())

    # ── Fallback: if too little was extracted, progressively add more sections ──
    used_fallback = False
    if extracted_chars < min_extract_chars:
        used_fallback = True
        for sec_name in FALLBACK_PRIORITY:
            if sec_name not in sections and sec_name in all_sections:
                sections[sec_name] = all_sections[sec_name]
                extracted_chars = sum(len(v) for v in sections.values())
                if extracted_chars >= min_extract_chars:
                    break

    # If we've exhausted all known sections and still too small, add any remaining
    if extracted_chars < min_extract_chars:
        for sec_name, sec_text in all_sections.items():
            if sec_name not in sections:
                sections[sec_name] = sec_text
                extracted_chars = sum(len(v) for v in sections.values())
                if extracted_chars >= min_extract_chars:
                    break

    # Ultimate fallback: if section-based extraction still too small, use head/tail
    if extracted_chars < min_extract_chars:
        return _fallback_head_tail(text, title, total_chars, min_extract_chars)

    return ExtractedPaper(
        paper_id="",
        title=title,
        sections=sections,
        total_chars=total_chars,
        extracted_chars=extracted_chars,
        section_count=len(sections),
        used_fallback=used_fallback,
    )


def _fallback_head_tail(
    text: str,
    title: str,
    total_chars: int,
    min_chars: int,
) -> ExtractedPaper:
    """
    Last-resort fallback: take text from the head and tail of the paper.

    Strategy: 60% from the start (title, abstract, introduction context),
    40% from the end (conclusion, discussion, final remarks).
    """
    # If the paper is small enough, just use the whole thing
    if total_chars <= min_chars * 2:
        return ExtractedPaper(
            paper_id="",
            title=title,
            sections={"full_text": text},
            total_chars=total_chars,
            extracted_chars=total_chars,
            section_count=1,
            used_fallback=True,
        )

    head_chars = int(min_chars * 0.6)
    tail_chars = int(min_chars * 0.4)

    sections: dict[str, str] = {
        "opening": text[:head_chars].strip(),
        "closing": text[-tail_chars:].strip(),
    }

    extracted_chars = sum(len(v) for v in sections.values())

    return ExtractedPaper(
        paper_id="",
        title=title,
        sections=sections,
        total_chars=total_chars,
        extracted_chars=extracted_chars,
        section_count=2,
        used_fallback=True,
    )


# ── Batch loading ─────────────────────────────────────────────────────────────

def load_papers_jsonl() -> dict[str, dict]:
    """Load all parsed papers from JSONL. Returns {paper_id: record}."""
    papers = {}
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                p = json.loads(line)
                papers[p["paper_id"]] = p
    return papers


def load_scores() -> dict[str, dict]:
    """Load paper scores. Returns {paper_id: score_dict}."""
    if not SCORES_PATH.exists():
        return {}
    with open(SCORES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {s["paper_id"]: s for s in data if s.get("paper_id")}


def load_benchmarks() -> list[dict]:
    """Load benchmarks.json for category assignments."""
    if not BENCHMARKS_PATH.exists():
        return []
    with open(BENCHMARKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_and_extract_all(
    min_relevance: int = 7,
    profile: str = "standard",
    target_sections: set[str] | None = None,
    min_extract_chars: int = MIN_EXTRACT_CHARS,
    group_by: str = "framework",
) -> tuple[dict[str, list[ExtractedPaper]], dict]:
    """
    Load all high-relevance papers, extract key sections, and group them.

    Args:
        min_relevance: Minimum relevance score (1-10) to include.
        profile: Extraction profile ("lean", "standard", "deep", "full").
        target_sections: Explicit section set (overrides profile).
        min_extract_chars: Minimum chars per paper before fallback.
        group_by: Grouping key — "framework" (default) or "tool_type".

    Returns:
        (grouped_papers, stats) where:
        - grouped_papers: {group_key: [ExtractedPaper, ...]}
        - stats: summary statistics dict
    """
    papers = load_papers_jsonl()
    scores = load_scores()

    # Filter to high-relevance papers that have parsed text
    relevant_ids = {
        pid for pid, s in scores.items()
        if s.get("relevance_score", 0) >= min_relevance
        and s.get("status") == "scored"
    }

    # Extract sections
    extracted: dict[str, ExtractedPaper] = {}
    fallback_count = 0
    for pid in relevant_ids:
        if pid not in papers:
            continue
        p = papers[pid]
        text = p.get("text", "")
        if len(text) < 100:
            continue

        ep = extract_key_sections(
            text,
            title=p.get("title", ""),
            profile=profile,
            target_sections=target_sections,
            min_extract_chars=min_extract_chars,
        )
        ep.paper_id = pid
        ep.relevance_score = scores[pid].get("relevance_score", 0)
        ep.framework_ids = scores[pid].get("framework_ids", [])
        ep.tool_types = scores[pid].get("tool_types", [])
        ep.summary = scores[pid].get("summary", "")
        extracted[pid] = ep
        if ep.used_fallback:
            fallback_count += 1

    # Group by the requested dimension
    grouped_papers: dict[str, list[ExtractedPaper]] = defaultdict(list)
    if group_by == "concern":
        # Keyword-match papers to concern themes
        from config import CONCERNS
        import re as _re

        for ep in extracted.values():
            # Build a searchable blob from title + summary + extracted text
            blob = (ep.title + " " + ep.summary + " " + ep.to_text()).lower()
            matched_any = False
            for concern_key, concern_info in CONCERNS.items():
                for kw in concern_info["keywords"]:
                    if _re.search(r'\b' + _re.escape(kw.lower()) + r'\b', blob):
                        grouped_papers[concern_key].append(ep)
                        matched_any = True
                        break  # one keyword match is enough per concern
            # Don't add to uncategorized — we only want matched papers
    elif group_by == "tool_type":
        for ep in extracted.values():
            for tt in ep.tool_types:
                grouped_papers[tt].append(ep)
            if not ep.tool_types:
                grouped_papers["uncategorized"].append(ep)
    else:
        # Default: group by framework category
        for ep in extracted.values():
            for fid in ep.framework_ids:
                grouped_papers[fid].append(ep)
            if not ep.framework_ids:
                grouped_papers["uncategorized"].append(ep)

    # Sort each group by relevance (highest first)
    for key in grouped_papers:
        grouped_papers[key].sort(key=lambda x: -x.relevance_score)

    # Stats
    total_original = sum(ep.total_chars for ep in extracted.values())
    total_extracted = sum(ep.extracted_chars for ep in extracted.values())
    stats = {
        "total_papers": len(extracted),
        "total_original_chars": total_original,
        "total_extracted_chars": total_extracted,
        "total_original_tokens": total_original // 4,
        "total_extracted_tokens": total_extracted // 4,
        "compression_ratio": total_extracted / total_original if total_original else 0,
        "groups": len(grouped_papers),
        "group_by": group_by,
        "avg_sections_per_paper": (
            sum(ep.section_count for ep in extracted.values()) / len(extracted)
            if extracted else 0
        ),
        "fallback_count": fallback_count,
        "fallback_pct": fallback_count / len(extracted) * 100 if extracted else 0,
    }

    return dict(grouped_papers), stats


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    """Print extraction stats and a preview."""
    from rich.console import Console
    from rich.table import Table

    parser = argparse.ArgumentParser(
        description="Smart section extractor for academic papers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Profiles:\n"
            "  lean      Abstract + Conclusion (~900 tokens, 94%% reduction)\n"
            "  standard  Abstract + Intro + Results + Discussion + Conclusion + Limitations\n"
            "            (~2,500 tokens, 83%% reduction)\n"
            "  deep      standard + Methods + Related Work (~4,500 tokens, 69%% reduction)\n"
            "  full      All sections (~14,500 tokens, no reduction)\n"
            "\n"
            "Available sections for --sections:\n"
            "  abstract, introduction, related work, methods, results, discussion,\n"
            "  conclusion, limitations, dataset, analysis\n"
        ),
    )
    parser.add_argument(
        "--profile", "-p",
        choices=list(PROFILES.keys()),
        default="standard",
        help="Extraction profile (default: standard).",
    )
    parser.add_argument(
        "--sections", "-s",
        type=str,
        default=None,
        help="Comma-separated list of sections to extract (overrides profile).",
    )
    parser.add_argument(
        "--min-relevance",
        type=int,
        default=7,
        help="Minimum relevance score (default: 7).",
    )
    parser.add_argument(
        "--min-chars",
        type=int,
        default=MIN_EXTRACT_CHARS,
        help=f"Minimum extracted chars per paper before fallback (default: {MIN_EXTRACT_CHARS}).",
    )
    args = parser.parse_args()

    # Parse custom sections
    custom_sections = None
    if args.sections:
        custom_sections = {s.strip() for s in args.sections.split(",")}
        unknown = custom_sections - set(SECTION_VARIANTS.keys())
        if unknown:
            print(f"Warning: unknown sections {unknown}. "
                  f"Available: {sorted(SECTION_VARIANTS.keys())}")

    console = Console()
    profile_name = f"custom ({args.sections})" if custom_sections else args.profile
    console.print(f"[bold]Smart Section Extractor[/bold]  profile=[cyan]{profile_name}[/cyan]\n")

    if not custom_sections:
        wanted = PROFILES[args.profile]
        console.print(f"  Sections: {', '.join(sorted(wanted))}\n")

    category_papers, stats = load_and_extract_all(
        min_relevance=args.min_relevance,
        profile=args.profile,
        target_sections=custom_sections,
        min_extract_chars=args.min_chars,
    )

    console.print(f"[bold]Extraction stats:[/bold]")
    console.print(f"  Papers extracted:    [cyan]{stats['total_papers']}[/cyan]")
    console.print(f"  Original tokens:     [dim]{stats['total_original_tokens']:,}[/dim]")
    console.print(f"  Extracted tokens:    [green]{stats['total_extracted_tokens']:,}[/green]")
    ratio = stats['compression_ratio'] * 100
    console.print(f"  Compression:         [yellow]{ratio:.1f}%[/yellow] of original")
    console.print(f"  Avg sections/paper:  [dim]{stats['avg_sections_per_paper']:.1f}[/dim]")
    console.print(f"  Fallback used:       [dim]{stats['fallback_count']} papers "
                  f"({stats['fallback_pct']:.1f}%)[/dim]")

    # Category breakdown
    table = Table(title="\nPer-category breakdown")
    table.add_column("Category", style="cyan")
    table.add_column("Papers", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Fallbacks", justify="right", style="dim")
    table.add_column("Batches (180K)", justify="right")

    total_batches = 0
    for fid in sorted(category_papers.keys()):
        papers = category_papers[fid]
        tokens = sum(ep.extracted_tokens for ep in papers)
        fallbacks = sum(1 for ep in papers if ep.used_fallback)
        batches = max(1, (tokens + 179_999) // 180_000)
        total_batches += batches
        table.add_row(fid, str(len(papers)), f"{tokens:,}", str(fallbacks), str(batches))

    console.print(table)
    console.print(f"\n  [bold]Total batch API calls needed: ~{total_batches}[/bold]")

    # Profile comparison
    console.print("\n[bold]Profile comparison (all profiles):[/bold]")
    comp_table = Table()
    comp_table.add_column("Profile", style="cyan")
    comp_table.add_column("Tokens", justify="right")
    comp_table.add_column("Compression", justify="right")
    comp_table.add_column("Fallbacks", justify="right")
    comp_table.add_column("Batches", justify="right")

    for pname in ["lean", "standard", "deep", "full"]:
        cp, st = load_and_extract_all(
            min_relevance=args.min_relevance,
            profile=pname,
            min_extract_chars=args.min_chars,
        )
        tok = st["total_extracted_tokens"]
        rat = st["compression_ratio"] * 100
        fb = st["fallback_count"]
        total_b = 0
        for papers in cp.values():
            t = sum(ep.extracted_tokens for ep in papers)
            total_b += max(1, (t + 179_999) // 180_000)
        marker = " <--" if pname == args.profile else ""
        comp_table.add_row(
            f"{pname}{marker}", f"{tok:,}", f"{rat:.1f}%", str(fb), str(total_b)
        )

    console.print(comp_table)

    # Show a few sample extractions
    console.print("\n[bold]Sample extractions:[/bold]")
    shown = 0
    for fid in sorted(category_papers.keys()):
        for ep in category_papers[fid][:1]:
            fb = " [yellow](fallback)[/yellow]" if ep.used_fallback else ""
            console.print(f"\n  [cyan]{fid}[/cyan]: {ep.title[:80]}{fb}")
            console.print(f"    Sections: {list(ep.sections.keys())}")
            console.print(f"    {ep.total_chars:,} -> {ep.extracted_chars:,} chars "
                          f"({ep.compression_ratio:.0%})")
            shown += 1
            if shown >= 3:
                break
        if shown >= 3:
            break


if __name__ == "__main__":
    main()
