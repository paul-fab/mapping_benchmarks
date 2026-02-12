"""
Parse downloaded PDFs into structured text (JSON + Markdown).

Extracts full text from each PDF using PyMuPDF, producing:
  - output/papers_parsed/  -- one .json file per paper (metadata + text)
  - output/papers_md/      -- one .md file per paper (readable markdown)
  - output/all_papers.jsonl -- single JSONL file with every paper (for LLM pipelines)

Features:
  - Parallel parsing with configurable workers
  - Progress bar with ETA (rich)
  - Resume support: skips already-parsed files
  - Incremental JSONL writing (append mode)

Usage:
    uv run parse_papers.py                   # Parse all (default 8 workers)
    uv run parse_papers.py --workers 4       # Fewer workers
    uv run parse_papers.py --limit 100       # Parse only first 100
    uv run parse_papers.py --format json     # Only JSON output
    uv run parse_papers.py --format md       # Only Markdown output
    uv run parse_papers.py --format both     # Both (default)
"""

import argparse
import json
import os
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

import pymupdf  # PyMuPDF

from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
    SpinnerColumn,
)

# ── Config ────────────────────────────────────────────────────────────────────

PAPERS_DIR = Path("output/papers")
PARSED_JSON_DIR = Path("output/papers_parsed")
PARSED_MD_DIR = Path("output/papers_md")
JSONL_PATH = Path("output/all_papers.jsonl")
MANIFEST_PATH = Path("output/papers_manifest.json")

console = Console()


# ── Text cleaning ─────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Clean extracted PDF text: fix encoding artifacts, normalise whitespace."""
    # Fix common ligatures / encoding issues
    text = text.replace("\ufb01", "fi")
    text = text.replace("\ufb02", "fl")
    text = text.replace("\ufb00", "ff")
    text = text.replace("\ufb03", "ffi")
    text = text.replace("\ufb04", "ffl")
    text = text.replace("\u2019", "'")
    text = text.replace("\u2018", "'")
    text = text.replace("\u201c", '"')
    text = text.replace("\u201d", '"')
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "--")

    # Remove null bytes
    text = text.replace("\x00", "")

    # Collapse excessive whitespace (but preserve paragraph breaks)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove lines that are just page numbers
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

    return text.strip()


# ── Single PDF parser (runs in worker process) ───────────────────────────────

def parse_single_pdf(pdf_path: str) -> dict:
    """
    Extract text and metadata from a single PDF.

    Returns a dict with: filename, title, page_count, text, char_count, error.
    This function is designed to run in a separate process.
    """
    result = {
        "filename": os.path.basename(pdf_path),
        "title": "",
        "page_count": 0,
        "text": "",
        "char_count": 0,
        "error": "",
    }

    try:
        doc = pymupdf.open(pdf_path)
        result["page_count"] = len(doc)

        # Extract metadata title
        meta = doc.metadata
        if meta and meta.get("title"):
            result["title"] = meta["title"].strip()

        # Extract text from all pages
        pages_text: list[str] = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if text:
                pages_text.append(text)

        doc.close()

        full_text = "\n\n".join(pages_text)
        full_text = clean_text(full_text)

        result["text"] = full_text
        result["char_count"] = len(full_text)

    except Exception as e:
        result["error"] = str(e)[:500]

    return result


# ── Manifest helpers ──────────────────────────────────────────────────────────

def load_manifest() -> dict[str, dict]:
    """Load the download manifest to get paper metadata."""
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {item["filename"]: item for item in data if item.get("status") == "downloaded"}
        except (json.JSONDecodeError, KeyError, OSError):
            pass
    return {}


# ── Output writers ────────────────────────────────────────────────────────────

def write_json(parsed: dict, manifest_entry: dict):
    """Write a single parsed paper as a JSON file."""
    out = {
        "paper_id": manifest_entry.get("paper_id", ""),
        "title": parsed["title"] or manifest_entry.get("title", ""),
        "pdf_url": manifest_entry.get("pdf_url", ""),
        "source": manifest_entry.get("source", ""),
        "filename": parsed["filename"],
        "page_count": parsed["page_count"],
        "char_count": parsed["char_count"],
        "text": parsed["text"],
    }

    json_name = Path(parsed["filename"]).stem + ".json"
    json_path = PARSED_JSON_DIR / json_name
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)


def write_md(parsed: dict, manifest_entry: dict):
    """Write a single parsed paper as a Markdown file."""
    title = parsed["title"] or manifest_entry.get("title", parsed["filename"])
    pdf_url = manifest_entry.get("pdf_url", "")

    md_parts = [
        f"# {title}",
        "",
        f"- **Source**: [{pdf_url}]({pdf_url})" if pdf_url else "",
        f"- **Pages**: {parsed['page_count']}",
        f"- **Characters**: {parsed['char_count']:,}",
        "",
        "---",
        "",
        parsed["text"],
    ]

    md_name = Path(parsed["filename"]).stem + ".md"
    md_path = PARSED_MD_DIR / md_name
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_parts))


def append_jsonl(parsed: dict, manifest_entry: dict):
    """Append a single parsed paper to the JSONL file."""
    record = {
        "paper_id": manifest_entry.get("paper_id", ""),
        "title": parsed["title"] or manifest_entry.get("title", ""),
        "pdf_url": manifest_entry.get("pdf_url", ""),
        "filename": parsed["filename"],
        "page_count": parsed["page_count"],
        "char_count": parsed["char_count"],
        "text": parsed["text"],
    }

    with open(JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_parser(
    max_workers: int = 8,
    limit: Optional[int] = None,
    output_format: str = "both",  # "json" | "md" | "both"
):
    """Parse all downloaded PDFs in parallel."""
    manifest = load_manifest()

    if not manifest:
        console.print("[red]No downloaded papers found in manifest.[/red]")
        return

    # Create output directories
    write_json_flag = output_format in ("json", "both")
    write_md_flag = output_format in ("md", "both")

    if write_json_flag:
        PARSED_JSON_DIR.mkdir(parents=True, exist_ok=True)
    if write_md_flag:
        PARSED_MD_DIR.mkdir(parents=True, exist_ok=True)

    # Determine which PDFs still need parsing
    pdf_files: list[tuple[str, dict]] = []  # (pdf_path, manifest_entry)
    already_done = 0

    for filename, entry in manifest.items():
        pdf_path = PAPERS_DIR / filename
        if not pdf_path.exists():
            continue

        # Check if already parsed
        stem = Path(filename).stem
        json_exists = (PARSED_JSON_DIR / f"{stem}.json").exists() if write_json_flag else False
        md_exists = (PARSED_MD_DIR / f"{stem}.md").exists() if write_md_flag else False

        if write_json_flag and write_md_flag and json_exists and md_exists:
            already_done += 1
            continue
        elif write_json_flag and not write_md_flag and json_exists:
            already_done += 1
            continue
        elif write_md_flag and not write_json_flag and md_exists:
            already_done += 1
            continue

        pdf_files.append((str(pdf_path), entry))

    if limit:
        pdf_files = pdf_files[:limit]

    console.print(f"\n[bold]Parse plan:[/bold]")
    console.print(f"  PDFs in manifest:   [cyan]{len(manifest)}[/cyan]")
    console.print(f"  Already parsed:     [green]{already_done}[/green]")
    console.print(f"  To parse:           [yellow]{len(pdf_files)}[/yellow]")
    console.print(f"  Workers:            [yellow]{max_workers}[/yellow]")
    console.print(f"  Output format:      [cyan]{output_format}[/cyan]")
    if write_json_flag:
        console.print(f"  JSON dir:           [dim]{PARSED_JSON_DIR}[/dim]")
    if write_md_flag:
        console.print(f"  Markdown dir:       [dim]{PARSED_MD_DIR}[/dim]")
    console.print(f"  JSONL file:         [dim]{JSONL_PATH}[/dim]\n")

    if not pdf_files:
        console.print("[green]All papers already parsed![/green]")
        return

    # Clear JSONL if starting fresh (not resuming)
    if already_done == 0 and JSONL_PATH.exists():
        JSONL_PATH.unlink()

    parsed_count = 0
    failed_count = 0
    total_chars = 0
    total_pages = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        MofNCompleteColumn(),
        TextColumn("*"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Parsing PDFs", total=len(pdf_files))

        # Use ProcessPoolExecutor for CPU-bound PDF parsing
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_entry = {}
            for pdf_path, entry in pdf_files:
                future = executor.submit(parse_single_pdf, pdf_path)
                future_to_entry[future] = entry

            for future in as_completed(future_to_entry):
                entry = future_to_entry[future]

                try:
                    parsed = future.result()
                except Exception as e:
                    parsed = {
                        "filename": entry.get("filename", ""),
                        "title": "",
                        "page_count": 0,
                        "text": "",
                        "char_count": 0,
                        "error": str(e)[:500],
                    }

                if parsed["error"]:
                    failed_count += 1
                elif parsed["char_count"] < 10:
                    # Almost empty — likely a scanned image PDF
                    failed_count += 1
                    parsed["error"] = "No text extracted (likely scanned/image PDF)"
                else:
                    parsed_count += 1
                    total_chars += parsed["char_count"]
                    total_pages += parsed["page_count"]

                    # Write outputs
                    if write_json_flag:
                        write_json(parsed, entry)
                    if write_md_flag:
                        write_md(parsed, entry)

                    # Always append to JSONL
                    append_jsonl(parsed, entry)

                progress.update(task, advance=1)

    # Summary
    console.print(f"\n[bold]Parsing complete![/bold]")
    console.print(f"  Parsed:      [green]{parsed_count}[/green]")
    console.print(f"  Failed:      [red]{failed_count}[/red]")
    console.print(f"  Total pages: [cyan]{total_pages:,}[/cyan]")
    console.print(f"  Total chars: [cyan]{total_chars:,}[/cyan] ({total_chars / 1_000_000:.1f}M)")
    console.print(f"  JSONL:       [dim]{JSONL_PATH}[/dim]")

    if write_json_flag:
        json_count = len(list(PARSED_JSON_DIR.glob("*.json")))
        console.print(f"  JSON files:  [dim]{json_count} in {PARSED_JSON_DIR}[/dim]")
    if write_md_flag:
        md_count = len(list(PARSED_MD_DIR.glob("*.md")))
        console.print(f"  MD files:    [dim]{md_count} in {PARSED_MD_DIR}[/dim]")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Parse downloaded PDFs into structured text (JSON + Markdown)."
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=8,
        help="Number of parallel parser workers (default: 8).",
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Only parse the first N pending PDFs.",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "md", "both"],
        default="both",
        help="Output format: json, md, or both (default: both).",
    )
    args = parser.parse_args()

    run_parser(
        max_workers=args.workers,
        limit=args.limit,
        output_format=args.format,
    )


if __name__ == "__main__":
    main()
