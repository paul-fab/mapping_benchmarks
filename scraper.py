"""
Search for education-related benchmarks across multiple sources:

  1. HuggingFace REST API  (datasets + daily papers)
  2. Semantic Scholar API  (comprehensive academic paper search, 200M+ papers)
     - Bulk search  (GET /paper/search/bulk) -- up to 1000 results per request
     - Batch detail (POST /paper/batch)      -- full metadata for every hit

Both APIs return structured JSON and support pagination.
"""

import json
import os
import re
import time
import httpx
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class BenchmarkEntry:
    """A single benchmark / eval / dataset discovered from HuggingFace."""
    name: str
    source_url: str
    source_type: str  # "paper" | "dataset" | "space"
    description: str = ""
    date: str = ""
    tags: list[str] = field(default_factory=list)
    # Mapped later
    framework_ids: list[str] = field(default_factory=list)
    tool_types: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


BASE = "https://huggingface.co"
API_BASE = "https://huggingface.co/api"
HEADERS = {
    "User-Agent": "edu-benchmark-mapper/0.1 (research tool)",
    "Accept": "application/json",
}

# ── HTTP helpers ─────────────────────────────────────────────────────────────

def _api_get_json(
    url: str,
    client: httpx.Client,
    params: dict | None = None,
) -> Optional[list | dict]:
    """GET a JSON API endpoint with retry + back-off."""
    for attempt in range(3):
        try:
            r = client.get(
                url, headers=HEADERS, params=params,
                follow_redirects=True, timeout=30,
            )
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"  Rate-limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            print(f"  HTTP {r.status_code} for {url}")
            return None
        except (httpx.HTTPError, ValueError) as exc:
            print(f"  Error fetching {url}: {exc}")
            time.sleep(1)
    return None


def _get_html(url: str, client: httpx.Client, params: dict | None = None) -> Optional[str]:
    """GET an HTML page with retry (used only as paper-search fallback)."""
    html_headers = {**HEADERS, "Accept": "text/html,application/xhtml+xml"}
    for attempt in range(3):
        try:
            r = client.get(
                url, headers=html_headers, params=params,
                follow_redirects=True, timeout=30,
            )
            if r.status_code == 200:
                return r.text
            if r.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"  Rate-limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            print(f"  HTTP {r.status_code} for {url}")
            return None
        except httpx.HTTPError as exc:
            print(f"  Error fetching {url}: {exc}")
            time.sleep(1)
    return None


# ── Dataset search (REST API, paginated) ─────────────────────────────────────

def search_datasets(
    query: str,
    client: httpx.Client,
    max_results: int = 200,
    delay: float = 0.5,
) -> list[BenchmarkEntry]:
    """
    Search HuggingFace datasets via ``GET /api/datasets``.

    Paginates through results using ``limit`` / ``offset`` until either
    *max_results* are collected or no more results are returned.
    """
    PAGE_SIZE = 100  # HF API maximum
    results: list[BenchmarkEntry] = []
    offset = 0

    while offset < max_results:
        batch_limit = min(PAGE_SIZE, max_results - offset)
        data = _api_get_json(
            f"{API_BASE}/datasets",
            client,
            params={
                "search": query,
                "sort": "likes",
                "direction": "-1",
                "limit": batch_limit,
                "offset": offset,
                "full": "true",      # include cardData with descriptions
            },
        )

        if not data or not isinstance(data, list):
            break

        for ds in data:
            ds_id = ds.get("id", "")
            if not ds_id:
                continue

            # ── Extract description ──────────────────────────────────────
            description = ""
            card_data = ds.get("cardData") or {}
            if isinstance(card_data, dict):
                description = (
                    card_data.get("dataset_summary", "")
                    or card_data.get("description", "")
                )
            if not description:
                description = ds.get("description", "")

            # Strip any HTML tags that snuck in
            if description and "<" in description:
                description = re.sub(r"<[^>]+>", " ", description)
                description = re.sub(r"\s+", " ", description).strip()

            # ── Extract useful tags ──────────────────────────────────────
            tags_raw = ds.get("tags") or []
            tags_clean = [
                t.split(":")[-1]
                for t in tags_raw
                if ":" in t
                and t.split(":")[0] in (
                    "task_categories", "task_ids", "language",
                    "size_categories", "license",
                )
            ]

            last_modified = ds.get("lastModified", "")
            date_str = last_modified[:10] if last_modified else ""

            results.append(BenchmarkEntry(
                name=ds_id,
                source_url=f"{BASE}/datasets/{ds_id}",
                source_type="dataset",
                description=(description or "")[:500],
                date=date_str,
                tags=[query] + tags_clean,
            ))

        # If the API returned fewer items than we asked for → last page
        if len(data) < batch_limit:
            break

        offset += len(data)
        time.sleep(delay)  # be polite between pages

    return results


# ── Paper search (REST API + HTML fallback) ──────────────────────────────────

def fetch_daily_papers(client: httpx.Client) -> list[BenchmarkEntry]:
    """Fetch trending / daily papers from ``GET /api/daily_papers`` (JSON)."""
    data = _api_get_json(f"{API_BASE}/daily_papers", client)
    if not data or not isinstance(data, list):
        return []

    results: list[BenchmarkEntry] = []
    for item in data:
        paper = item.get("paper") or {}
        paper_id = paper.get("id", "")
        title = paper.get("title", "")
        summary = paper.get("summary", "")
        published = paper.get("publishedAt", "")
        if not paper_id or not title:
            continue

        date_str = published[:10] if published else ""
        results.append(BenchmarkEntry(
            name=title,
            source_url=f"{BASE}/papers/{paper_id}",
            source_type="paper",
            description=summary[:500],
            date=date_str,
            tags=["daily_papers"],
        ))

    return results


def search_papers(
    query: str,
    client: httpx.Client,
    max_results: int = 100,
) -> list[BenchmarkEntry]:
    """
    Search HuggingFace papers.

    Tries the JSON API at ``/api/papers/search`` first.  If that endpoint
    doesn't exist (404), falls back to paginated HTML full-text search.
    """
    # ── Attempt 1: JSON API ──────────────────────────────────────────────
    data = _api_get_json(
        f"{API_BASE}/papers/search",
        client,
        params={"q": query, "limit": min(max_results, 100)},
    )
    if data and isinstance(data, list) and len(data) > 0:
        results: list[BenchmarkEntry] = []
        for item in data:
            paper = item if "id" in item else item.get("paper", {})
            paper_id = paper.get("id", "")
            title = paper.get("title", "")
            summary = paper.get("summary", "")
            published = paper.get("publishedAt", "")
            if not paper_id or not title:
                continue
            date_str = published[:10] if published else ""
            results.append(BenchmarkEntry(
                name=title,
                source_url=f"{BASE}/papers/{paper_id}",
                source_type="paper",
                description=summary[:500],
                date=date_str,
                tags=[query],
            ))
        return results

    # ── Attempt 2: paginated HTML full-text search ───────────────────────
    return _search_papers_html(query, client, max_results)


def _search_papers_html(
    query: str,
    client: httpx.Client,
    max_results: int = 100,
) -> list[BenchmarkEntry]:
    """Fallback: scrape ``/search/full-text?type=paper`` with pagination."""
    from bs4 import BeautifulSoup

    results: list[BenchmarkEntry] = []
    page = 0

    while len(results) < max_results:
        html = _get_html(
            f"{BASE}/search/full-text",
            client,
            params={"q": query, "type": "paper", "p": page},
        )
        if not html:
            break

        soup = BeautifulSoup(html, "html.parser")
        found_any = False

        for article in soup.select("article, div.paper-card, [class*='paper']"):
            link_el = article.select_one("a[href*='/papers/']")
            if not link_el:
                continue

            href = link_el.get("href", "")
            title = link_el.get_text(strip=True)
            if not title or not href:
                continue

            found_any = True
            desc_el = article.select_one("p, .description, [class*='desc']")
            desc = desc_el.get_text(strip=True) if desc_el else ""
            date_el = article.select_one("time, [class*='date']")
            date = date_el.get_text(strip=True) if date_el else ""

            full_url = href if href.startswith("http") else f"{BASE}{href}"
            results.append(BenchmarkEntry(
                name=title,
                source_url=full_url,
                source_type="paper",
                description=desc[:500],
                date=date,
                tags=[query],
            ))

            if len(results) >= max_results:
                break

        if not found_any:
            break
        page += 1

    return results


# ── Semantic Scholar (comprehensive academic paper search) ────────────────────

S2_API_BASE = "https://api.semanticscholar.org/graph/v1"

# Fields for bulk search (lightweight -- just enough to identify papers)
S2_BULK_FIELDS = (
    "paperId,title,abstract,year,citationCount,url,"
    "externalIds,publicationDate,fieldsOfStudy,publicationTypes"
)

# Fields for full detail fetch (everything useful for analysis)
S2_DETAIL_FIELDS = (
    "paperId,title,abstract,year,citationCount,influentialCitationCount,"
    "url,externalIds,publicationDate,fieldsOfStudy,publicationTypes,"
    "venue,openAccessPdf,tldr,authors,references.paperId,references.title"
)


def _s2_api_key() -> str:
    """Return the Semantic Scholar API key from env, or empty string."""
    return os.environ.get("S2_API_KEY", "")


def _s2_headers() -> dict:
    """Build Semantic Scholar request headers (with optional API key)."""
    headers = {"Accept": "application/json"}
    api_key = _s2_api_key()
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def _s2_request(
    client: httpx.Client,
    method: str,
    url: str,
    headers: dict,
    delay: float = 1.0,
    **kwargs,
) -> Optional[dict]:
    """Make a Semantic Scholar API request with retry + back-off."""
    for attempt in range(4):
        try:
            r = client.request(method, url, headers=headers, timeout=60, **kwargs)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                wait = min(2 ** (attempt + 1), 30)
                print(f"    S2 rate-limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            print(f"    S2 HTTP {r.status_code} for {url}")
            return None
        except (httpx.HTTPError, ValueError) as exc:
            print(f"    S2 error: {exc}")
            time.sleep(delay)
    return None


def search_semantic_scholar(
    query: str,
    client: httpx.Client,
    max_results: int = 1000,
    delay: float = 1.0,
) -> list[BenchmarkEntry]:
    """
    Search Semantic Scholar using the **bulk search** endpoint.

    Uses ``GET /paper/search/bulk`` which returns up to 1,000 results per
    request and uses token-based pagination for subsequent pages.

    Returns BenchmarkEntry objects with source_type="paper".
    """
    results: list[BenchmarkEntry] = []
    s2_headers = _s2_headers()
    continuation_token: Optional[str] = None
    page = 0

    while len(results) < max_results:
        params: dict = {
            "query": query,
            "fields": S2_BULK_FIELDS,
            "sort": "citationCount:desc",
        }
        if continuation_token:
            params["token"] = continuation_token

        data = _s2_request(
            client, "GET", f"{S2_API_BASE}/paper/search/bulk",
            headers=s2_headers, delay=delay, params=params,
        )
        if not data or "data" not in data:
            break

        papers = data["data"]
        if not papers:
            break

        page += 1
        for paper in papers:
            if len(results) >= max_results:
                break
            paper_id = paper.get("paperId", "")
            title = paper.get("title", "")
            if not paper_id or not title:
                continue

            abstract = paper.get("abstract") or ""
            year = paper.get("year")
            pub_date = paper.get("publicationDate") or ""
            citation_count = paper.get("citationCount") or 0
            fields = paper.get("fieldsOfStudy") or []

            # Best URL: prefer arXiv, fall back to S2
            ext_ids = paper.get("externalIds") or {}
            arxiv_id = ext_ids.get("ArXiv", "")
            if arxiv_id:
                source_url = f"https://arxiv.org/abs/{arxiv_id}"
            else:
                source_url = paper.get("url") or f"https://www.semanticscholar.org/paper/{paper_id}"

            date_str = pub_date[:10] if pub_date else (str(year) if year else "")

            extra_tags = [f.lower().replace(" ", "-") for f in fields]
            if citation_count >= 100:
                extra_tags.append("highly-cited")

            results.append(BenchmarkEntry(
                name=title,
                source_url=source_url,
                source_type="paper",
                description=abstract[:500],
                date=date_str,
                tags=[query] + extra_tags,
            ))

        # Token-based pagination: if a token is returned, there are more pages
        continuation_token = data.get("token")
        if not continuation_token:
            break

        print(f"    page {page}: {len(results)} papers so far (total in S2: {data.get('total', '?')})")
        time.sleep(delay)

    return results


def fetch_paper_details(
    paper_ids: list[str],
    client: httpx.Client,
    delay: float = 1.0,
) -> list[dict]:
    """
    Fetch full details for papers using ``POST /paper/batch``.

    Sends batches of up to 500 paper IDs per request.
    Returns the raw S2 JSON dicts with all detail fields.
    """
    BATCH_SIZE = 500
    s2_headers = {**_s2_headers(), "Content-Type": "application/json"}
    all_details: list[dict] = []

    for start in range(0, len(paper_ids), BATCH_SIZE):
        batch = paper_ids[start : start + BATCH_SIZE]
        batch_num = start // BATCH_SIZE + 1
        total_batches = (len(paper_ids) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"  Fetching paper details batch {batch_num}/{total_batches} ({len(batch)} papers) ...")

        data = _s2_request(
            client,
            "POST",
            f"{S2_API_BASE}/paper/batch",
            headers=s2_headers,
            delay=delay,
            params={"fields": S2_DETAIL_FIELDS},
            json={"ids": batch},
        )
        if data and isinstance(data, list):
            # Filter out None entries (papers not found)
            all_details.extend([p for p in data if p is not None])
        else:
            print(f"    Warning: batch {batch_num} returned no data")

        time.sleep(delay)

    return all_details


def save_paper_details(details: list[dict], output_path: str):
    """Save the raw Semantic Scholar paper details to a JSON file."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(details, f, indent=2, ensure_ascii=False)
    print(f"  Saved {len(details)} paper details -> {output_path}")


# ── Main search orchestrator ─────────────────────────────────────────────────

def run_search(
    queries: list[str],
    include_daily_papers: bool = True,
    include_semantic_scholar: bool = True,
    delay: float = 1.0,
    max_datasets_per_query: int = 200,
    max_papers_per_query: int = 1000,
    fetch_details: bool = True,
    details_output_path: str = "output/s2_paper_details.json",
) -> list[BenchmarkEntry]:
    """
    Run all searches and return de-duplicated results.

    Args:
        queries: Search terms to use.
        include_daily_papers: Also fetch HuggingFace trending daily papers.
        include_semantic_scholar: Use S2 bulk search for papers (200M+ corpus).
        delay: Seconds between request batches (be polite).
        max_datasets_per_query: Max HF dataset results per query (paginated).
        max_papers_per_query: Max paper results per S2 bulk query (up to 1000/page).
        fetch_details: After bulk search, fetch full paper details via batch API.
        details_output_path: Where to save the raw S2 paper detail JSON.
    """
    all_results: list[BenchmarkEntry] = []
    seen_urls: set[str] = set()
    s2_paper_ids: list[str] = []  # collect S2 paper IDs for detail fetch

    def _add(entries: list[BenchmarkEntry]) -> int:
        added = 0
        for e in entries:
            if e.source_url not in seen_urls:
                seen_urls.add(e.source_url)
                all_results.append(e)
                added += 1
        return added

    # If using S2 without an API key, enforce a longer delay to avoid rate limits
    if include_semantic_scholar:
        if _s2_api_key():
            print("Semantic Scholar API key detected.")
        else:
            print("No S2_API_KEY set -- using unauthenticated rate limit (slow).")
            print("Set S2_API_KEY env var for faster paper search.\n")
            delay = max(delay, 3.0)

    with httpx.Client() as client:
        # ── HuggingFace daily papers ─────────────────────────────────────
        if include_daily_papers:
            print("Fetching HuggingFace daily papers (API) ...")
            papers = fetch_daily_papers(client)
            added = _add(papers)
            print(f"   -> {len(papers)} daily papers ({added} new)")
            time.sleep(delay)

        total_queries = len(queries)
        for i, q in enumerate(queries, 1):
            print(f"\n[{i}/{total_queries}] Query: '{q}'")

            # ── Semantic Scholar bulk search ──────────────────────────────
            if include_semantic_scholar:
                print(f"  S2 bulk search ...")
                s2_papers = search_semantic_scholar(
                    q, client, max_results=max_papers_per_query, delay=delay,
                )
                added = _add(s2_papers)
                print(f"   -> {len(s2_papers)} papers ({added} new)")
                time.sleep(delay)
            else:
                # Fall back to HuggingFace paper search
                print(f"  Searching HF papers ...")
                hf_papers = search_papers(q, client, max_results=max_papers_per_query)
                added = _add(hf_papers)
                print(f"   -> {len(hf_papers)} papers ({added} new)")
                time.sleep(delay)

            # ── HuggingFace datasets ─────────────────────────────────────
            print(f"  Searching HF datasets ...")
            datasets = search_datasets(
                q, client, max_results=max_datasets_per_query, delay=delay * 0.5,
            )
            added = _add(datasets)
            print(f"   -> {len(datasets)} datasets ({added} new)")
            time.sleep(delay)

        print(f"\nFound {len(all_results)} unique results across {total_queries} queries.")

        # ── Fetch full S2 paper details for all paper entries ────────────
        if include_semantic_scholar and fetch_details:
            # Extract S2 paper IDs from source URLs
            for entry in all_results:
                if entry.source_type == "paper":
                    # Try to extract S2 paper ID from the URL or tags
                    url = entry.source_url
                    if "semanticscholar.org/paper/" in url:
                        pid = url.split("/paper/")[-1].split("/")[0].split("?")[0]
                        if pid:
                            s2_paper_ids.append(pid)
                    elif "arxiv.org/abs/" in url:
                        arxiv_id = url.split("/abs/")[-1].split("?")[0]
                        if arxiv_id:
                            s2_paper_ids.append(f"ArXiv:{arxiv_id}")

            # De-duplicate paper IDs
            s2_paper_ids_unique = list(dict.fromkeys(s2_paper_ids))

            if s2_paper_ids_unique:
                print(f"\nFetching full details for {len(s2_paper_ids_unique)} papers via S2 batch API ...")
                details = fetch_paper_details(
                    s2_paper_ids_unique, client, delay=delay,
                )
                print(f"  Retrieved details for {len(details)}/{len(s2_paper_ids_unique)} papers.")
                save_paper_details(details, details_output_path)

    return all_results
