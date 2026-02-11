"""
Report generator — outputs the mapped benchmarks as Markdown and CSV.
"""

import csv
import json
import os
from datetime import datetime

from config import FRAMEWORK, TOOL_TYPES, OUTPUT_DIR, REPORT_FILENAME
from scraper import BenchmarkEntry


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _framework_label(fid: str) -> str:
    entry = FRAMEWORK.get(fid)
    return f"{fid} {entry['name']}" if entry else fid


def _tool_label(tid: str) -> str:
    entry = TOOL_TYPES.get(tid)
    return entry["name"] if entry else tid


# ── Markdown report ──────────────────────────────────────────────────────────

def generate_markdown(entries: list[BenchmarkEntry]) -> str:
    """Generate a full Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Education Benchmark Mapping Report",
        f"Generated: {now}\n",
        f"Total benchmarks found: **{len(entries)}**\n",
    ]

    # ── Summary matrix ───────────────────────────────────────────────────
    lines.append("## Summary Matrix\n")
    lines.append("| Framework Category | AI Tutors | PAL Systems | Teacher Support | Total |")
    lines.append("|---|---|---|---|---|")

    for fid, finfo in FRAMEWORK.items():
        in_cat = [e for e in entries if fid in e.framework_ids]
        tutor = sum(1 for e in in_cat if "ai_tutor" in e.tool_types)
        pal = sum(1 for e in in_cat if "pal" in e.tool_types)
        teacher = sum(1 for e in in_cat if "teacher_support" in e.tool_types)
        total = len(in_cat)
        lines.append(f"| **{fid}** {finfo['name']} | {tutor} | {pal} | {teacher} | {total} |")

    lines.append("")

    # ── Per-category detail ──────────────────────────────────────────────
    lines.append("## Benchmarks by Framework Category\n")

    for fid, finfo in FRAMEWORK.items():
        in_cat = [e for e in entries if fid in e.framework_ids]
        lines.append(f"### {fid} — {finfo['name']}")
        lines.append(f"*{finfo['description']}*\n")

        if not in_cat:
            lines.append("*No benchmarks mapped to this category yet.*\n")
            continue

        for e in in_cat:
            tools = ", ".join(_tool_label(t) for t in e.tool_types) or "General"
            lines.append(f"- **[{e.name}]({e.source_url})** ({e.source_type})")
            lines.append(f"  - Tools: {tools}")
            if e.description and e.description != "(from daily papers page)":
                lines.append(f"  - {e.description[:200]}")
            if e.date:
                lines.append(f"  - Date: {e.date}")
        lines.append("")

    # ── Per-tool-type view ───────────────────────────────────────────────
    lines.append("## Benchmarks by Tool Type\n")

    for tid, tinfo in TOOL_TYPES.items():
        in_tool = [e for e in entries if tid in e.tool_types]
        lines.append(f"### {tinfo['name']}")
        lines.append(f"*{tinfo['description']}*\n")

        if not in_tool:
            lines.append("*No benchmarks mapped to this tool type yet.*\n")
            continue

        for e in in_tool:
            cats = ", ".join(_framework_label(f) for f in e.framework_ids)
            lines.append(f"- **[{e.name}]({e.source_url})**")
            lines.append(f"  - Categories: {cats}")
        lines.append("")

    # ── Unmapped entries ─────────────────────────────────────────────────
    unmapped = [e for e in entries if not e.framework_ids]
    if unmapped:
        lines.append("## Unmapped Entries\n")
        lines.append("*These entries were found but did not match any framework category. "
                      "They may still be relevant — review manually.*\n")
        for e in unmapped:
            lines.append(f"- [{e.name}]({e.source_url}) — {e.description[:120]}")
        lines.append("")

    return "\n".join(lines)


# ── CSV report ───────────────────────────────────────────────────────────────

def generate_csv(entries: list[BenchmarkEntry], path: str):
    """Write entries to a CSV file."""
    fieldnames = [
        "name", "source_url", "source_type", "description", "date",
        "framework_ids", "framework_names", "tool_types", "tool_names", "tags",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in entries:
            writer.writerow({
                "name": e.name,
                "source_url": e.source_url,
                "source_type": e.source_type,
                "description": e.description,
                "date": e.date,
                "framework_ids": "; ".join(e.framework_ids),
                "framework_names": "; ".join(_framework_label(f) for f in e.framework_ids),
                "tool_types": "; ".join(e.tool_types),
                "tool_names": "; ".join(_tool_label(t) for t in e.tool_types),
                "tags": "; ".join(e.tags),
            })


# ── JSON dump ────────────────────────────────────────────────────────────────

def generate_json(entries: list[BenchmarkEntry], path: str):
    """Write entries to a JSON file."""
    data = [e.to_dict() for e in entries]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Write all reports ────────────────────────────────────────────────────────

def write_reports(entries: list[BenchmarkEntry]):
    """Generate and save Markdown, CSV, and JSON reports."""
    _ensure_output_dir()

    md_path = os.path.join(OUTPUT_DIR, f"{REPORT_FILENAME}.md")
    csv_path = os.path.join(OUTPUT_DIR, f"{REPORT_FILENAME}.csv")
    json_path = os.path.join(OUTPUT_DIR, f"{REPORT_FILENAME}.json")

    md = generate_markdown(entries)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"  Markdown -> {md_path}")

    generate_csv(entries, csv_path)
    print(f"  CSV      -> {csv_path}")

    generate_json(entries, json_path)
    print(f"  JSON     -> {json_path}")

    return md_path, csv_path, json_path
