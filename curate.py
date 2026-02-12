"""
Curate benchmarks: apply human review decisions and regenerate website data.

Workflow:
  1. Run the pipeline:          uv run main.py
  2. Sync to website:           uv run curate.py sync
  3. Review on website:         cd website && npm run dev
  4. Export dismissed list:     (click "Export" button on website)
  5. Apply dismissals:          uv run curate.py apply dismissed-benchmarks.json
  6. Redeploy website:          cd website && npm run build

Other commands:
  uv run curate.py sync                         # Pipeline JSON → website benchmarks.ts
  uv run curate.py apply <dismissed.json>        # Remove dismissed entries & regenerate
  uv run curate.py stats                         # Show current benchmark counts
"""

import json
import os
import re
import sys
from pathlib import Path

PIPELINE_JSON = "output/education_benchmark_mapping.json"
S2_DETAILS_JSON = "output/s2_paper_details.json"
PAPER_SCORES_JSON = "output/paper_scores.json"
WEBSITE_BENCHMARKS_TS = "website/src/lib/data/benchmarks.ts"
WEBSITE_BENCHMARKS_JSON = "website/static/benchmarks.json"
DISMISSED_ARCHIVE = "output/dismissed_slugs.json"
RESEARCH_REPORTS_DIR = "output/research/reports"
WEBSITE_RESEARCH_DIR = "website/static/research"


def slugify(name: str) -> str:
    """Match the JS slugify function in benchmarks.ts."""
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def load_pipeline_entries() -> list[dict]:
    """Load entries from the pipeline JSON output."""
    if not os.path.exists(PIPELINE_JSON):
        print(f"Error: {PIPELINE_JSON} not found. Run 'uv run main.py' first.")
        sys.exit(1)
    with open(PIPELINE_JSON, "r", encoding="utf-8") as f:
        entries = json.load(f)
    print(f"Loaded {len(entries)} entries from {PIPELINE_JSON}")
    return entries


def load_dismissed(path: str) -> set[str]:
    """Load dismissed slugs from a JSON file."""
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        slugs = json.load(f)
    if not isinstance(slugs, list):
        print(f"Error: {path} should contain a JSON array of slug strings.")
        sys.exit(1)
    return set(slugs)


def load_archived_dismissed() -> set[str]:
    """Load previously dismissed slugs from the archive."""
    if os.path.exists(DISMISSED_ARCHIVE):
        with open(DISMISSED_ARCHIVE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return set(data)
    return set()


def save_archived_dismissed(slugs: set[str]):
    """Save dismissed slugs to the archive (accumulates over time)."""
    os.makedirs(os.path.dirname(DISMISSED_ARCHIVE) or ".", exist_ok=True)
    with open(DISMISSED_ARCHIVE, "w", encoding="utf-8") as f:
        json.dump(sorted(slugs), f, indent=2)
    print(f"Archived {len(slugs)} dismissed slugs -> {DISMISSED_ARCHIVE}")


def _build_s2_lookup(s2_details: list[dict]) -> dict[str, dict]:
    """Build a lookup dict from S2 paper details, indexed by paper ID and ArXiv ID."""
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


def _find_s2_detail(source_url: str, s2_lookup: dict[str, dict]) -> dict | None:
    """Try to find the S2 paper detail for an entry by its source URL."""
    if "semanticscholar.org/paper/" in source_url:
        pid = source_url.split("/paper/")[-1].split("/")[0].split("?")[0]
        if pid in s2_lookup:
            return s2_lookup[pid]
    if "arxiv.org/abs/" in source_url:
        arxiv_id = source_url.split("/abs/")[-1].split("?")[0]
        arxiv_id = re.sub(r"v\d+$", "", arxiv_id).lower()
        for key in [arxiv_id, f"arxiv:{arxiv_id}"]:
            if key in s2_lookup:
                return s2_lookup[key]
    # HuggingFace paper URLs contain arXiv IDs (e.g. /papers/2402.08070)
    if "huggingface.co/papers/" in source_url:
        hf_id = source_url.split("/papers/")[-1].split("?")[0]
        for key in [hf_id.lower(), f"arxiv:{hf_id.lower()}"]:
            if key in s2_lookup:
                return s2_lookup[key]
    return None


def load_s2_details() -> dict[str, dict]:
    """Load S2 paper details and build a lookup dict. Returns empty dict if unavailable."""
    if not os.path.exists(S2_DETAILS_JSON):
        return {}
    with open(S2_DETAILS_JSON, "r", encoding="utf-8") as f:
        details = json.load(f)
    if not isinstance(details, list):
        return {}
    lookup = _build_s2_lookup(details)
    print(f"Loaded {len(details)} S2 paper details ({len(lookup)} lookup keys)")
    return lookup


def load_paper_scores() -> dict[str, dict]:
    """Load LLM-generated paper scores and build a lookup by paper ID.

    Returns {paper_id: score_dict} where score_dict has keys:
      relevance_score, framework_ids, tool_types, summary, reasoning, status
    """
    if not os.path.exists(PAPER_SCORES_JSON):
        return {}
    try:
        with open(PAPER_SCORES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return {}
        lookup = {s["paper_id"]: s for s in data if s.get("paper_id") and s.get("status") == "scored"}
        print(f"Loaded {len(lookup)} paper scores from {PAPER_SCORES_JSON}")
        return lookup
    except (json.JSONDecodeError, OSError):
        return {}


def _find_paper_score(source_url: str, s2_lookup: dict[str, dict], scores_lookup: dict[str, dict]) -> dict | None:
    """Try to find the paper score for an entry by resolving its S2 paper ID."""
    # First find the S2 detail to get the paper ID
    s2 = _find_s2_detail(source_url, s2_lookup)
    if s2:
        pid = s2.get("paperId", "")
        if pid and pid in scores_lookup:
            return scores_lookup[pid]
    return None


def generate_benchmarks_json(
    entries: list[dict],
    s2_lookup: dict[str, dict] | None = None,
    scores_lookup: dict[str, dict] | None = None,
) -> list[dict]:
    """Generate benchmark JSON data from pipeline entries, enriched with S2 details and paper scores."""
    benchmarks = []
    s2_hits = 0
    score_hits = 0

    for entry in entries:
        name = entry["name"]
        slug = slugify(name)
        desc = entry.get("description", "")[:500]
        source_url = entry.get("source_url", "")
        source_type = entry.get("source_type", "dataset")
        framework_ids = entry.get("framework_ids", [])
        tool_types = entry.get("tool_types", [])
        tags = [t for t in entry.get("tags", []) if not t.startswith("llm:")][:8]

        # Extract year from date field (e.g. "2024-03-15" -> 2024)
        date_str = entry.get("date", "")
        year = None
        if date_str and len(date_str) >= 4:
            try:
                year = int(date_str[:4])
            except ValueError:
                pass

        benchmark: dict = {
            "name": name,
            "slug": slug,
            "sourceUrl": source_url,
            "sourceType": source_type,
            "description": desc,
            "frameworkIds": framework_ids,
            "toolTypes": tool_types,
            "tags": tags,
        }
        if year:
            benchmark["year"] = year

        # Enrich with S2 paper details (tldr, citationCount, pdfUrl)
        if s2_lookup:
            s2 = _find_s2_detail(source_url, s2_lookup)
            if s2:
                s2_hits += 1
                # TLDR — one-line AI summary
                tldr_data = s2.get("tldr")
                if isinstance(tldr_data, dict):
                    tldr = tldr_data.get("text", "")
                elif isinstance(tldr_data, str):
                    tldr = tldr_data
                else:
                    tldr = ""
                if tldr:
                    benchmark["tldr"] = tldr

                # Citation count
                citation_count = s2.get("citationCount")
                if citation_count and isinstance(citation_count, int):
                    benchmark["citationCount"] = citation_count

                # Open access PDF URL
                pdf_data = s2.get("openAccessPdf")
                if isinstance(pdf_data, dict):
                    pdf_url = pdf_data.get("url", "")
                    if pdf_url:
                        benchmark["pdfUrl"] = pdf_url

        # Enrich with LLM paper scores (relevance, reclassification, summary)
        if scores_lookup and s2_lookup:
            score = _find_paper_score(source_url, s2_lookup, scores_lookup)
            if score:
                score_hits += 1

                # Relevance score (1-10)
                rel = score.get("relevance_score")
                if rel and isinstance(rel, int) and 1 <= rel <= 10:
                    benchmark["relevanceScore"] = rel

                # LLM-generated summary (prefer over S2 TLDR when available)
                summary = score.get("summary", "")
                if summary:
                    benchmark["tldr"] = summary

                # Reclassified framework IDs and tool types (replace pipeline values)
                llm_fw = score.get("framework_ids", [])
                if llm_fw:
                    benchmark["frameworkIds"] = llm_fw

                llm_tools = score.get("tool_types", [])
                if llm_tools:
                    benchmark["toolTypes"] = llm_tools

        benchmarks.append(benchmark)

    if s2_lookup:
        print(f"  S2 enrichment: {s2_hits}/{len(entries)} entries matched")
    if scores_lookup:
        print(f"  Score enrichment: {score_hits}/{len(entries)} entries matched")

    return benchmarks


def cmd_sync():
    """Sync pipeline output -> website static/benchmarks.json."""
    entries = load_pipeline_entries()

    # Only include entries with at least one framework mapping
    mapped = [e for e in entries if e.get("framework_ids")]
    print(f"  {len(mapped)} entries have framework mappings (keeping these)")

    # Exclude entries flagged as not-a-benchmark
    benchmarks = [e for e in mapped if "not-a-benchmark" not in e.get("tags", [])]
    print(f"  {len(benchmarks)} after removing not-a-benchmark entries")

    # Apply any previously archived dismissals
    archived = load_archived_dismissed()
    if archived:
        before = len(benchmarks)
        benchmarks = [e for e in benchmarks if slugify(e["name"]) not in archived]
        print(f"  {before - len(benchmarks)} removed by archived dismissals")

    # Load S2 paper details for enrichment (tldr, citations, PDF links)
    s2_lookup = load_s2_details()

    # Load LLM paper scores for enrichment (relevance, reclassification, summary)
    scores_lookup = load_paper_scores()

    # Write static JSON (loaded asynchronously by the website)
    json_data = generate_benchmarks_json(benchmarks, s2_lookup=s2_lookup, scores_lookup=scores_lookup)
    os.makedirs(os.path.dirname(WEBSITE_BENCHMARKS_JSON), exist_ok=True)
    with open(WEBSITE_BENCHMARKS_JSON, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False)

    print(f"\nDone: Written {len(benchmarks)} benchmarks -> {WEBSITE_BENCHMARKS_JSON}")

    # Sync research reports to website
    sync_research_reports()


def sync_research_reports():
    """Copy research report markdown files to the website static folder and generate manifests."""
    import shutil

    src_dir = Path(RESEARCH_REPORTS_DIR)
    dst_dir = Path(WEBSITE_RESEARCH_DIR)
    dst_dir.mkdir(parents=True, exist_ok=True)

    # ── Framework category reports: category_{id}_report.md -> {id}.md ──
    cat_files = sorted(src_dir.glob("category_*_report.md"))
    cat_ids: list[str] = []
    for report_path in cat_files:
        stem = report_path.stem  # category_6.2_report
        cat_id = stem.replace("category_", "").replace("_report", "")
        shutil.copy2(report_path, dst_dir / f"{cat_id}.md")
        cat_ids.append(cat_id)

    manifest_path = dst_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(cat_ids, f)

    print(f"\n  Synced {len(cat_ids)} category reports -> {WEBSITE_RESEARCH_DIR}/")
    if cat_ids:
        print(f"  Categories: {', '.join(cat_ids)}")

    # ── Tool-type reports: tool_type_{key}_report.md -> tool-type/{key}.md ──
    tt_dst = dst_dir / "tool-type"
    tt_dst.mkdir(parents=True, exist_ok=True)

    tt_files = sorted(src_dir.glob("tool_type_*_report.md"))
    tt_keys: list[str] = []
    for report_path in tt_files:
        stem = report_path.stem  # tool_type_ai_tutor_report
        tt_key = stem.replace("tool_type_", "").replace("_report", "")
        shutil.copy2(report_path, tt_dst / f"{tt_key}.md")
        tt_keys.append(tt_key)

    tt_manifest = tt_dst / "manifest.json"
    with open(tt_manifest, "w", encoding="utf-8") as f:
        json.dump(tt_keys, f)

    print(f"  Synced {len(tt_keys)} tool-type reports -> {WEBSITE_RESEARCH_DIR}/tool-type/")
    if tt_keys:
        print(f"  Tool types: {', '.join(tt_keys)}")


def cmd_apply(dismissed_json_path: str):
    """Apply dismissed list: archive dismissals, then re-sync."""
    new_dismissed = load_dismissed(dismissed_json_path)
    print(f"Loaded {len(new_dismissed)} dismissed slugs from {dismissed_json_path}")

    # Merge with existing archived dismissals
    archived = load_archived_dismissed()
    merged = archived | new_dismissed
    added = len(merged) - len(archived)
    print(f"  {added} new dismissals (total archived: {len(merged)})")

    save_archived_dismissed(merged)

    # Re-sync with the updated dismissals
    print()
    cmd_sync()


def cmd_stats():
    """Show current benchmark counts."""
    if os.path.exists(PIPELINE_JSON):
        with open(PIPELINE_JSON, "r", encoding="utf-8") as f:
            entries = json.load(f)
        mapped = [e for e in entries if e.get("framework_ids")]
        benchmarks = [e for e in mapped if "not-a-benchmark" not in e.get("tags", [])]
        print(f"Pipeline output:     {len(entries)} total entries")
        print(f"  With mappings:     {len(mapped)}")
        print(f"  Actual benchmarks: {len(benchmarks)}")
    else:
        print(f"Pipeline output not found ({PIPELINE_JSON})")

    archived = load_archived_dismissed()
    print(f"  Archived dismissed: {len(archived)}")

    if os.path.exists(WEBSITE_BENCHMARKS_JSON):
        with open(WEBSITE_BENCHMARKS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"  Website benchmarks: {len(data)}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "sync":
        cmd_sync()
    elif cmd == "apply":
        if len(sys.argv) < 3:
            print("Usage: uv run curate.py apply <dismissed-benchmarks.json>")
            sys.exit(1)
        cmd_apply(sys.argv[2])
    elif cmd == "stats":
        cmd_stats()
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: sync, apply, stats")
        sys.exit(1)


if __name__ == "__main__":
    main()
