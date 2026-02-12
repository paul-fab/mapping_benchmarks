"""
Download full-text PDFs for all papers in the education benchmark mapping.

Features:
  - Parallel downloads (configurable concurrency)
  - Progress bar with ETA (via rich)
  - Resume support: skips already-downloaded files
  - Incremental manifest (papers_manifest.json) tracks status of every paper
  - Graceful error handling with retries

Usage:
    uv run download_papers.py                    # Download all (default 20 workers)
    uv run download_papers.py --workers 10       # Fewer concurrent downloads
    uv run download_papers.py --limit 100        # Download only first 100
    uv run download_papers.py --dry-run          # Show what would be downloaded
"""

import argparse
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
    SpinnerColumn,
    TransferSpeedColumn,
)

# ── Config ────────────────────────────────────────────────────────────────────

PAPERS_DIR = Path("output/papers")
MANIFEST_PATH = Path("output/papers_manifest.json")
S2_DETAILS_PATH = Path("output/s2_paper_details.json")
MAPPING_PATH = Path("output/education_benchmark_mapping.json")

MAX_RETRIES = 3
TIMEOUT = 60  # seconds per request
USER_AGENT = "edu-benchmark-mapper/0.1 (research tool; bulk PDF download)"

console = Console()


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class PaperDownload:
    """Tracks a single paper's download state."""
    paper_id: str
    title: str
    pdf_url: str
    source: str  # "openAccessPdf" | "arxiv"
    filename: str
    status: str = "pending"  # "pending" | "downloaded" | "failed" | "skipped"
    error: str = ""
    size_bytes: int = 0


# ── Helpers ───────────────────────────────────────────────────────────────────

def sanitise_filename(title: str, max_len: int = 120) -> str:
    """Create a filesystem-safe filename from a paper title."""
    # Remove/replace problematic characters
    clean = re.sub(r'[<>:"/\\|?*]', '', title)
    clean = re.sub(r'\s+', '_', clean.strip())
    clean = clean[:max_len]
    # Remove trailing dots/underscores
    clean = clean.rstrip('._')
    return clean or "untitled"


def build_download_list() -> list[PaperDownload]:
    """
    Cross-reference the mapping with S2 paper details to build a list of
    papers with downloadable PDF URLs.
    """
    console.print("[bold]Loading data...[/bold]")

    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        benchmarks = json.load(f)

    with open(S2_DETAILS_PATH, "r", encoding="utf-8") as f:
        s2_details = json.load(f)

    # Build lookups
    by_pid: dict[str, dict] = {}
    by_arxiv: dict[str, dict] = {}
    for p in s2_details:
        pid = p.get("paperId", "")
        if pid:
            by_pid[pid] = p
        arxiv = (p.get("externalIds") or {}).get("ArXiv", "")
        if arxiv:
            by_arxiv[arxiv] = p

    papers = [b for b in benchmarks if b.get("source_type") == "paper"]
    downloads: list[PaperDownload] = []
    seen_ids: set[str] = set()

    for paper in papers:
        url = paper.get("source_url", "")
        detail = None

        # Match to S2 detail record
        if "semanticscholar.org/paper/" in url:
            pid = url.split("/paper/")[-1].split("/")[0].split("?")[0]
            detail = by_pid.get(pid)
        elif "arxiv.org/abs/" in url:
            aid = url.split("/abs/")[-1].split("?")[0]
            detail = by_arxiv.get(aid)

        if not detail:
            continue

        paper_id = detail.get("paperId", "")
        if not paper_id or paper_id in seen_ids:
            continue
        seen_ids.add(paper_id)

        title = detail.get("title", "") or paper.get("name", "")

        # Determine PDF URL
        pdf_url = ""
        source = ""
        oa = detail.get("openAccessPdf")
        if oa and oa.get("url"):
            pdf_url = oa["url"]
            source = "openAccessPdf"
        else:
            arxiv_id = (detail.get("externalIds") or {}).get("ArXiv", "")
            if arxiv_id:
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
                source = "arxiv"

        if not pdf_url:
            continue

        filename = f"{sanitise_filename(title)}_{paper_id[:8]}.pdf"

        downloads.append(PaperDownload(
            paper_id=paper_id,
            title=title,
            pdf_url=pdf_url,
            source=source,
            filename=filename,
        ))

    console.print(f"  Papers in mapping: [cyan]{len(papers)}[/cyan]")
    console.print(f"  Downloadable PDFs: [green]{len(downloads)}[/green]")

    return downloads


# ── Manifest (tracks state across runs) ───────────────────────────────────────

def load_manifest() -> dict[str, dict]:
    """Load the download manifest from disk, or return empty dict."""
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {item["paper_id"]: item for item in data}
        except (json.JSONDecodeError, KeyError, OSError):
            pass
    return {}


def save_manifest(manifest: dict[str, dict]):
    """Save the download manifest to disk."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    items = list(manifest.values())
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


# ── Download logic ────────────────────────────────────────────────────────────

def download_one(paper: PaperDownload, client: httpx.Client) -> PaperDownload:
    """Download a single PDF. Returns the updated PaperDownload."""
    dest = PAPERS_DIR / paper.filename

    # Already downloaded?
    if dest.exists() and dest.stat().st_size > 1000:
        paper.status = "downloaded"
        paper.size_bytes = dest.stat().st_size
        return paper

    for attempt in range(MAX_RETRIES):
        try:
            r = client.get(
                paper.pdf_url,
                follow_redirects=True,
                timeout=TIMEOUT,
                headers={"User-Agent": USER_AGENT},
            )

            if r.status_code == 200:
                content_type = r.headers.get("content-type", "")
                # Verify we got a PDF, not an HTML error page
                if "pdf" in content_type or r.content[:5] == b"%PDF-":
                    dest.write_bytes(r.content)
                    paper.status = "downloaded"
                    paper.size_bytes = len(r.content)
                    return paper
                else:
                    paper.error = f"Not a PDF (content-type: {content_type})"
                    paper.status = "failed"
                    return paper

            if r.status_code == 429:
                wait = min(2 ** (attempt + 1), 30)
                time.sleep(wait)
                continue

            if r.status_code in (403, 451):
                paper.error = f"Access denied (HTTP {r.status_code})"
                paper.status = "failed"
                return paper

            paper.error = f"HTTP {r.status_code}"

        except httpx.TimeoutException:
            paper.error = "Timeout"
            time.sleep(2)
        except httpx.HTTPError as e:
            paper.error = str(e)[:200]
            time.sleep(1)

    paper.status = "failed"
    return paper


def run_downloads(
    downloads: list[PaperDownload],
    max_workers: int = 20,
    limit: Optional[int] = None,
    dry_run: bool = False,
):
    """Download PDFs in parallel with progress tracking and manifest saving."""
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()

    # Filter out already-downloaded papers
    pending: list[PaperDownload] = []
    already_done = 0
    for paper in downloads:
        existing = manifest.get(paper.paper_id)
        dest = PAPERS_DIR / paper.filename
        if existing and existing.get("status") == "downloaded" and dest.exists():
            already_done += 1
        else:
            pending.append(paper)

    if limit:
        pending = pending[:limit]

    console.print(f"\n[bold]Download plan:[/bold]")
    console.print(f"  Already downloaded: [green]{already_done}[/green]")
    console.print(f"  To download:        [cyan]{len(pending)}[/cyan]")
    console.print(f"  Workers:            [yellow]{max_workers}[/yellow]")
    console.print(f"  Output dir:         [dim]{PAPERS_DIR}[/dim]\n")

    if dry_run:
        console.print("[yellow]Dry run — no files will be downloaded.[/yellow]")
        for p in pending[:20]:
            console.print(f"  [dim]{p.filename}[/dim] <- {p.pdf_url}")
        if len(pending) > 20:
            console.print(f"  ... and {len(pending) - 20} more")
        return

    if not pending:
        console.print("[green]All papers already downloaded![/green]")
        return

    downloaded = 0
    failed = 0
    total_bytes = 0
    save_every = 50  # Save manifest every N completions

    with httpx.Client() as client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            MofNCompleteColumn(),
            TextColumn("•"),
            TransferSpeedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Downloading papers", total=len(pending))

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(download_one, paper, client): paper
                    for paper in pending
                }

                for future in as_completed(futures):
                    result = future.result()
                    completed_count = downloaded + failed + 1

                    # Update manifest
                    manifest[result.paper_id] = {
                        "paper_id": result.paper_id,
                        "title": result.title,
                        "pdf_url": result.pdf_url,
                        "source": result.source,
                        "filename": result.filename,
                        "status": result.status,
                        "error": result.error,
                        "size_bytes": result.size_bytes,
                    }

                    if result.status == "downloaded":
                        downloaded += 1
                        total_bytes += result.size_bytes
                    else:
                        failed += 1

                    progress.update(task, advance=1, completed=completed_count)

                    # Incremental manifest save
                    if completed_count % save_every == 0:
                        save_manifest(manifest)

    # Final manifest save
    save_manifest(manifest)

    # Summary
    console.print(f"\n[bold]Download complete![/bold]")
    console.print(f"  Downloaded: [green]{downloaded}[/green]")
    console.print(f"  Failed:     [red]{failed}[/red]")
    console.print(f"  Total size: [cyan]{total_bytes / (1024**3):.2f} GB[/cyan]")
    console.print(f"  Manifest:   [dim]{MANIFEST_PATH}[/dim]")

    if failed > 0:
        console.print(f"\n[yellow]Run again to retry failed downloads.[/yellow]")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Download full-text PDFs for mapped education benchmark papers."
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=20,
        help="Number of parallel download workers (default: 20).",
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Only download the first N pending papers.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without actually downloading.",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry papers that previously failed.",
    )
    args = parser.parse_args()

    # Build the download list
    downloads = build_download_list()

    if not downloads:
        console.print("[red]No downloadable papers found.[/red]")
        return

    # If retrying, clear failed status in manifest so they're re-attempted
    if args.retry_failed:
        manifest = load_manifest()
        cleared = 0
        for pid, entry in manifest.items():
            if entry.get("status") == "failed":
                entry["status"] = "pending"
                cleared += 1
        if cleared:
            save_manifest(manifest)
            console.print(f"[yellow]Cleared {cleared} failed entries for retry.[/yellow]")

    run_downloads(
        downloads,
        max_workers=args.workers,
        limit=args.limit,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
