"""
Education Benchmark Mapping Framework - Configuration

Defines the education framework categories and tool types used to classify
benchmarks discovered from HuggingFace and other sources.
"""

# ── Education framework categories (from the mapping image) ──────────────────

FRAMEWORK = {
    "1": {
        "area": "General reasoning",
        "id": "1",
        "name": "General reasoning",
        "description": "Benchmarks measuring general cognitive and reasoning abilities (logic, math, reading comprehension, problem-solving).",
    },
    "2.1": {
        "area": "Pedagogy",
        "id": "2.1",
        "name": "Pedagogical knowledge",
        "description": "Benchmarks measuring knowledge *about* teaching — instructional strategies, learning theories, curriculum design.",
    },
    "2.2": {
        "area": "Pedagogy",
        "id": "2.2",
        "name": "Pedagogy of generated outputs",
        "description": "Benchmarks evaluating the pedagogical quality of AI-generated explanations, hints, and instructional content.",
    },
    "2.3": {
        "area": "Pedagogy",
        "id": "2.3",
        "name": "Pedagogical interactions",
        "description": "Benchmarks evaluating interactive teaching behaviours — Socratic questioning, scaffolding, adaptive dialogue.",
    },
    "3.1": {
        "area": "Educational content",
        "id": "3.1",
        "name": "Content knowledge",
        "description": "Benchmarks measuring mastery of subject-matter content (STEM, humanities, etc.).",
    },
    "3.2": {
        "area": "Educational content",
        "id": "3.2",
        "name": "Content alignment",
        "description": "Benchmarks measuring alignment of content to curricula, standards, or learning objectives.",
    },
    "4.1": {
        "area": "Assessment",
        "id": "4.1",
        "name": "Scoring and grading",
        "description": "Benchmarks evaluating automated scoring, grading, and rubric application.",
    },
    "4.2": {
        "area": "Assessment",
        "id": "4.2",
        "name": "Feedback with reasoning",
        "description": "Benchmarks evaluating quality of feedback — explanations, reasoning traces, actionable suggestions.",
    },
    "5": {
        "area": "Ethics and bias",
        "id": "5",
        "name": "Ethics and bias",
        "description": "Benchmarks measuring fairness, bias, safety, and ethical behaviour in educational contexts.",
    },
    "6.1": {
        "area": "Digitisation / accessibility",
        "id": "6.1",
        "name": "Multimodal capabilities",
        "description": "Benchmarks evaluating vision, audio, diagram understanding, and multimodal reasoning for education.",
    },
    "6.2": {
        "area": "Digitisation / accessibility",
        "id": "6.2",
        "name": "Multilingual capabilities",
        "description": "Benchmarks evaluating performance across languages and cross-lingual educational tasks.",
    },
}

# ── Tool types ───────────────────────────────────────────────────────────────

TOOL_TYPES = {
    "ai_tutor": {
        "name": "AI Tutors",
        "description": "1-to-1 conversational tutoring systems (e.g. Khanmigo, Duolingo Max).",
        "key_needs": ["2.3", "2.2", "4.2", "3.1", "1"],
    },
    "pal": {
        "name": "Personalised Adaptive Learning",
        "description": "Systems that adapt content/difficulty to individual learners (e.g. adaptive courseware, ITS).",
        "key_needs": ["3.2", "2.1", "4.1", "4.2", "6.1", "6.2"],
    },
    "teacher_support": {
        "name": "Teacher Support Tools",
        "description": "Tools that assist teachers — lesson planning, content generation, grading, analytics.",
        "key_needs": ["2.1", "3.1", "3.2", "4.1", "4.2", "5"],
    },
}

# ── HuggingFace search queries ───────────────────────────────────────────────

HF_SEARCH_QUERIES = [
    # Direct education
    "education benchmark",
    "educational evaluation LLM",
    "tutoring benchmark",
    "pedagogy evaluation",
    "pedagogical knowledge",
    "teaching assessment AI",
    # Content knowledge
    "MMLU benchmark",
    "math reasoning benchmark",
    "science question answering",
    "ARC benchmark",
    "OpenBookQA",
    # Assessment
    "automated essay scoring",
    "grading rubric LLM",
    "feedback generation education",
    # Pedagogy
    "Socratic questioning",
    "tutoring dialogue",
    "adaptive learning evaluation",
    "scaffolding education AI",
    # Ethics and bias
    "bias fairness education",
    "FairEval benchmark",
    "BBQ bias benchmark",
    # Multimodal
    "multimodal education",
    "math vision benchmark",
    "diagram understanding",
    # Multilingual
    "multilingual education benchmark",
    "EXAMS multilingual",
    "cross-lingual education",
]

# ── Output settings ──────────────────────────────────────────────────────────

OUTPUT_DIR = "output"
REPORT_FILENAME = "education_benchmark_mapping"
