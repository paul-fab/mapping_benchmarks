# Benchmark Development and General LLM Evaluation in K-12 Education

## Executive Summary

The rapid integration of large language models (LLMs) into educational settings has prompted a growing body of research focussed on building benchmarks — structured evaluation tools — to assess whether these models can genuinely support K-12 learning. Our analysis of **30 papers** in this area reveals a field that is maturing in its approach to benchmark construction but confronting a fundamental and uncomfortable finding: **LLMs frequently achieve high accuracy on standard educational assessments through shallow pattern matching rather than genuine reasoning**. Multiple studies demonstrate that small perturbations to questions — changing a number, rewording a phrase, inserting a distractor — can cause accuracy drops of **up to 40%**, while human student performance remains stable under the same conditions.

The benchmarks in this collection span an impressive range of dimensions, including grade-level progression from elementary through high school, cross-linguistic evaluation across languages such as Chinese, Vietnamese, Indonesian, and Bangla, and multimodal integration requiring reasoning over diagrams and images alongside text. Notable contributions include MDK12-Bench, which provides **141,000 real-world K-12 exam questions** across six disciplines, and GSM-PLUS, which systematically exposes the brittleness of mathematical reasoning in models that were leading at the time of evaluation. Visual reasoning emerges as a particularly critical weakness — even for advanced multimodal models, diagram misinterpretation accounts for **more than 50% of errors** in some evaluations.

However, the field remains heavily focussed on measuring answer correctness rather than the quality of reasoning processes, the pedagogical value of explanations, or the impact on genuine student learning. Only three papers in this collection include step-by-step process evaluation. This means that current benchmarks — whilst valuable for comparing model capabilities — tell us relatively little about whether AI-EdTech tools built on these models will actually improve learning outcomes in classrooms, particularly in low- and middle-income countries (LMICs) where educational contexts, languages, and cultural knowledge differ markedly from the training data these models have absorbed.

## Key Themes

### Mathematical reasoning is robust on the surface but brittle underneath

The largest cluster of papers in this collection — **10 studies** — focusses on evaluating the mathematical reasoning capabilities of LLMs, and the findings are sobering. The widely used **GSM8K benchmark**, which contains 8,500 grade school maths word problems requiring multi-step reasoning, has become something of a gold standard for cross-study comparison. Yet multiple papers now demonstrate that this benchmark has become saturated — models achieve impressively high scores that may partly reflect training data leakage rather than genuine mathematical understanding.

GSM-PLUS addresses this directly by applying eight types of systematic perturbations to GSM8K questions, including numerical substitutions, arithmetic complexity changes, distractor insertion, and critical thinking modifications. The results reveal that models which appear highly capable on the original benchmark suffer dramatic accuracy drops — **up to 40%** — when questions are only slightly altered, whilst human performance remains stable. The SVAMP benchmark was among the first to expose this phenomenon at the elementary level, showing that models could achieve high accuracy without meaningfully processing the question text or word order. A Careful Examination of Large Language Model Performance on Grade School Arithmetic reinforced these findings, demonstrating that even models considered leading at the time of study exhibited shallow heuristic-based solving strategies. FineMath contributed a fine-grained Chinese-language perspective, revealing that mathematical struggles persist regardless of the language in which problems are presented.

This theme carries significant implications for education stakeholders. If AI-EdTech tools built on these models are deployed for mathematics tutoring or assessment in LMIC classrooms, their apparent competence may mask a fundamental inability to handle the natural variation that real students produce in their questions and problem formulations.

### Visual reasoning remains a critical weakness for multimodal models

Nine papers in the collection evaluate **multimodal mathematical and scientific reasoning** — the ability to integrate information from diagrams, graphs, geometric figures, and images with textual problem content. This is particularly relevant for K-12 education, where visual representations are central to how mathematics and science are taught. The findings are consistent and concerning: visual interpretation remains a major weakness even for the most advanced models evaluated.

**VisioMath** takes an innovative approach by presenting problems where all answer options are visually similar diagrams, forcing models to engage in fine-grained comparative visual reasoning. The benchmark exposes critical image-text misalignment failures, with models frequently resorting to positional heuristics — selecting answers based on their position rather than their content. **MM-MATH**, one of the few benchmarks to incorporate systematic process evaluation, identifies diagram misinterpretation as the dominant error type, accounting for **more than 50% of all errors** in its evaluation of middle school maths problems. MDK12-Bench and VisScience extend these findings across multiple disciplines, confirming that visual reasoning challenges are not limited to mathematics but affect science subjects broadly.

### Multilingual and cross-cultural evaluation reveals significant disparities

Eight papers address the critical question of how LLMs perform across different languages and cultural contexts — a question of central importance for LMIC applications. **E-EVAL**, the first comprehensive Chinese K-12 benchmark, reveals an important finding: Chinese-dominant models outperform English-dominant models (including GPT-4, which was the leading commercial model at the time of these studies) on Chinese educational content. This suggests that **language-specific training data matters enormously** for educational applications.

The **EXAMS** benchmark provides cross-lingual evaluation using authentic high school examination questions from multiple countries, whilst **IndoMMLU** and **VNHSGE** offer focused evaluations for Indonesian and Vietnamese educational contexts respectively. **BanglaMATH** addresses mathematical reasoning in Bangla, a language spoken by over 230 million people yet severely underrepresented in LLM training data. A recurring finding across these papers is that models may demonstrate reasonable language proficiency whilst failing on region-specific cultural knowledge — a gap that could significantly undermine the usefulness of AI-EdTech tools in diverse LMIC contexts where local curricula reflect particular cultural, historical, and geographical content.

### Student voices are largely absent — but illuminating when included

A small but significant cluster of **three papers** involves K-12 students directly in the evaluation and design of AI systems. The Participatory Design of GenAI with High School Students study is a rare and valuable example of including young people as co-designers. Its findings challenge adult assumptions: **students prioritise system-level solutions** — such as built-in citations, bias mitigation, and transparency features — over user education approaches that place the burden of responsible use on individual learners. Learning About Algorithm Auditing in Five Steps and Not Just Training, Also Testing further demonstrate that young people can engage meaningfully with questions of AI evaluation, fairness, and accountability when given appropriate frameworks. These studies represent a methodological direction that the field should pursue far more actively.

### Educational assessment validity and AI detection

Two papers examine the policy dimensions of AI in educational assessment. Research on AI-generated student essay detection reveals the difficulty of reliably identifying AI-authored work — an **adversarial evaluation** demonstrates that current detection tools can be readily circumvented. This raises fundamental questions about how educational assessment must evolve in an era of readily accessible generative AI, particularly in contexts where assessment infrastructure is already under-resourced.

## What Is Being Measured

The benchmarks in this collection evaluate a broad range of capabilities, though with notable concentrations. **Answer correctness** across multiple-choice and open-ended questions at various grade levels forms the baseline measure for nearly all studies. Mathematical reasoning — spanning arithmetic, algebra, geometry, and word problem solving — is the most heavily evaluated domain.

Beyond simple accuracy, several benchmarks measure **robustness to perturbation**, testing whether models maintain performance when questions are subtly altered. **Cross-linguistic performance** is evaluated by comparing accuracy across languages including English, Chinese, Vietnamese, Indonesian, and Bangla. **Multimodal integration** — the ability to reason jointly over text, diagrams, graphs, and scientific symbols — features prominently. Fine-grained measures include **knowledge point mastery** (whether models demonstrate specific conceptual competencies), **performance by difficulty level** and grade progression, and response characteristics across different prompting strategies such as Chain-of-Thought and self-consistency approaches. Several studies establish **human baselines** using student performance data, enabling relative comparisons between model and student capabilities.

## Critical Gaps

What is not being measured is arguably more important than what is. The field's overwhelming focus on answer correctness leaves enormous gaps in our understanding of whether AI-EdTech tools can genuinely support learning.

**Process evaluation** — assessing the quality and correctness of intermediate reasoning steps — features in only **three of 30 papers**. This means we have limited insight into whether models arrive at correct answers through sound reasoning or lucky shortcuts. **Explanation quality** from a pedagogical perspective is almost entirely unmeasured: we do not know whether model-generated explanations actually help students understand concepts.

Perhaps most critically for education stakeholders, there is virtually no measurement of **learning transfer** (whether solving one problem with AI assistance helps with related problems), **long-term retention**, or **productive struggle** (the educationally valuable experience of persisting through difficulty). The impact on **student motivation, confidence, and attitudes** toward learning remains unexamined, as do **social and collaborative dimensions** of learning.

**Equity considerations** represent another significant gap. There is minimal evaluation of how these tools perform for students with varying prior knowledge levels, disabilities, or language backgrounds — precisely the populations that stand to benefit most, or be most harmed, by AI-EdTech deployment. **Teacher integration** — how effectively educators can use benchmark insights for formative assessment and instructional design — is similarly absent.

## Notable Benchmarks and Datasets

**GSM-PLUS** stands out for its systematic approach to robustness evaluation, applying eight perturbation types to the widely used GSM8K benchmark and revealing accuracy drops of up to 40%. This benchmark should be considered essential reading for anyone deploying mathematical AI-EdTech tools.

**MDK12-Bench** is the largest and most comprehensive multimodal K-12 benchmark currently available, with **141,000 real-world exam questions** across six disciplines, annotated with 6,225 structured knowledge points. Its dynamic evaluation framework — designed to prevent data contamination through test-time transformations — represents a methodological advance that other benchmarks should emulate.

**SVAMP** was pioneering in demonstrating that elementary maths models could achieve high accuracy without meaningfully processing question content, whilst **VisioMath** exposes critical visual reasoning failures through its innovative design requiring fine-grained diagram comparison. **MM-MATH**, with its 5,929 open-ended middle school problems and systematic process evaluation, provides one of the few windows into reasoning quality rather than just outcome accuracy. **E-EVAL** remains the foundational Chinese K-12 benchmark, and **GSM8K** — despite concerns about saturation and data leakage — continues to serve as the field's most widely adopted mathematical reasoning evaluation tool.

## Methodological Trends

The field demonstrates increasing sophistication in benchmark construction. The dominant approach involves building benchmarks from **authentic educational materials** — real exam papers, textbooks, and workbooks — rather than synthetic generation, lending ecological validity to evaluations. Multi-dimensional annotation has become standard practice, with benchmarks tagging questions by difficulty level, knowledge points, grade level, subject area, and solution pathway.

**Adversarial and robustness testing** through systematic perturbation represents a particularly valuable methodological advance, moving beyond static accuracy measurement. Evaluation typically employs zero-shot and few-shot prompting across multiple model families, both proprietary and open-source. The comparison of prompting techniques — Chain-of-Thought, self-consistency, programme generation — across benchmarks provides insight into how different interaction strategies affect performance.

An emerging but still limited trend is the use of **LLM-as-judge** approaches, where models such as GPT-4 are used to evaluate reasoning chains produced by other models. Whilst pragmatic, this approach introduces its own biases and limitations. **Participatory design methods** involving students represent a small but important methodological direction. Dynamic evaluation frameworks that prevent memorisation through test-time transformations address the growing concern about benchmark contamination — a concern that is only likely to intensify as models are trained on ever-larger internet corpora.

## Recommendations

We recommend that funders and development partners investing in AI-EdTech for LMICs prioritise the following actions:

The field should **adopt robustness testing as standard practice** rather than relying on static benchmark accuracy, which significantly overestimates true reasoning capabilities. Any AI-EdTech tool claiming mathematical or scientific reasoning capability should be evaluated under perturbation conditions *(by end of 2026)*.

We recommend **substantial investment in process evaluation methodologies** — assessing the quality of reasoning steps, not just final answers. With only three of 30 papers incorporating step-by-step evaluation, this represents the single largest methodological gap in the field.

Development partners should fund the creation of **authentic multilingual benchmarks built from local educational materials** rather than translations of English-language assessments. Translation introduces noise and — critically — fails to capture region-specific knowledge, cultural contexts, and curricular priorities that are essential for LMIC deployment *(ongoing)*.

We recommend that **K-12 students be involved as co-designers** in benchmark development and AI policy formation through participatory design methods. The existing evidence demonstrates that young people's priorities — including system-level accountability and transparency — differ meaningfully from adult assumptions.

The field should develop benchmarks that measure **pedagogically relevant dimensions** — explanation quality, learning transfer, productive struggle, metacognitive awareness — alongside technical accuracy. Current benchmarks tell us whether models can answer questions correctly but not whether they can support genuine learning.

Finally, we recommend establishing **careful human baselines** using grade-appropriate student populations under proper test-taking conditions, rather than comparing models to experts or averaged populations. This is essential for making meaningful claims about model readiness for classroom deployment *(by mid-2027)*.

## Key Papers

- **GSM-PLUS: A Comprehensive Benchmark for Evaluating the Robustness of LLMs as Mathematical Problem Solvers** — Systematically demonstrates that small perturbations cause accuracy drops of up to 40%, revealing brittleness in mathematical reasoning despite high benchmark performance. Essential reading for anyone evaluating maths-focussed AI-EdTech.

- **MDK12-Bench: A Comprehensive Evaluation of Multimodal Large Language Models on Multidisciplinary Exams** — The largest and most comprehensive multimodal K-12 benchmark available, with 141,000 questions, a structured knowledge taxonomy, and a dynamic evaluation framework designed to prevent data contamination.

- **Are NLP Models Really Able to Solve Simple Math Word Problems? (SVAMP)** — Pioneering work demonstrating that models solve problems without meaningfully processing question content or word order, establishing the adversarial evaluation paradigm for mathematical reasoning.

- **VisioMath: Benchmarking Figure-based Mathematical Reasoning in LMMs** — Reveals critical image-text misalignment failures in multimodal models through innovative visual option similarity testing, with direct implications for STEM education tools.

- **Participatory Design of GenAI with High School Students** — A rare and valuable example of involving young people in AI tool and policy design, revealing their priorities for system-level solutions over individual user education.

- **E-EVAL: A Comprehensive Chinese K-12 Education Evaluation Benchmark** — The first comprehensive Chinese K-12 benchmark, demonstrating language-specific model advantages whilst revealing universal struggles with mathematics across all models evaluated.

- **MM-MATH: Advancing Multimodal Math Evaluation with Process Evaluation and Fine-grained Classification** — One of only three papers incorporating systematic process evaluation, identifying diagram misinterpretation as the dominant error type accounting for more than 50% of failures.