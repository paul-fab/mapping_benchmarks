"""
K-12 Education Benchmark Mapping Framework - Configuration

Defines the education framework categories and tool types used to classify
benchmarks discovered from HuggingFace and other sources.

SCOPE: K-12 education (ages 5-18, primary and secondary school).
"""

# ── Education framework categories (from the mapping image) ──────────────────

FRAMEWORK = {
    "1": {
        "area": "General reasoning",
        "id": "1",
        "name": "General reasoning",
        "description": "Benchmarks measuring general cognitive and reasoning abilities relevant to K-12 learners (logic, math, reading comprehension, problem-solving).",
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
        "description": "Benchmarks measuring mastery of K-12 subject-matter content (STEM, humanities, etc.).",
    },
    "3.2": {
        "area": "Educational content",
        "id": "3.2",
        "name": "Content alignment",
        "description": "Benchmarks measuring alignment of content to K-12 curricula, standards (e.g. Common Core), or learning objectives.",
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
        "description": "Benchmarks measuring fairness, bias, safety, and ethical behaviour in K-12 educational contexts (including child safety).",
    },
    "6.1": {
        "area": "Digitisation / accessibility",
        "id": "6.1",
        "name": "Multimodal capabilities",
        "description": "Benchmarks evaluating vision, audio, diagram understanding, and multimodal reasoning for K-12 education.",
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
    # ── Layer 1: Broad discovery (wide net, K-12 focus) ────────────────
    "LLM evaluation K-12 education",
    "benchmark dataset education learning",
    "AI tutoring evaluation K-12",
    "educational assessment natural language processing",
    "large language model evaluation education",
    "K-12 AI benchmark",
    "primary school AI evaluation",
    "secondary school AI evaluation",
    "elementary education benchmark",

    # ── Layer 2: Framework-aligned queries ────────────────────────────
    # 1 – General reasoning
    "reasoning evaluation LLM",
    "commonsense reasoning test",
    "math word problems grade school",
    # 2.1 – Pedagogical knowledge
    "pedagogical content knowledge assessment",
    "teacher knowledge evaluation AI",
    "K-12 teaching strategies assessment",
    # 2.2 – Pedagogy of generated outputs
    "explanation quality evaluation",
    "instructional text generation",
    "age-appropriate explanation generation",
    # 2.3 – Pedagogical interactions
    "tutoring dialogue evaluation",
    "Socratic method AI education",
    "intelligent tutoring system evaluation",
    # 3.1 – Content knowledge
    "STEM knowledge evaluation K-12",
    "math reasoning evaluation grade school",
    "science question answering dataset K-12",
    "K-12 education evaluation AI",
    "elementary math benchmark",
    "high school science evaluation",
    # 3.2 – Content alignment
    "curriculum alignment evaluation K-12",
    "learning objectives assessment",
    "Bloom taxonomy classification",
    "Common Core standards alignment",
    "grade level text complexity",
    # 4.1 – Scoring and grading
    "automated essay scoring evaluation",
    "short answer grading NLP",
    "K-12 student writing assessment",
    # 4.2 – Feedback with reasoning
    "automated feedback education",
    "misconception detection student",
    "formative assessment AI",
    "student homework feedback",
    # 5 – Ethics and bias
    "bias fairness evaluation LLM education",
    "safety evaluation language model children",
    "child-safe AI evaluation",
    # 6.1 – Multimodal
    "multimodal education evaluation",
    "visual question answering STEM",
    "diagram understanding evaluation",
    # 6.2 – Multilingual
    "multilingual evaluation education",
    "cross-lingual assessment benchmark",

    # ── Layer 3: Learning science / cognitive impact ────────────────────
    "cognitive offloading AI students",
    "cognitive load theory AI education",
    "productive struggle AI learning",
    "desirable difficulties learning",
    "metacognition self-regulated learning AI",
    "critical thinking AI education evaluation",
    "higher order thinking skills AI",
    "student over-reliance AI",
    "AI dependency learning outcomes",
    "Socratic reasoning evaluation",
    "learning transfer AI assisted",
    "student autonomy AI education",
    "zone of proximal development AI tutoring",
    "scaffolding vs over-scaffolding AI",
    "student agency AI learning",
    "deep learning vs surface learning education",

    # ── Layer 4: Niche / emerging K-12 areas ──────────────────────────
    "knowledge tracing student model",
    "question generation education",
    "reading comprehension difficulty level",
    "code education evaluation programming K-12",
    "LLM as judge evaluation",
    "AI grading rubric evaluation",
    "student error analysis",
    "educational dialogue system",
    "exam question generation assessment",
    "reading level assessment",
    "adaptive learning K-12",
    "gamification education evaluation",
    "special education AI evaluation",
]

# ── Output settings ──────────────────────────────────────────────────────────

OUTPUT_DIR = "output"
REPORT_FILENAME = "education_benchmark_mapping"
