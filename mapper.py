"""
Benchmark Mapper — maps discovered benchmarks to the education framework
categories and tool types using keyword heuristics.

This is a first-pass heuristic mapper. You can refine the keyword lists
or replace this with an LLM-based classifier for higher accuracy.
"""

from config import FRAMEWORK, TOOL_TYPES
from scraper import BenchmarkEntry

# ── Keyword → framework-id mapping ──────────────────────────────────────────
# Each key is a framework ID; its value is a list of keywords/phrases.
# A benchmark matches if its name+description contains any keyword.

FRAMEWORK_KEYWORDS: dict[str, list[str]] = {
    "1": [
        "general reasoning", "reasoning", "commonsense", "logic",
        "problem solving", "critical thinking", "cognitive", "GPQA",
        "BIG-Bench", "HellaSwag", "Winogrande", "ARC-Challenge",
        "abstract reasoning", "analogical",
    ],
    "2.1": [
        "pedagogical knowledge", "teaching knowledge", "instructional design",
        "curriculum design", "learning theory", "pedagogy knowledge",
        "teacher knowledge", "PCK", "TPACK", "educational psychology",
        "lesson planning",
    ],
    "2.2": [
        "explanation quality", "generated explanation", "instructional text",
        "hint generation", "step-by-step explanation", "pedagogical output",
        "teaching quality", "educational generation", "worked example",
    ],
    "2.3": [
        "tutoring", "tutor", "Socratic", "scaffolding", "dialogue",
        "interactive teaching", "conversational tutor", "student interaction",
        "adaptive dialogue", "TutorChat", "TutorEval", "multi-turn education",
    ],
    "3.1": [
        "content knowledge", "subject knowledge", "MMLU", "STEM",
        "math", "science", "history", "biology", "chemistry", "physics",
        "reading comprehension", "SciQ", "OpenBookQA", "MathBench",
        "MAmmoTH", "GSM8K", "MATH benchmark", "medical knowledge",
        "computer science", "humanities", "social science",
    ],
    "3.2": [
        "content alignment", "curriculum alignment", "learning objective",
        "standards alignment", "bloom taxonomy", "learning outcome",
        "course material", "syllabus", "content mapping",
    ],
    "4.1": [
        "scoring", "grading", "rubric", "automated essay scoring",
        "AES", "ASAP", "essay scoring", "short answer grading",
        "mark scheme", "assessment scoring",
    ],
    "4.2": [
        "feedback", "feedback generation", "formative feedback",
        "reasoning feedback", "error analysis", "misconception",
        "diagnostic feedback", "corrective feedback", "actionable feedback",
    ],
    "5": [
        "bias", "fairness", "ethics", "toxicity", "safety",
        "stereotype", "discrimination", "equity", "BBQ",
        "FairEval", "TruthfulQA", "harmful", "responsible AI",
        "cultural sensitivity",
    ],
    "6.1": [
        "multimodal", "vision", "image understanding", "diagram",
        "figure", "chart understanding", "OCR", "visual question",
        "MathVista", "MMMU", "multi-modal education", "video understanding",
        "audio", "speech",
    ],
    "6.2": [
        "multilingual", "cross-lingual", "translation", "EXAMS",
        "language diversity", "non-English", "low-resource language",
        "multilingual education", "polyglot",
    ],
}

# ── Keyword → tool-type mapping ──────────────────────────────────────────────

TOOL_KEYWORDS: dict[str, list[str]] = {
    "ai_tutor": [
        "tutor", "tutoring", "Socratic", "dialogue", "conversational",
        "1-to-1", "one-on-one", "student interaction", "chat-based",
        "scaffolding", "hint", "explanation", "worked example",
    ],
    "pal": [
        "adaptive", "personalised", "personalized", "adaptive learning",
        "learning path", "difficulty adaptation", "student model",
        "knowledge tracing", "learner model", "ITS", "intelligent tutoring",
        "mastery", "spaced repetition",
    ],
    "teacher_support": [
        "teacher", "grading", "scoring", "rubric", "lesson plan",
        "curriculum", "content generation", "question generation",
        "assessment creation", "analytics", "learning analytics",
        "classroom", "instructor", "marking",
    ],
}


def _text_blob(entry: BenchmarkEntry) -> str:
    """Combine searchable text fields into one lowercase string."""
    parts = [entry.name, entry.description] + entry.tags
    return " ".join(parts).lower()


def map_to_framework(entry: BenchmarkEntry) -> list[str]:
    """Return list of matching framework IDs for a benchmark entry."""
    blob = _text_blob(entry)
    matches = []
    for fid, keywords in FRAMEWORK_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in blob:
                matches.append(fid)
                break
    return matches


def map_to_tools(entry: BenchmarkEntry) -> list[str]:
    """Return list of matching tool type keys for a benchmark entry."""
    blob = _text_blob(entry)
    matches = []
    for tid, keywords in TOOL_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in blob:
                matches.append(tid)
                break
    return matches


def map_all(entries: list[BenchmarkEntry]) -> list[BenchmarkEntry]:
    """Map all entries to framework categories and tool types, in place.

    If an entry already has framework_ids or tool_types set (e.g. from
    the curated known_benchmarks list), those are preserved and augmented
    with any additional keyword matches.
    """
    mapped_count = 0
    for entry in entries:
        # Augment rather than replace: keep hand-curated IDs, add keyword hits
        kw_framework = map_to_framework(entry)
        kw_tools = map_to_tools(entry)

        existing_fw = set(entry.framework_ids)
        existing_tools = set(entry.tool_types)

        merged_fw = list(dict.fromkeys(entry.framework_ids + [f for f in kw_framework if f not in existing_fw]))
        merged_tools = list(dict.fromkeys(entry.tool_types + [t for t in kw_tools if t not in existing_tools]))

        entry.framework_ids = merged_fw
        entry.tool_types = merged_tools

        if entry.framework_ids:
            mapped_count += 1
    print(f"Mapped {mapped_count}/{len(entries)} entries to at least one framework category.")
    return entries
