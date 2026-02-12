# AI Tutors: Benchmarking Personalised Learning Systems in K-12 Education

## Executive Summary

AI tutors represent one of the most mature and actively researched areas in educational AI — and one of the most contested. Our analysis covers **348 papers** spanning intelligent tutoring systems (ITS), large language model (LLM)-powered conversational tutors, and adaptive learning platforms, primarily targeting K-12 mathematics and STEM education. The field demonstrates impressive technical progress: systems like ASSISTments, Reasoning Mind Genie 2, and newer LLM-based platforms such as Khanmigo and Duolingo Max can now deliver fluent, personalised instruction at scale. A rigorous randomised controlled trial (RCT) in UK classrooms found human-supervised AI tutoring achieved **comparable efficacy to human tutors**, with knowledge transfer rates of **66.2% versus 60.7%** for human instruction.

Yet beneath this progress lies a fundamental tension. Research consistently reveals that AI tutors — particularly those powered by LLMs — risk undermining the very learning they are designed to support. Studies show that students with unrestricted ChatGPT access scored **17% lower on independent tests** despite solving **48% more practice problems**. One large-scale study found cognitive engagement scores were significantly lower (mean **2.95/5**) for ChatGPT users compared with controls (**4.19/5**). The field's most authoritative benchmark, TutorBench, demonstrates that no frontier LLM exceeds **56% overall performance** on core tutoring skills. These findings point to a critical gap between what AI tutors can do technically and what they achieve pedagogically.

The methodological landscape is shifting rapidly — from rule-based systems toward LLM-powered approaches, and from evaluating answer correctness toward assessing the quality of the tutoring process itself. However, the vast majority of studies measure immediate post-test performance rather than long-term retention, transfer, or metacognitive development. For funders and policymakers in low- and middle-income countries (LMICs), this evidence base demands careful interpretation: AI tutors hold genuine promise for scaling personalised instruction, but deployment without pedagogical safeguards risks creating what researchers have termed a **"Zone of No Development"** — where permanent AI scaffolding replaces, rather than supports, cognitive growth.

## Key Themes

### Pedagogical Quality: The Gap Between Fluency and Sound Teaching

A dominant concern across **18 papers** is whether AI tutors follow sound pedagogical principles — or merely generate plausible-sounding responses. The GuideEval benchmark, introduced in *Discerning minds or generic tutors?*, evaluates LLMs across three phases: **Perception** (inferring learner states), **Orchestration** (adapting strategies), and **Elicitation** (stimulating productive reflections). Results reveal that while LLMs can generate reasonable questions, they fail at the dynamic adaptation that defines expert human tutoring. The MRBench taxonomy, developed through the *Unifying AI Tutor Evaluation* paper, consolidates eight pedagogical dimensions — including mistake identification, guidance provision, and feedback actionability — and finds that LLMs frequently **reveal answers prematurely**, with leak rates between **25.66% and 91.40%** depending on configuration. EduGuardBench goes further, simultaneously testing **pedagogical fidelity and adversarial safety**, uncovering harmful teaching behaviours even in reasoning-optimised models. This means that scaling AI tutors without addressing pedagogical alignment could actively harm learning quality, particularly for younger students who lack the metacognitive skills to compensate for poor tutoring strategies.

### Learning Outcomes: Promising but Incomplete Evidence

Approximately **15 papers** present rigorous empirical evaluations of student learning gains through classroom experiments and RCTs. The UK classroom RCT (*AI tutoring can safely and effectively support students*) provides some of the strongest evidence for safe deployment, while Reasoning Mind Genie 2 demonstrated deployment at scale with **67,000 students** and effect sizes exceeding **d > 1** for cross-cultural curriculum transfer. A large-scale RCT with 265 students (*Improved Performances and Motivation in Intelligent Tutoring Systems*) revealed that learning progress-based personalisation improves both outcomes and motivation — but that offering choice within linear curricula actually **harmed learning** due to attentional distraction. Meta-analyses across the field suggest step-based ITS systems approach human tutor effectiveness, with effect sizes typically between **d = 0.4 and d = 0.8**, though they do not consistently exceed it.

### The Rise — and Risks — of LLM-Powered Tutoring

The most significant methodological shift in this field is the transition from rule-based systems to **LLM-powered conversational tutors**, with **28 papers** focussed specifically on this area. Systems built on models available during 2023–2024 — including GPT-4, GPT-3.5, and LLaMA variants — demonstrate natural language fluency far exceeding earlier approaches. The paper *Beyond Final Answers* reveals the core challenge: LLMs achieve **85.5% correct answers** but only **56.6% error-free dialogues**, highlighting the critical gap between answer accuracy and tutoring quality. TeachLM demonstrates that fine-tuning on **100,000 hours** of real tutoring data significantly improves pedagogical quality compared with prompt engineering alone, suggesting that raw language capability is insufficient without grounding in authentic teaching practice. AutoTutor's hybrid approach — combining finite state transducers for pedagogical control with LLM flexibility — illustrates that **structured teaching strategies remain essential** even as the underlying technology becomes more capable. Given the pace of model development, findings based on GPT-4-era models may need re-evaluation with current-generation systems, though the fundamental pedagogical challenges are likely to persist.

### Knowledge Tracing and Student Modelling

The ability to track and model student knowledge over time remains central to effective tutoring, addressed across **12 papers** on knowledge tracing specifically. The field has evolved from Bayesian Knowledge Tracing (BKT) to Deep Knowledge Tracing (DKT) and transformer-based architectures — with *Deep Knowledge Tracing with Transformers* achieving approximately **10% AUC improvement** over prior methods. However, *Problems With Large Language Models for Learner Modelling* provides comprehensive empirical evidence that LLMs fail at fundamental knowledge tracing tasks despite fine-tuning. This argues strongly for **hybrid architectures** combining specialised sequential models for student modelling with LLM generative capabilities for dialogue — a design principle with significant implications for system architecture in LMIC deployments where computational resources may be constrained.

### Safety and Child-Appropriate Design

A smaller but critical cluster of **6 papers** addresses safety specifically for K-12 contexts. Safe-Child-LLM, MinorBench, and SproutBench each develop benchmarks for evaluating age-appropriate responses, harmful content detection, and developmental appropriateness. MinorBench, grounded in a real-world case study of middle-school ChatGPT usage, systematically evaluates child safety through a taxonomy of content-based risks specific to minors — moving beyond adult-centric safety measures. For LMIC contexts, where regulatory frameworks for child-facing AI may be less developed, these benchmarks offer essential starting points for quality assurance.

### Cross-Cultural and Multilingual Dimensions

Research examining AI tutors across languages and cultural contexts — though represented by only **5 papers** — reveals **systematic biases**, with English consistently outperforming other languages in both content quality and pedagogical effectiveness. *Investigating Bias: A Multilingual Pipeline* documents how mathematical problem-solving quality degrades in non-English languages. This is a critical finding for LMIC deployment, where instruction often occurs in languages underrepresented in LLM training data.

## What Is Being Measured

The field has developed a rich — if uneven — measurement ecosystem. The most common metrics include **learning gains** via pre-post test scores (with effect sizes typically reported as Cohen's d between 0.3 and 0.8), **knowledge tracing accuracy** (AUC, RMSE), and **prediction accuracy** for student performance. Pedagogical quality is increasingly assessed through expert-annotated rubrics covering Socratic questioning, scaffolding appropriateness, mistake identification, and feedback actionability. Dialogue quality metrics include BLEU, BERTScore, turn-taking balance, and coherence measures.

Student engagement is captured through behavioural proxies — time-on-task, problem completion rates, hint requests — and through validated instruments such as the ARCS motivation model, the Intrinsic Motivation Inventory (IMI), and the Technology Acceptance Model (TAM). Hallucination rates and factual accuracy are measured in LLM-based systems, though inconsistently. Notably, the BEA 2025 Shared Task established community-wide evaluation protocols across five tracks, with **50+ international teams** participating — yet the best systems achieved only **58–70% macro F1**, indicating substantial room for improvement.

## Critical Gaps

The most consequential gap is the near-total absence of **long-term retention studies**. The vast majority of evaluations measure learning immediately after intervention, with few extending beyond one to two weeks. We found virtually no studies tracking outcomes at six months or beyond — meaning the field cannot yet answer the fundamental question of whether AI-tutored learning persists.

Equally concerning is the lack of measurement of **metacognitive skill development**. While several papers identify metacognitive laziness as a risk, almost none measure whether students develop self-regulation, planning, or monitoring capabilities through AI tutoring. Closely related is the absence of metrics for **productive struggle** — whether students develop persistence, resilience, and the ability to work through difficulty independently.

**Equity-focussed deployment studies** represent another significant gap. Systematic measurement of differential effects across socioeconomic status, prior achievement levels, and learning disabilities is rare. For LMIC contexts, this gap is particularly acute — the assumption that systems effective for well-resourced English-speaking students will transfer equitably to diverse populations remains largely untested.

**Cost-effectiveness analyses** are almost entirely absent. No rigorous comparative studies examine AI tutoring costs against alternatives such as peer tutoring, small-group instruction, or teacher professional development at equivalent scale. For development funders making investment decisions, this represents a critical evidence gap.

Finally, the field lacks studies on **teacher integration and professional development**. How teachers adapt their practice when AI tutors are introduced, what training they need, and how classroom dynamics shift remain underexplored — yet these factors are likely decisive for real-world deployment success.

## Cognitive Offloading: The Field's Central Challenge

Cognitive offloading — the tendency for students to delegate thinking to AI rather than engage in genuine learning — emerges as arguably the most important finding across this entire research area. A remarkable **62 papers** address this concern, with convergent evidence that unrestricted AI tutor access reduces deep cognitive engagement even as it improves surface-level task performance.

The evidence is striking. An experimental study found that **52.1% of students adopted incorrect ChatGPT suggestions** despite receiving AI literacy interventions, indicating that brief educational programmes are insufficient to combat over-reliance. Students using ChatGPT for essay writing showed **reduced neural connectivity and cognitive engagement** compared with unassisted approaches, as measured by EEG. In one Turkish high school field experiment, students with unrestricted ChatGPT access completed **48% more practice problems** yet scored **17% lower** on independent assessments — a finding that crystallises the paradox at the heart of AI tutoring.

The theoretical framework of the **"Zone of No Development"** — introduced in *The Unspoken Crisis of Learning* — argues that permanent AI scaffolding replaces cognitive development rather than supporting it, inverting Vygotsky's Zone of Proximal Development. Students develop what researchers term **"metacognitive laziness"**, with reduced reflection, diminished need for understanding, and lower critical thinking despite improved task performance. After experiencing hallucinations, students developed **"epistemic safeguarding"** — restricting AI use only to domains where they could verify answers — suggesting some self-protective adaptation, but one that limits AI's educational potential.

Several papers propose mitigation strategies. The **"Extraheric AI"** framework redesigns AI interaction so that the system poses questions rather than provides answers, fostering germane cognitive load. MetaCLASS introduces an **interpretable 11-move framework** for metacognitive coaching with explicit productive restraint. The architecture of **"enhanced cognitive scaffolding"** proposes progressive autonomy where AI support fades as competence grows. MusicScaffold demonstrates AI tutor design that prevents cognitive offloading through explicit error detection and multi-role scaffolding. However, these remain largely experimental — the field has identified the problem far more thoroughly than it has solved it.

For LMIC deployment, these findings carry particular weight. Where teacher oversight may be limited and students may have fewer alternative learning supports, the risk that AI tutors create dependency rather than capability is especially acute.

## Notable Benchmarks and Datasets

Several benchmarks stand out for their relevance to quality assurance in educational AI. **TutorBench** provides 1,490 expert-curated samples with sample-specific rubrics for evaluating explanations, feedback, and hints — and its finding that no frontier model exceeds 56% overall performance establishes a sobering baseline. **GuideEval** is the first benchmark to evaluate dynamic adaptation to student cognitive states rather than generic response generation. **EduGuardBench** uniquely combines pedagogical fidelity and adversarial safety assessment, testing both teaching competence and resistance to jailbreaking.

For student modelling, **FoundationalASSIST** provides **1.7 million K-12 interactions** with complete question text and actual student responses aligned to Common Core standards — the first dataset enabling genuine LLM research in cognitive student modelling. The **ASSISTments datasets** (2009, 2012, 2017) remain the most widely used benchmarks for knowledge tracing, enabling cross-study comparisons. **ES-KT-24** offers the first multimodal knowledge tracing dataset combining video, text, and interaction logs from educational games.

For safety evaluation, **MinorBench** and **Safe-Child-LLM** provide child-specific risk taxonomies that go beyond adult-centric safety measures — essential resources for anyone deploying AI tutors with children in any context.

## Methodological Trends

The field shows a clear evolution across several dimensions. **Randomised controlled trials** in authentic classroom settings — with sample sizes from 50 to over 2,000 students — are increasingly common, moving beyond lab studies. Mixed-methods approaches combining quantitative learning outcomes with qualitative interviews and think-aloud protocols provide richer understanding of learning processes.

**LLM-as-a-judge** evaluation is emerging as a scalable alternative to expensive human expert annotation, though its limitations are acknowledged. Reinforcement learning approaches are shifting from optimising for user satisfaction toward **pedagogically-grounded reward functions** — training models to promote productive struggle and conceptual transfer rather than merely correct answers. The use of **simulated students** (LLM-based synthetic learners) enables scalable testing before deployment with real learners, though questions remain about how well simulated interactions represent authentic student behaviour.

Retrieval-Augmented Generation (RAG) is increasingly used to ground tutor responses in verified educational content, reducing hallucinations. Hybrid architectures combining symbolic reasoning with neural methods are emerging as the most promising approach — particularly for integrating knowledge tracing with conversational capability.

## Recommendations

We recommend the following priorities for funders, policymakers, and development partners:

**The field should mandate long-term outcome measurement.** Studies evaluating AI tutors should include delayed post-tests at minimum three months post-intervention, with six to twelve-month follow-ups for major deployments. Without this, the evidence base cannot support confident investment decisions. *(Immediate priority)*

**We recommend establishing standardised metrics for cognitive offloading.** The field needs validated, practical measures — including behavioural indicators such as copy-paste frequency and hint dependency, alongside self-explanation quality and problem-solving persistence. These should be required alongside traditional learning gain metrics. *(By end of 2026)*

**Development partners should invest in equity-focussed deployment studies in LMICs.** Systematic measurement of differential effects across socioeconomic status, languages, cultural contexts, and access to technology is essential before scaling AI tutors in resource-constrained settings. *(Ongoing, with initial studies commissioned by mid-2026)*

**AI tutor developers should implement deliberate scaffolding fade-out mechanisms** — designing systems with explicit protocols for gradually reducing support as student competence grows, following the "enhanced cognitive scaffolding" and "progressive autonomy" frameworks emerging in the literature.

**We recommend prioritising hybrid architectures** that combine specialised sequential models for knowledge tracing with LLM generative capabilities for dialogue. LLMs alone fail at temporal student modelling; purpose-built components remain essential.

**The field should develop child-specific safety standards** distinct from adult-centric AI safety measures, with age-appropriate frameworks for children (ages 5–12) and adolescents (ages 13–17), including developmental considerations and parental oversight mechanisms. *(By end of 2026)*

**Funders should require cost-effectiveness analyses** comparing AI tutoring against alternative interventions — including peer tutoring, small-group instruction, and teacher professional development — to inform resource allocation decisions in contexts where every dollar matters.

**We aim to support the development of multilingual and culturally responsive benchmarks** that assess AI tutor quality in languages beyond English, addressing the systematic performance biases documented in current research.

## Key Papers

- **"AI tutoring can safely and effectively support students"** — Rigorous UK classroom RCT (N=165) demonstrating comparable efficacy to human tutors with superior knowledge transfer, establishing a safe deployment pathway.

- **"TutorBench"** — Expert-curated benchmark revealing no frontier LLM exceeds 56% on core tutoring skills, establishing the performance ceiling for current technology.

- **"Training LLM-based Tutors to Improve Student Learning Outcomes in Dialogues"** — Demonstrates training LLMs to maximise learning outcomes using student model predictions as reward signals, achieving 33% improvement in correctness prediction.

- **"The Unspoken Crisis of Learning: The Surging Zone of No Development"** — Introduces the theoretical framework arguing permanent AI assistance replaces cognitive development, with implications for system design.

- **"Problems With Large Language Models for Learner Modelling"** — Comprehensive evidence that LLMs fail at knowledge tracing despite fine-tuning, arguing for hybrid architectures.

- **"Short-term AI literacy intervention does not reduce over-reliance on incorrect ChatGPT suggestions"** — Experimental evidence that 52.1% of students adopted incorrect suggestions, highlighting the difficulty of combating cognitive offloading through education alone.

- **"FoundationalASSIST"** — First large-scale dataset (1.7M interactions) with complete question text and student responses, enabling previously impossible research directions.

- **"EduGuardBench"** — The only benchmark simultaneously assessing pedagogical competence and adversarial safety in educational contexts.

- **"Beware of Metacognitive Laziness"** — Rigorous experimental evidence that ChatGPT improves task performance while reducing metacognitive engagement, with detailed process analysis.

- **"Reasoning Mind Genie 2"** — Large-scale deployment (67,000 students) demonstrating cross-cultural curriculum transfer with strong effect sizes, relevant to LMIC scaling questions.

- **"Beyond Final Answers: Evaluating LLMs for Math Tutoring"** — Demonstrates the critical gap between 85.5% answer accuracy and 56.6% error-free dialogues.

- **"When Peers Outperform AI (and When They Don't)"** — Reveals that high-quality peer interactions generate curiosity AI cannot match, shifting focus from modality to interaction quality — a finding with significant implications for how AI tutors should be positioned alongside human learning.