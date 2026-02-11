"""
Education Benchmark Mapper -- CLI entry point.

Usage:
    uv run main.py                  # Full search (S2 + HF) + known benchmarks + report
    uv run main.py --known-only     # Only use curated known benchmarks (no API search)
    uv run main.py --search-only    # Only use API results; skip curated benchmarks
    uv run main.py --no-s2          # Skip Semantic Scholar; only use HuggingFace
    uv run main.py --query "math"   # Add a custom query to the search list
"""

import argparse
import sys

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
        help="Skip HuggingFace scraping; only use the curated known benchmarks.",
    )
    parser.add_argument(
        "--search-only",
        action="store_true",
        help="Only use scraped results; don't include curated known benchmarks.",
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
        "--max-datasets",
        type=int,
        default=200,
        help="Max dataset results per query via HF API (default: 200).",
    )
    parser.add_argument(
        "--max-papers",
        type=int,
        default=200,
        help="Max paper results per query via Semantic Scholar (default: 200).",
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

    if not args.known_only:
        queries = HF_SEARCH_QUERIES + args.query
        use_s2 = not args.no_s2
        sources = []
        if use_s2:
            sources.append("Semantic Scholar")
        sources.append("HuggingFace")
        print(f"Starting search with {len(queries)} queries across {', '.join(sources)} ...\n")
        scraped = run_search(
            queries,
            include_daily_papers=not args.no_daily_papers,
            include_semantic_scholar=use_s2,
            delay=args.delay,
            max_datasets_per_query=args.max_datasets,
            max_papers_per_query=args.max_papers,
        )

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
    print("Mapping to framework categories and tool types ...")
    entries = map_all(entries)

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
