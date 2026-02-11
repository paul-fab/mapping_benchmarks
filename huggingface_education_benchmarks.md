# HuggingFace Education Benchmarks, Evaluations, and Datasets
## Comprehensive Survey (2024-2026)

Last updated: 2026-02-11

---

## PART 1: KEY BENCHMARKS AND EVALUATION PAPERS

### 1. MathTutorBench
- **Paper**: "MathTutorBench: A Benchmark for Measuring Open-ended Pedagogical Capabilities of LLM Tutors"
- **HuggingFace URL**: https://huggingface.co/papers/2502.18940
- **Date**: February 26, 2025
- **Authors**: Jakub Macina, Nico Daheim, Ido Hakimi, Manu Kapur, Iryna Gurevych, Mrinmaya Sachan
- **What it measures**: Evaluates AI tutoring models on pedagogical quality, subject expertise, dialog-based teaching, and questioning strategies. Uses a trained reward model to score open-ended teacher responses.
- **Key findings**: Subject expertise does NOT translate to good teaching; pedagogy and expertise form a trade-off. No models exceed 56% performance. Longer dialogs make questioning strategies fail.
- **Resources**: Open-source benchmark, reward model (eth-nlped/Qwen2.5-1.5B-pedagogical-rewardmodel), leaderboard at https://eth-lre.github.io/mathtutorbench/

### 2. TutorBench
- **Paper**: "TutorBench: A Benchmark To Assess Tutoring Capabilities Of Large Language Models"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2510.02663
- **HuggingFace Dataset URL**: https://huggingface.co/datasets/ScaleAI/TutorBench
- **Date**: October 3, 2025
- **Authors**: Rakshith S Srinivasa, Zora Che, et al. (Scale AI)
- **What it measures**: Evaluates LLMs on three core tutoring tasks: adaptive explanations, actionable feedback, and active learning (hint generation). 1,490 samples curated by human experts across high-school and AP-level curricula (Chemistry, Calculus, Biology, Physics, Computer Science).
- **Key findings**: No frontier LLMs achieved >56%. All tested models achieved <60% pass rate on criteria for guiding, diagnosing, and supporting students. Claude models outperform on active learning but lag on explanations/feedback.
- **Dataset size**: 1,470 rows, multimodal (text + images)

### 3. The Pedagogy Benchmark
- **Paper**: "Benchmarking the Pedagogical Knowledge of Large Language Models"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2506.18710
- **HuggingFace Dataset URL**: https://huggingface.co/datasets/AI-for-Education/pedagogy-benchmark
- **Date**: June 23, 2025
- **License**: MIT
- **What it measures**: Evaluates LLMs on pedagogical knowledge including teaching strategies, assessment methods, student understanding, education theories, and classroom management. Two subsets: CDPK (920 MCQs on cross-domain pedagogical knowledge) and SEND (223 MCQs on special educational needs and disability).
- **Source**: Chilean Ministry of Education teacher training exams (translated from Spanish to English)
- **97 models evaluated** with online leaderboards
- **Dataset size**: 1,143 questions total

### 4. EduBench
- **Paper**: "EduBench: A Comprehensive Benchmarking Dataset for Evaluating Large Language Models in Diverse Educational Scenarios"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2505.16160
- **HuggingFace Dataset URL**: https://huggingface.co/datasets/DirectionAI/EduBench
- **Date**: May 21, 2025
- **Authors**: Bin Xu, Yu Bai, Huashan Sun, et al. (Beijing Institute of Technology)
- **License**: MIT
- **What it measures**: First diverse benchmark for educational scenarios with 9 major scenarios, 4,000+ educational contexts, and multi-dimensional evaluation metrics covering 12 critical aspects. Covers Q&A, error correction, and more across multiple subjects and difficulty levels (Chinese + English).
- **Key findings**: A relatively small model trained on EduBench achieves performance comparable to DeepSeek V3 and Qwen Max.

### 5. EducationQ
- **Paper**: "EducationQ: Evaluating LLMs' Teaching Capabilities Through Multi-Agent Dialogue Framework" (ACL 2025)
- **HuggingFace Dataset URL**: https://huggingface.co/datasets/SunriserFuture/EducationQ
- **Date**: January 1, 2026 (dataset); ACL 2025 paper
- **Authors**: Yao Shi, Rongkeng Liang, Yong Xu
- **License**: CC BY 4.0
- **What it measures**: High-quality, balanced, teaching-oriented testbed for evaluating LLMs' pedagogical capabilities. 1,498 questions across 13 disciplines x 10 difficulty levels. Combines GPQA Diamond (198 graduate-level) with MMLU-Pro stratified (1,300 undergraduate-level).
- **Evaluation**: Multi-agent dialogue framework for evaluating teaching capabilities

### 6. ELMES
- **Paper**: "ELMES: An Automated Framework for Evaluating Large Language Models in Educational Scenarios"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2507.22947
- **Date**: July 27, 2025
- **Authors**: Shou'ang Wei, Xinyun Wang, et al.
- **What it measures**: Evaluates LLMs across 4 critical educational scenarios: Knowledge Point Explanation, Guided Problem-Solving Teaching, Interdisciplinary Lesson Plan Generation, and Contextualized Question Generation. Uses LLM-as-a-Judge with fine-grained pedagogical metrics.
- **Open-source framework**: https://github.com/sii-research/elmes.git

### 7. EduAlign (HPC-RM)
- **Paper**: "Cultivating Helpful, Personalized, and Creative AI Tutors: A Framework for Pedagogical Alignment using Reinforcement Learning"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2507.20335
- **Date**: July 27, 2025
- **Authors**: Siyu Song, Wentao Liu, et al.
- **What it measures**: Evaluates AI tutors on three dimensions: Helpfulness (H), Personalization (P), and Creativity (C). Includes HPC-RM reward model trained on 8,000 educational interactions. Fine-tuned with GRPO on 2,000 diverse prompts.

### 8. LearnLM
- **Paper**: "LearnLM: Improving Gemini for Learning"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2412.16429
- **Date**: December 20, 2024
- **Authors**: LearnLM Team (46+ authors, Google)
- **What it measures**: Pedagogical instruction following capabilities. Framework for training pedagogically-aligned LLMs.
- **Key findings**: +31% preference over GPT-4o, +11% over Claude 3.5, +13% over Gemini 1.5 Pro across diverse learning scenarios.

### 9. VisScience
- **Paper**: "VisScience: An Extensive Benchmark for Evaluating K12 Educational Multi-modal Scientific Reasoning"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2409.13730
- **Date**: September 10, 2024
- **Authors**: Zhihuan Jiang, Zhen Yang, et al.
- **What it measures**: Multi-modal scientific reasoning across K12 Mathematics, Physics, and Chemistry. 3,000 questions (1,000 per discipline) across 21 subjects and 5 difficulty levels. Evaluated 25 MLLMs.
- **Key findings**: Best accuracy: Math 53.4% (Claude 3.5-Sonnet), Physics 38.2% (GPT-4o), Chemistry 47.0% (Gemini-1.5-Pro).

### 10. SAS-Bench
- **Paper**: "SAS-Bench: A Fine-Grained Benchmark for Evaluating Short Answer Scoring with Large Language Models"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2505.07247
- **Date**: May 12, 2025
- **What it measures**: LLM-based short answer scoring with fine-grained step-wise scoring. 1,030 questions from real-world subject-specific exams with expert-annotated error categories.

### 11. Math Misconceptions Benchmark
- **Paper**: "A Benchmark for Math Misconceptions: Bridging Gaps in Middle School Algebra with AI-Supported Instruction"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2412.03765
- **HuggingFace Dataset URL**: https://huggingface.co/datasets/nanote/algebra_misconceptions
- **Date**: December 4, 2024
- **Authors**: Nancy Otero, Stefania Druga, Andrew Lan
- **What it measures**: AI systems' ability to detect algebra misconceptions. 55 misconceptions and 220 diagnostic algebra examples.
- **Key findings**: 83.9% precision with topic constraints; 80%+ of educators confirmed encountering these misconceptions.

### 12. COGENT
- **Paper**: "COGENT: A Curriculum-oriented Framework for Generating Grade-appropriate Educational Content"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2506.09367
- **Date**: June 10, 2025
- **Authors**: Zhengyuan Liu, Stella Xin Yin, Dion Hoe-Lian Goh, Nancy F. Chen
- **What it measures**: Grade-appropriateness of generated STEM content. Evaluates curriculum alignment, readability control, and student engagement through wonder-based approaches.
- **Key findings**: Consistently produces grade-appropriate passages comparable or superior to human references.

### 13. EduPlanner
- **Paper**: "EduPlanner: LLM-Based Multi-Agent Systems for Customized and Intelligent Instructional Design"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2504.05370
- **Date**: April 7, 2025
- **Authors**: Xueqiao Zhang, Chao Zhang, et al.
- **What it measures**: Instructional design quality via CIDDP 5-dimensional evaluation: Clarity, Integrity, Depth, Practicality, Pertinence. Tested on GSM8K and Algebra datasets.

### 14. EXAMS-V
- **Paper**: "EXAMS-V: A Multi-Discipline Multilingual Multimodal Exam Benchmark"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2403.10378
- **Date**: March 15, 2024
- **What it measures**: 20,932 multimodal MCQs across 20 disciplines in 11 languages from various education systems.

### 15. M3KE
- **Paper**: "M3KE: A Massive Multi-Level Multi-Subject Knowledge Evaluation Benchmark for Chinese LLMs"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2305.10263
- **Date**: May 17, 2023 (still widely used)
- **What it measures**: 20,477 questions covering 71 tasks across all Chinese education levels (primary to college).

### 16. MathExplain
- **Paper**: "Explain with Visual Keypoints Like a Real Mentor! A Benchmark for Multimodal Solution Explanation"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2504.03197
- **Date**: April 4, 2025
- **What it measures**: 997 math problems annotated with visual keypoints for evaluating multimodal LLM solution explanations in education.

### 17. Socratic Benchmark
- **HuggingFace Dataset URL**: https://huggingface.co/datasets/koutch/socratic_benchmark
- **Date**: August 12, 2025
- **Creator**: Charles Koutcheme
- **What it measures**: Tutor-student interactions for training and evaluating feedback/tutor language models. 267 programming tutoring scenarios across 3 versions with buggy code, bug descriptions, and Socratic dialogue.

### 18. LLM Prompt Evaluation for Educational Applications
- **HuggingFace Paper URL**: https://huggingface.co/papers/2601.16134
- **Date**: January 22, 2026
- **What it measures**: Tournament-style evaluation of LLM prompts in education using Glicko2 rating system. Tests 6 templates across 120 user interactions.

### 19. KoNET (Korean National Education Tests)
- **Paper**: "Evaluating Multimodal Generative AI with Korean Educational Standards"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2502.15422
- **Date**: February 21, 2025
- **What it measures**: Multimodal AI evaluation using Korean national exams (KoEGED, KoMGED, KoHGED, KoCSAT) across educational levels.

### 20. Automated Feedback in Math Education
- **Paper**: "Automated Feedback in Math Education: A Comparative Analysis of LLMs for Open-Ended Responses"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2411.08910
- **Date**: October 29, 2024
- **What it measures**: Compares Mistral (fine-tuned), SBERT, and GPT-4 for evaluating math student responses. Fine-tuned Mistral matches GPT-4.

### 21. Tutor CoPilot
- **Paper**: "Tutor CoPilot: A Human-AI Approach for Scaling Real-Time Expertise"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2410.03017
- **Date**: October 3, 2024
- **What it measures**: RCT with 900 tutors and 1,800 students showing 4 p.p. improvement in topic mastery, with greatest benefit for lower-rated tutors (9 p.p. gain).

### 22. GEDE Benchmark
- **Paper**: "Assessing LLM Text Detection in Educational Contexts"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2508.08096
- **Date**: August 11, 2025
- **What it measures**: 900+ student essays evaluating LLM-generated text detection at various contribution levels in educational contexts.

### 23. The AI Assessment Scale
- **Paper**: "The AI Assessment Scale Revisited: A Framework for Educational Assessment"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2412.09029
- **Date**: December 12, 2024
- **What it measures**: Framework for GenAI integration in educational assessment with five levels, from "No AI" to "AI Exploration."

### 24. EMNLP: Educator-role Moral and Normative LLM Profiling
- **HuggingFace Paper URL**: https://huggingface.co/papers/2508.15250
- **Date**: August 21, 2025
- **What it measures**: Evaluates 12 LLMs in educator roles across 88 teacher-specific moral dilemmas, personality profiling, and soft prompt injection vulnerability.

### 25. CLR-Bench
- **Paper**: "CLR-Bench: Evaluating Large Language Models in College-level Reasoning"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2410.17558
- **Date**: October 23, 2024
- **What it measures**: 1,018 discipline-specific questions across 16 college subjects. Shows GPT-4 Turbo accuracy drops from 63.31% (QA) to 39.00% (QAR reasoning).

### 26. LaoBench
- **Paper**: "LaoBench: A Large-Scale Multidimensional Lao Benchmark"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2511.11334
- **Date**: November 14, 2025
- **What it measures**: First large-scale benchmark for Lao language LLMs across knowledge, K12 education, and bilingual translation.

### 27. Automated Question Generation at Bloom's Skill Levels
- **HuggingFace Paper URL**: https://huggingface.co/papers/2408.04394
- **Date**: August 8, 2024
- **What it measures**: Evaluates 5 LLMs on Bloom's taxonomy-aligned question generation for educational contexts.

### 28. Can LLMs Estimate Student Struggles?
- **HuggingFace Paper URL**: https://huggingface.co/papers/2512.18880
- **Date**: December 21, 2025
- **What it measures**: Large-scale analysis of 20+ models showing systematic misalignment with human difficulty perception in item difficulty prediction.

### 29. MAIC Framework
- **Paper**: "From MOOC to MAIC: Reshaping Online Teaching and Learning through LLM-driven Agents"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2409.03512
- **Date**: September 5, 2024
- **What it measures**: LLM multi-agent system for AI-augmented classrooms, tested at Tsinghua with 500+ students and 100,000+ learning records.

### 30. SciEducator
- **Paper**: "SciEducator: Scientific Video Understanding and Educating via Multi-Agent System"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2511.17943
- **Date**: November 22, 2025
- **What it measures**: Multi-agent system for scientific video comprehension with SciVBench benchmark of 500 expert-verified science QA pairs.

### 31. SimulatorArena
- **Paper**: "SimulatorArena: Are User Simulators Reliable Proxies for Multi-Turn Evaluation?"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2510.05444
- **Date**: October 6, 2025
- **What it measures**: 909 annotated conversations evaluating LLM user simulators on math tutoring and document creation tasks.

### 32. ElectroVizQA
- **Paper**: "ElectroVizQA: How well do Multi-modal LLMs perform in Electronics Visual Question Answering?"
- **HuggingFace Paper URL**: https://huggingface.co/papers/2412.00102
- **Date**: November 27, 2024
- **What it measures**: 626 visual questions evaluating MLLMs on digital electronics circuit problems from undergraduate curricula.

---

## PART 2: KEY DATASETS

### Education Benchmarking Datasets

| Dataset | URL | Description | Size | Updated |
|---------|-----|-------------|------|---------|
| AI-for-Education/pedagogy-benchmark | https://huggingface.co/datasets/AI-for-Education/pedagogy-benchmark | MCQs on pedagogical knowledge (CDPK + SEND) from teacher training exams | 1,143 questions | Jun 2025 |
| DirectionAI/EduBench | https://huggingface.co/datasets/DirectionAI/EduBench | Comprehensive educational benchmark (Q&A, error correction, multi-subject) | 4,000+ contexts | Jun 2025 |
| SunriserFuture/EducationQ | https://huggingface.co/datasets/SunriserFuture/EducationQ | Balanced teaching-oriented testbed (13 disciplines x 10 difficulty levels) | 1,498 questions | Jan 2026 |
| ScaleAI/TutorBench | https://huggingface.co/datasets/ScaleAI/TutorBench | Tutoring assessment (adaptive explanations, feedback, active learning) | 1,470 samples | Oct 2025 |
| LabARSS/MMLU-Pro-education-level | https://huggingface.co/datasets/LabARSS/MMLU-Pro-education-level | MMLU Pro with education level annotations (HS/undergrad/grad/postgrad) | 11,567 rows | May 2025 |
| nanote/algebra_misconceptions | https://huggingface.co/datasets/nanote/algebra_misconceptions | 55 algebra misconceptions with 220 diagnostic examples for middle school | 1,130 rows | Dec 2024 |
| koutch/socratic_benchmark | https://huggingface.co/datasets/koutch/socratic_benchmark | Tutor-student programming interactions for Socratic dialogue evaluation | ~267 rows | Aug 2025 |
| Jennny/engagement-socratic-rated | https://huggingface.co/datasets/Jennny/engagement-socratic-rated | Rated Socratic educational engagement dialogues | 9,320 rows | Aug 2025 |

### Education Training/Fine-tuning Datasets

| Dataset | URL | Description | Size | Updated |
|---------|-----|-------------|------|---------|
| amd/InstructGpt-educational | https://huggingface.co/datasets/amd/InstructGpt-educational | Synthetic educational QA for SLM fine-tuning (LuminaSFT collection) | 851,000 rows | Feb 2026 |
| robworks-software/k12-comprehensive-educational-dataset | https://huggingface.co/datasets/robworks-software/k12-comprehensive-educational-dataset | Comprehensive K-12 dataset from 29 sources (CCSS, NGSS, NAEP, Texas education) | 7,860 rows | Feb 2026 |
| AndreiSobo/PACT-Socratic-Coding-Tutor | https://huggingface.co/datasets/AndreiSobo/PACT-Socratic-Coding-Tutor | Socratic hints for coding bugs (pedagogical fine-tuning) | 227 examples | Feb 2026 |
| ai-education/ruTeacherTalk | https://huggingface.co/datasets/ai-education/ruTeacherTalk | Russian lesson transcripts annotated with 19 teacher talk techniques | 212 transcripts | Jan 2026 |
| ushasree2001/educational-math-instruction-dataset | https://huggingface.co/datasets/ushasree2001/educational-math-instruction-dataset | Math instruction for LLM fine-tuning with step-by-step reasoning | 10K-100K | Feb 2026 |
| FreedomIntelligence/Socratic | https://huggingface.co/datasets/FreedomIntelligence/Socratic | Socratic method conversational dialogue (multi-turn Q&A) | 34,400 rows | Jun 2025 |
| sanjaypantdsd/socratic-method-conversations | https://huggingface.co/datasets/sanjaypantdsd/socratic-method-conversations | 5,000 Q&A pairs demonstrating Socratic method teaching | 5,000 pairs | Sep 2025 |
| vnovaai19/VNOVA_AI_CODING_LOGIC_TUTOR_DATASET_V1_JSONL | https://huggingface.co/datasets/vnovaai19/VNOVA_AI_CODING_LOGIC_TUTOR_DATASET_V1_JSONL | Synthetic dataset for coding tutors (100 scenarios) | 100 scenarios | Dec 2025 |
| patea4/educational-ai-agent | https://huggingface.co/datasets/patea4/educational-ai-agent | Educational AI agent training data | 190K downloads | Oct 2025 |
| neuralfoundry-coder/aihub-korean-education-instruct-sample | https://huggingface.co/datasets/neuralfoundry-coder/aihub-korean-education-instruct-sample | Korean education instruction (math, Korean, writing, tutoring) | 6,000 samples | Jan 2026 |

### Multilingual Pedagogy Datasets

| Dataset | URL | Description | Size | Updated |
|---------|-----|-------------|------|---------|
| CraneAILabs/pedagogy-benchmark-multilingual | https://huggingface.co/datasets/CraneAILabs/pedagogy-benchmark-multilingual | African language translations of pedagogy benchmark (Luganda, Nyankore) | N/A | Oct 2025 |
| CraneAILabs/pedagogy-benchmark-nyankore | https://huggingface.co/datasets/CraneAILabs/pedagogy-benchmark-nyankore | Nyankore translation of pedagogy benchmark | N/A | Oct 2025 |
| CraneAILabs/pedagogy-luganda-reviewed | https://huggingface.co/datasets/CraneAILabs/pedagogy-luganda-reviewed | Reviewed Luganda pedagogy dataset | N/A | Dec 2025 |
| FrancophonIA/Evaluation_Terms_In_Education | https://huggingface.co/datasets/FrancophonIA/Evaluation_Terms_In_Education | Multilingual education evaluation terminology (French/Arabic/English) | N/A | Mar 2025 |
| khaihoan99/VTF_EduBench_PCC_preview | https://huggingface.co/datasets/khaihoan99/VTF_EduBench_PCC_preview | Vietnamese educational translation benchmark with quality annotations | 100 rows | Nov 2025 |
| unicorn-team/Vietnamese-Education-Reasoning-Chat | https://huggingface.co/datasets/unicorn-team/Vietnamese-Education-Reasoning-Chat | Vietnamese education reasoning chat | 1K-10K | Jan 2026 |

### Student Assessment & Feedback Datasets

| Dataset | URL | Description | Size | Updated |
|---------|-----|-------------|------|---------|
| tasksource/AES2-essay-scoring | https://huggingface.co/datasets/tasksource/AES2-essay-scoring | Automated essay scoring dataset | 17.3K downloads | Jun 2024 |
| DysfunctionalHuman/essay-scoring | https://huggingface.co/datasets/DysfunctionalHuman/essay-scoring | Essay scoring dataset | 17.3K downloads | Jun 2024 |
| jatinmehra/Automated-Essay-Scoring-2.0 | https://huggingface.co/datasets/jatinmehra/Automated-Essay-Scoring-2.0 | Automated Essay Scoring 2.0 | 17.3K downloads | Dec 2024 |
| abdlh/Dataset_Automatic_Essay_Scoring_Essay-EssayScore_and_24_textual_features | https://huggingface.co/datasets/abdlh/Dataset_Automatic_Essay_Scoring_Essay-EssayScore_and_24_textual_features | Auto essay scoring with 24 textual features | 13K downloads | Dec 2024 |
| NLPC-UOM/Student_feedback_analysis_dataset | https://huggingface.co/datasets/NLPC-UOM/Student_feedback_analysis_dataset | Student feedback analysis | 54 downloads | Mar 2025 |
| electricsheepafrica/nigeria-education-instructional-evaluation | https://huggingface.co/datasets/electricsheepafrica/nigeria-education-instructional-evaluation | Teacher instructional quality evaluations (Nigeria, 100K records) | 100,000 rows | Oct 2025 |
| electricsheepafrica/nigeria-education-learning-outcomes-mapping | https://huggingface.co/datasets/electricsheepafrica/nigeria-education-learning-outcomes-mapping | Curriculum learning outcomes mapped to Bloom's taxonomy | 100,000 rows | Oct 2025 |
| burtenshaw/exam_questions | https://huggingface.co/datasets/burtenshaw/exam_questions | Exam questions dataset | 22 likes | Jan 2025 |
| zipu-w/AP-exam-questions | https://huggingface.co/datasets/zipu-w/AP-exam-questions | AP exam questions | 533 downloads | Sep 2025 |
| zipu-w/alevel-exam-questions | https://huggingface.co/datasets/zipu-w/alevel-exam-questions | A-level exam questions | 480 downloads | Sep 2025 |
| aravdhoot/llm-domain-shift-education | https://huggingface.co/datasets/aravdhoot/llm-domain-shift-education | LLM domain shift in education | 9,270 rows | Oct 2025 |

### Exam & Science Assessment Datasets

| Dataset | URL | Description | Size | Updated |
|---------|-----|-------------|------|---------|
| dry-melon/Chinese-middle-school-English-exam-questions | https://huggingface.co/datasets/dry-melon/Chinese-middle-school-English-exam-questions | Chinese middle school English exam questions | 106K downloads | Apr 2025 |
| HolySaint/MBE-exam-questions | https://huggingface.co/datasets/HolySaint/MBE-exam-questions | Multistate Bar Examination questions | N/A | Apr 2025 |
| NYCU-312555007/ZH-TW_Reading_Comprehension_Test_for_LLMs | https://huggingface.co/datasets/NYCU-312555007/ZH-TW_Reading_Comprehension_Test_for_LLMs | Chinese reading comprehension test for LLMs | 14.5K downloads | May 2024 |
| Tutoruslabs/GSM8K_KOR | https://huggingface.co/datasets/Tutoruslabs/GSM8K_KOR | Korean GSM8K math evaluation | 569 test samples | Dec 2025 |
| Tutoruslabs/ELEMENTARY_MATH | https://huggingface.co/datasets/Tutoruslabs/ELEMENTARY_MATH | Elementary school multimodal math | 448 questions | Nov 2025 |
| Tutoruslabs/KMMR-VisMath | https://huggingface.co/datasets/Tutoruslabs/KMMR-VisMath | Korean multimodal math reasoning | 2,055 problems | Nov 2025 |

### Synthetic Tutor Response Datasets

| Dataset | URL | Description | Size | Updated |
|---------|-----|-------------|------|---------|
| HueyKolowich/synthetic-tutor-responses-labeled-v1 | https://huggingface.co/datasets/HueyKolowich/synthetic-tutor-responses-labeled-v1 | Labeled synthetic tutor responses | N/A | Dec 2025 |
| HueyKolowich/synthetic-tutor-responses-labeled-embeddings-deberta-triplet-v2 | https://huggingface.co/datasets/HueyKolowich/synthetic-tutor-responses-labeled-embeddings-deberta-triplet-v2 | Tutor responses with DeBERTa embeddings | N/A | Dec 2025 |

### Other Relevant Education Datasets

| Dataset | URL | Description | Size | Updated |
|---------|-----|-------------|------|---------|
| iioos/education-explanations | https://huggingface.co/datasets/iioos/education-explanations | Topic-based explanations labeled by difficulty level | N/A | Dec 2025 |
| Georgiy1108/programming-tutor-ru | https://huggingface.co/datasets/Georgiy1108/programming-tutor-ru | Russian programming tutor (LeetCode/Codeforces) | N/A | Nov 2025 |
| MCP-1st-Birthday/smoltrace-education-tasks | https://huggingface.co/datasets/MCP-1st-Birthday/smoltrace-education-tasks | 80 education tasks in SMOLTRACE evaluation format | 80 tasks | Nov 2025 |
| hhhzzf/Socratic-geo | https://huggingface.co/datasets/hhhzzf/Socratic-geo | Geometry-focused Socratic dataset (multimodal) | 100K-1M | Dec 2025 |
| Ben-45/nigerian_education_continuous_assessment | https://huggingface.co/datasets/Ben-45/nigerian_education_continuous_assessment | Continuous assessment (mid-term/end-of-term CA scores) | 600,000 rows | Jan 2026 |
| uma-siddareddy/phi2-block-to-text-python-education-dataset | https://huggingface.co/datasets/uma-siddareddy/phi2-block-to-text-python-education-dataset | Block-to-text Python coding education | N/A | Feb 2026 |
| brhkim/education_data_portal_mirror | https://huggingface.co/datasets/brhkim/education_data_portal_mirror | Complete mirror of Urban Institute Education Data Portal | 1B-10B rows | Feb 2026 |

---

## PART 3: ADDITIONAL RELEVANT PAPERS (Education + AI)

| Paper | HF URL | Date | Focus |
|-------|--------|------|-------|
| Generative AI for Programming Education: Benchmarking ChatGPT, GPT-4, and Human Tutors | /papers/2306.17156 | Jun 2023 | Compares LLMs with human tutors on Python programming |
| Evaluating LLMs on the GMAT: Implications for Business Education | /papers/2401.02985 | Jan 2024 | GPT-4 Turbo surpasses average GMAT scores |
| CodeAid: Evaluating an LLM-based Programming Assistant | /papers/2401.11314 | Jan 2024 | 700 students, 8,000 usages of LLM-based coding assistant |
| Can Language Models Evaluate Human Written Text? (Korean Student Writing) | /papers/2407.17022 | Jul 2024 | GPT-4-Turbo reliably assesses grammaticality/fluency |
| Large Language Models in Student Assessment: Comparing ChatGPT and Human Graders | /papers/2406.16510 | Jun 2024 | GPT-4 grading of master-level essays |
| Is ChatGPT a Good Teacher Coach? | /papers/2306.03090 | Jun 2023 | Evaluates ChatGPT as automated teacher coach |
| Using Generative AI and Multi-Agents for Automatic Feedback (AutoFeedback) | /papers/2411.07407 | Nov 2024 | Multi-agent system reducing over-praise in student feedback |
| Evaluating GPT-4 at Grading Handwritten Solutions in Math Exams | /papers/2411.05231 | Nov 2024 | GPT-4o multimodal grading of handwritten math |
| Automated Assessment of Students' Code Comprehension using LLMs | /papers/2401.05399 | Dec 2023 | LLMs for assessing student programming explanations |
| Enhanced Classroom Dialogue Sequences Analysis with Hybrid AI Agent | /papers/2411.08418 | Nov 2024 | AI agent for classroom dialogue analysis |
| Distilling ChatGPT for Explainable Automated Student Answer Assessment | /papers/2305.12962 | May 2023 | Framework improving QWK score 11% |
| AI-Driven Virtual Teacher (VATE) | /papers/2409.09403 | Sep 2024 | LLM math error analysis on Squirrel AI platform |
| Automatic Legal Writing Evaluation (OAB-bench) | /papers/2504.21202 | Apr 2025 | 105 Brazilian Bar Exam questions for LLM legal writing |
| RECIPE4U: Student-ChatGPT Interaction Dataset in EFL Writing | /papers/2403.08272 | Mar 2024 | 212 EFL students' ChatGPT interactions for essay revision |
| AI-University: LLM-based Platform for Instructional Alignment | /papers/2504.08846 | Apr 2025 | Fine-tuning LLMs with RAG for course-specific responses |
| Automatic Large Language Models Creation of Interactive Learning Lessons | /papers/2506.17356 | Jun 2025 | GPT-4o tutor training lessons with RAG |
| Can LLMs Design Good Questions Based on Context? | /papers/2501.03491 | Jan 2025 | Evaluates LLM-generated questions vs human questions |
| EdNet: A Large-Scale Hierarchical Dataset in Education | /papers/1912.03072 | Dec 2019 | 131M+ interactions from 784K students |
| Graphusion: KG for NLP Education (TutorQA) | /papers/2407.10794 | Jul 2024 | TutorQA benchmark with 1,200 QA pairs |
| Instruction Tuning with Human Curriculum (Bloom's Taxonomy) | /papers/2310.09518 | Oct 2023 | Structured synthetic dataset using Bloom's taxonomy |
| BAREC: Arabic Readability Assessment | /papers/2502.13520 | Feb 2025 | 69,441 sentences across 19 readability levels |
| Scalable Math Problem Solving Strategy Prediction | /papers/2308.03892 | Aug 2023 | MATHia dataset with predictive equality |
| StuGPTViz: Visualizing Student-ChatGPT Interactions | /papers/2407.12423 | Jul 2024 | 48 students' ChatGPT interaction patterns |
| ArguGPT: Evaluating Argumentative Essays | /papers/2304.07666 | Apr 2023 | 4,038 essays from 7 GPT models vs human essays |
| Multimodal Lecture Presentations Dataset | /papers/2208.08080 | Aug 2022 | 180+ hours video and 9000+ slides |
| Which LLM should I use? (CS Students) | /papers/2402.01687 | Jan 2024 | LLM evaluation for CS student tasks |
| ECBD: Evidence-Centered Benchmark Design for NLP | /papers/2406.08723 | Jun 2024 | Framework from educational assessment for NLP benchmarks |
| Humanity's Last Exam | /papers/2501.14249 | Jan 2025 | 3,000 multi-modal frontier academic questions |
| Fluid Language Model Benchmarking | /papers/2509.11106 | Sep 2025 | Adaptive testing inspired by psychometrics |
| CITING: LLMs Create Curriculum for Instruction Tuning | /papers/2310.02527 | Oct 2023 | Teacher LLM creates rubrics for student LLM |
| ScholarBench: Bilingual Academic Benchmark | /papers/2505.16566 | May 2025 | English-Korean academic reasoning evaluation |

---

## SUMMARY STATISTICS

- **Total unique papers found**: 60+
- **Total unique datasets found**: 50+
- **Key education-specific benchmarks**: ~15 purpose-built benchmarks
- **Date range**: 2019-2026 (focus on 2024-2026)
- **Most impactful benchmarks for education AI**:
  1. MathTutorBench (pedagogical quality + reward model)
  2. TutorBench (Scale AI, multimodal tutoring assessment)
  3. Pedagogy Benchmark (teacher knowledge evaluation)
  4. EduBench (comprehensive educational scenarios)
  5. EducationQ (balanced teaching testbed, ACL 2025)
  6. ELMES (automated educational evaluation framework)
  7. LearnLM (pedagogical instruction following)
  8. VisScience (K12 multimodal science reasoning)
  9. SAS-Bench (short answer scoring)
  10. EduAlign/HPC-RM (pedagogical alignment reward model)
