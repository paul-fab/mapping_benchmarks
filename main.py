"""
Education Benchmark Mapper -- CLI entry point.

Usage:
    uv run main.py                  # Full pipeline: S2 + HF search → LLM classification → reports
    uv run main.py --known-only     # Only use curated known benchmarks (no API search)
    uv run main.py --skip-search    # Skip search, reload previous scraped results from cache
    uv run main.py --search-only    # Only use API results; skip curated benchmarks
    uv run main.py --no-s2          # Skip Semantic Scholar; only use HuggingFace
    uv run main.py --no-details     # Skip fetching full paper details after search
    uv run main.py --no-llm         # Skip LLM classification; heuristic keywords only
    uv run main.py --model claude-sonnet-4-20250514  # Use a different Anthropic model
    uv run main.py --query "math"   # Add a custom query to the search list
"""

import argparse
import json
import os
import sys

from dotenv import load_dotenv
load_dotenv()  # Load .env file (e.g. S2_API_KEY, ANTHROPIC_API_KEY)

from config import HF_SEARCH_QUERIES
from scraper import BenchmarkEntry, run_search
from known_benchmarks import KNOWN_BENCHMARKS
from mapper import map_all
from report import write_reports, generate_markdown


def merge_entries(
    scraped: list[BenchmarkEntry],
    known: list[BenchmarkEntry],
) -> list[BenchmarkEntry]:
    """Merge scraped and known entries, preferring known entries on URL collision."""
    seen_urls = set()
    merged = []

    # Known benchmarks take priority (they have hand-curated mappings)
    for entry in known:
        seen_urls.add(entry.source_url)
        merged.append(entry)

    # Add scraped entries that aren't already known
    for entry in scraped:
        if entry.source_url not in seen_urls:
            seen_urls.add(entry.source_url)
            merged.append(entry)

    return merged


def cli():
    parser = argparse.ArgumentParser(
        description="Search Semantic Scholar + HuggingFace for education benchmarks and map them to a framework.",
    )
    parser.add_argument(
        "--known-only",
        action="store_true",
        help="Skip API search; only use the curated known benchmarks.",
    )
    parser.add_argument(
        "--skip-search",
        action="store_true",
        help="Skip search; reload previously cached scraped results from output/scraped_cache.json.",
    )
    parser.add_argument(
        "--search-only",
        action="store_true",
        help="Only use API results; don't include curated known benchmarks.",
    )
    parser.add_argument(
        "--query", "-q",
        action="append",
        default=[],
        help="Add custom search queries (can be repeated).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between HTTP requests in seconds (default: 1.0).",
    )
    parser.add_argument(
        "--no-daily-papers",
        action="store_true",
        help="Skip fetching the HuggingFace daily papers.",
    )
    parser.add_argument(
        "--no-s2",
        action="store_true",
        help="Skip Semantic Scholar; only use HuggingFace for papers.",
    )
    parser.add_argument(
        "--no-details",
        action="store_true",
        help="Skip fetching full Semantic Scholar paper details after search.",
    )
    parser.add_argument(
        "--max-datasets",
        type=int,
        default=200,
        help="Max dataset results per query via HF API (default: 200).",
    )
    parser.add_argument(
        "--max-papers",
        type=int,
        default=1000,
        help="Max paper results per S2 bulk query (default: 1000).",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip LLM classification; use heuristic keyword mapping only.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-haiku-4-5-20251001",
        help="Anthropic model for LLM classification (default: claude-haiku-4-5-20251001).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Entries per LLM batch (default: 20).",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="Parallel LLM workers (default: 5).",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_report",
        help="Also print the Markdown report to stdout.",
    )
    args = parser.parse_args()

    # ── Collect entries ──────────────────────────────────────────────────
    scraped: list[BenchmarkEntry] = []
    known: list[BenchmarkEntry] = []
    scraped_cache_path = os.path.join("output", "scraped_cache.json")

    if args.skip_search:
        # Reload from cached scraped results
        if os.path.exists(scraped_cache_path):
            with open(scraped_cache_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            scraped = [BenchmarkEntry(**r) for r in raw]
            print(f"Loaded {len(scraped)} cached scraped entries from {scraped_cache_path}")
        else:
            print(f"ERROR: No cached scraped results found at {scraped_cache_path}")
            print("Run without --skip-search first to populate the cache.")
            sys.exit(1)
    elif not args.known_only:
        queries = HF_SEARCH_QUERIES + args.query
        use_s2 = not args.no_s2
        sources = []
        if use_s2:
            sources.append("Semantic Scholar (bulk)")
        sources.append("HuggingFace")
        print(f"Starting search with {len(queries)} queries across {', '.join(sources)} ...")
        if use_s2 and not args.no_details:
            print("Full paper details will be fetched after search.\n")
        else:
            print()

        scraped = run_search(
            queries,
            include_daily_papers=not args.no_daily_papers,
            include_semantic_scholar=use_s2,
            delay=args.delay,
            max_datasets_per_query=args.max_datasets,
            max_papers_per_query=args.max_papers,
            fetch_details=use_s2 and not args.no_details,
        )

        # Save scraped results to cache for --skip-search later
        os.makedirs("output", exist_ok=True)
        with open(scraped_cache_path, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in scraped], f, indent=2)
        print(f"Saved {len(scraped)} scraped entries to {scraped_cache_path}")

    if not args.search_only:
        known = list(KNOWN_BENCHMARKS)
        print(f"\nLoaded {len(known)} curated known benchmarks.")

    # ── Merge & map ──────────────────────────────────────────────────────
    if args.search_only:
        entries = scraped
    elif args.known_only:
        entries = known
    else:
        entries = merge_entries(scraped, known)

    print(f"\nTotal entries: {len(entries)}")

    # Load S2 paper details (for LLM context enrichment)
    s2_details = None
    details_path = "output/s2_paper_details.json"
    if os.path.exists(details_path):
        with open(details_path, "r", encoding="utf-8") as f:
            s2_details = json.load(f)
        print(f"Loaded {len(s2_details)} S2 paper details from {details_path}")

    print("Mapping to framework categories and tool types ...")
    entries = map_all(
        entries,
        s2_details=s2_details,
        use_llm=not args.no_llm,
        model=args.model,
        batch_size=args.batch_size,
        max_workers=args.max_workers,
    )

    # ── Report ───────────────────────────────────────────────────────────
    print("\nGenerating reports ...")
    md_path, csv_path, json_path = write_reports(entries)

    if args.print_report:
        print("\n" + "=" * 80)
        print(generate_markdown(entries))

    print(f"\nDone! Reports saved to:")
    print(f"  {md_path}")
    print(f"  {csv_path}")
    print(f"  {json_path}")

    return entries


if __name__ == "__main__":
    cli()
