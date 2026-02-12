# Education Benchmark Mapper

Search Semantic Scholar + HuggingFace for AI/LLM benchmarks and map them to a K-12 education evaluation framework.

**Live site:** [benchmarks.edtechquality.ai](https://benchmarks.edtechquality.ai)

## Overview

This project has two parts:

1. **Python pipeline** — discovers benchmarks/papers from Semantic Scholar and HuggingFace, classifies them into an education framework using heuristic keywords + LLM (Anthropic Claude), and generates reports.
2. **SvelteKit website** — a static site that presents the mapped benchmarks with search, filtering, and review tools.

## Project Structure

```
├── main.py              # CLI entry point for the full pipeline
├── scraper.py           # HuggingFace + Semantic Scholar API search
├── mapper.py            # Two-stage classification (heuristic + LLM)
├── known_benchmarks.py  # Hand-curated benchmark entries
├── config.py            # Framework categories, tool types, search queries
├── report.py            # Markdown / CSV / JSON report generation
├── download_papers.py   # Bulk PDF downloader for discovered papers
├── parse_papers.py      # PDF → text parser (parallel, multi-format output)
├── rank_papers.py       # LLM relevance scoring + reclassification
├── extract_sections.py  # Smart section extractor (78% token reduction)
├── research_categories.py # SoTA research via Anthropic Batch API
├── curate.py            # Curation utilities (merges scores → website)
├── pyproject.toml       # Python dependencies (managed by uv)
├── output/              # Generated reports + cached data
│   ├── education_benchmark_mapping.{md,csv,json}
│   ├── scraped_cache.json
│   ├── s2_paper_details.json
│   ├── paper_scores.json     # LLM relevance scores
│   ├── all_papers.jsonl      # Parsed paper text
│   ├── papers/               # Downloaded PDFs
│   ├── papers_parsed/        # Parsed JSON per paper
│   └── research/             # Per-category SoTA analysis
└── website/             # SvelteKit frontend
    ├── svelte.config.js         # SvelteKit config (adapter-static)
    ├── src/
    │   ├── lib/
    │   │   ├── data/
    │   │   │   ├── benchmarks.ts   # Benchmark loading + filtering
    │   │   │   ├── search.ts       # MiniSearch full-text search engine
    │   │   │   ├── framework.ts    # Education framework definitions
    │   │   │   └── tool-types.ts   # Tool type definitions
    │   │   ├── components/         # Svelte UI components
    │   │   ├── stores/             # Svelte 5 runes-based stores
    │   │   └── types.ts            # TypeScript interfaces
    │   └── routes/                 # SvelteKit pages
    │       ├── benchmark/[slug]/   # Individual benchmark detail
    │       ├── framework/[id]/     # Framework category view
    │       ├── tool-type/[key]/    # Tool type view
    │       └── research/           # Research analysis pages
    └── static/
        └── benchmarks.json         # Static benchmark data (loaded at runtime)
```

## Python Pipeline

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- API keys in `.env`:
  - `ANTHROPIC_API_KEY` — for LLM classification (optional, falls back to heuristics)
  - `S2_API_KEY` — for Semantic Scholar (optional, uses unauthenticated rate limit)

### Usage

```sh
# Full pipeline: S2 + HF search → LLM classification → reports
uv run main.py

# Common flags
uv run main.py --known-only     # Only use curated known benchmarks (no API search)
uv run main.py --skip-search    # Skip search, reload previous scraped results from cache
uv run main.py --no-llm         # Skip LLM classification; heuristic keywords only
uv run main.py --no-s2          # Skip Semantic Scholar; only use HuggingFace
uv run main.py --query "math"   # Add a custom query to the search list
```

### Classification Pipeline

1. **Search** — queries Semantic Scholar (bulk API, up to 1000 results/query) and HuggingFace (datasets + papers)
2. **Heuristic scoring** — word-boundary keyword matching with multi-word phrase boosting
3. **LLM classification** — Anthropic Claude classifies entries in parallel batches with S2 TLDR context enrichment
4. **Reports** — generates Markdown, CSV, and JSON output

### Deep Analysis Pipeline

After the initial classification, a deeper analysis pipeline processes full paper PDFs:

```sh
uv run download_papers.py                  # Download all PDFs (parallel, ~8K papers)
uv run parse_papers.py                     # Parse PDFs → text (parallel, JSON + MD + JSONL)
uv run rank_papers.py                      # LLM relevance scoring 1-10 + reclassification
uv run curate.py sync                      # Merge scores into website benchmarks.json
uv run extract_sections.py                 # Preview smart extraction stats
uv run research_categories.py              # Submit batch SoTA research (50% cost savings)
uv run research_categories.py --status     # Check batch progress
uv run research_categories.py --collect    # Collect completed results
```

### Smart Section Extraction

Academic papers follow a predictable IMRAD structure. Rather than sending full text (~14,500 tokens/paper) or just abstracts (~400 tokens), we extract the **information-dense sections** — Abstract, Introduction, Results, Discussion, Conclusion, and Limitations — achieving:

| Metric | Value |
|---|---|
| Compression | 83% reduction (17% of original) |
| Avg tokens/paper | ~2,500 (down from ~14,500) |
| Section detection rate | 99.8% of papers |
| Detection method | Numbered headings + keyword fallback |

This is documented in detail in `extract_sections.py`.

### Batch API

The `research_categories.py` script uses the [Anthropic Message Batches API](https://docs.anthropic.com/en/api/messages-batches) for **50% cost savings** on the SoTA synthesis. Papers are grouped by framework category, split into sub-batches that fit within 200K context windows, and submitted as a single batch job that processes within 24 hours.

## Website

### Prerequisites

- Node.js 18+
- npm

### Development

```sh
cd website
npm install
npm run dev
```

### Search

The website uses [MiniSearch](https://github.com/lucaong/minisearch) for client-side full-text search across 14K+ benchmarks. Features:

- **Ranked results** — BM25-based scoring, most relevant first
- **Fuzzy matching** — handles typos (e.g. "tutring" → "tutoring")
- **Prefix search** — results appear as you type
- **Field boosting** — benchmark names weighted 3×, tags 2×, TLDR 1.5×, descriptions 1×
- **Automatic fallback** — if strict search finds nothing, retries with higher fuzziness
- Indexes all benchmarks on first page load (~100ms for 14K documents)

### Data Enrichment

Each benchmark is enriched with metadata from Semantic Scholar paper details (via `curate.py sync`):

- **TLDR** — AI-generated one-line summary (available for ~69% of entries)
- **Citation count** — total citations from S2 (available for ~77% of entries)
- **PDF URL** — open-access PDF link (available for ~26% of entries)

The enrichment happens in `curate.py` `generate_benchmarks_json()`, which joins pipeline entries with `output/s2_paper_details.json` by matching source URLs to S2 paper IDs and ArXiv IDs.

### Building

```sh
npm run build    # outputs static site to website/build/
npm run preview  # preview the production build locally
```

### Deployment

The site is deployed as static files on a DigitalOcean droplet at [benchmarks.edtechquality.ai](https://benchmarks.edtechquality.ai), served by Nginx with Let's Encrypt SSL.

To redeploy after changes:

```sh
cd website
npm run build
# From Git Bash (for incremental sync):
rsync -avz --delete build/ root@157.245.0.32:/var/www/benchmarks/ --chown=www-data:www-data
```

## Education Framework

The framework classifies benchmarks across these areas:

| ID  | Category                    | Area                        |
|-----|-----------------------------|-----------------------------|
| 1   | General reasoning           | General reasoning           |
| 2.1 | Pedagogical knowledge       | Pedagogy                    |
| 2.2 | Pedagogy of generated outputs | Pedagogy                  |
| 2.3 | Pedagogical interactions    | Pedagogy                    |
| 3.1 | Content knowledge           | Educational content         |
| 3.2 | Content alignment           | Educational content         |
| 4.1 | Scoring and grading         | Assessment                  |
| 4.2 | Feedback with reasoning     | Assessment                  |
| 5   | Ethics and bias             | Ethics and bias             |
| 6.1 | Multimodal capabilities     | Digitisation / accessibility |
| 6.2 | Multilingual capabilities   | Digitisation / accessibility |

### Tool Types

- **AI Tutors** — 1-to-1 conversational tutoring systems
- **Personalised Adaptive Learning (PAL)** — systems that adapt content/difficulty to individual learners
- **Teacher Support Tools** — lesson planning, content generation, grading, analytics
