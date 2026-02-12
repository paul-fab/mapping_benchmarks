# Personalised Adaptive Learning: Benchmarking AI-Driven Systems for Education

## Executive Summary

Personalised adaptive learning represents one of the most technically mature — yet pedagogically under-evaluated — areas in AI-for-education research. Our analysis covers **200 papers** spanning knowledge tracing models, intelligent tutoring systems (ITS), adaptive content sequencing, and the emerging integration of large language models (LLMs) into personalised learning pathways. The field has produced sophisticated architectures capable of predicting whether a student will answer the next question correctly, but it has done remarkably little to establish whether these predictions translate into genuine, lasting learning.

The dominant research paradigm centres on **knowledge tracing (KT)** — modelling student knowledge states from interaction logs to predict future performance. Deep learning approaches have largely supplanted classical Bayesian methods, with Transformer-based and attention-mechanism architectures now standard. However, a critical tension runs through the literature: while prediction accuracy (measured via AUC and RMSE) has improved steadily, the field overwhelmingly evaluates systems on narrow technical metrics rather than on whether students actually learn more, retain knowledge longer, or develop independent problem-solving capacity. Fewer than a handful of the 200 papers examined conduct longitudinal evaluations or measure transfer of learning to novel contexts.

For low- and middle-income countries (LMICs), these gaps matter profoundly. Most benchmark datasets originate from platforms in the United States, South Korea, and China, meaning adaptive systems are trained and validated on learner populations that bear little resemblance to the diverse linguistic, curricular, and infrastructural contexts of LMICs. The cold-start problem — how to personalise effectively when limited learner data exists — is acutely relevant to settings where digital learning infrastructure is nascent. This report sets out what is being measured, what is missing, and where investment could shift the field from prediction optimisation toward genuine impact at scale.

## Key Themes

### Knowledge Tracing: The Technical Backbone

Knowledge tracing is the single most researched topic in personalised adaptive learning, appearing across approximately **70 papers** in this corpus. The trajectory of the field is clear: from Bayesian Knowledge Tracing (BKT) and Item Response Theory (IRT), through the landmark **Deep Knowledge Tracing** paper that applied recurrent neural networks to student interaction sequences, to contemporary architectures employing self-attention mechanisms, memory-augmented networks, and graph neural networks.

Papers such as **simpleKT** have demonstrated that a straightforward attention-based model can match or exceed the performance of far more complex architectures — raising important questions about whether the field's emphasis on architectural novelty has outpaced genuine progress. The **pyKT** benchmark suite, which standardised evaluation across seven datasets and ten model implementations, revealed that many innovations show **minimal improvement over the original DKT** when rigorously and consistently evaluated. This finding — that much of the apparent progress may be an artefact of inconsistent evaluation practices — is among the most important in the corpus.

Meanwhile, **"How Deep is Knowledge Tracing?"** critically examined whether deep models genuinely outperform well-engineered traditional approaches, challenging the assumption that model complexity automatically yields better educational insights. These sceptical contributions are essential for grounding the field's development.

### Beyond Binary Correctness: Richer Student Models

A growing strand of research moves beyond the simplistic question of whether a student got an answer right or wrong. **FoundationalASSIST** introduced the first large-scale KT dataset containing full question text and actual student responses — not just correctness labels — enabling researchers to analyse student thinking rather than merely student outcomes. The **Eedi** dataset, designed around diagnostic multiple-choice questions, captures specific misconceptions through carefully designed distractors. **Open-ended Knowledge Tracing for Computer Science Education** pioneered prediction of actual student code rather than binary pass/fail results, enabling fine-grained analysis of programming knowledge.

These richer data representations are critical for LMIC contexts, where understanding *why* a student struggles — whether due to language barriers, conceptual gaps, or unfamiliarity with question formats — matters far more than simply predicting whether they will answer correctly.

### LLM Integration: Promise and Peril

Approximately **10 papers** explore LLMs in personalised adaptive learning, reflecting the field's rapid engagement with these models. **"Problems With Large Language Models for Learner Modelling"** provides a sobering assessment, demonstrating that LLMs — including GPT-4, which was the leading commercial model at the time of these studies — lack the temporal coherence needed for reliable knowledge tracing and raise significant concerns around responsible AI use in K-12 settings. **"LLMs are Biased Teachers"** documents how LLM-driven personalisation can reproduce and amplify biases affecting different student groups inequitably.

Conversely, **CLST** demonstrates that generative language models can help mitigate the cold-start problem by leveraging pre-trained knowledge to make initial predictions about new learners. **Language Bottleneck Models** offer a promising middle path, using LLMs to generate interpretable natural-language knowledge state summaries that express nuanced insights — such as specific misconceptions — bridging the gap between prediction and explanation. These hybrid approaches, which combine the strengths of structured educational models with LLM capabilities, appear more promising than LLM-only solutions.

### Adaptive Content Sequencing and Reinforcement Learning

Approximately **18 papers** address the challenge of deciding what to present to a learner and when. **"Multi-Armed Bandits for Intelligent Tutoring Systems"** validated a reinforcement learning approach for curriculum optimisation with **400 real students**, showing results comparable to expert-designed sequences — a notable achievement for scalability in contexts where curriculum design expertise is scarce. **"How Should Intelligent Tutoring Systems Sequence Multiple Graphical Representations of Fractions?"** combined classroom experiments, think-aloud protocols, and knowledge tracing to demonstrate that interleaved practice produces better conceptual learning than blocked practice for students with dyscalculia — a rare example of a multi-methods study that measures actual learning outcomes.

### Engagement, Agency, and the Role of the Learner

Research on gamification and learner engagement — approximately **8 papers** — highlights an underappreciated dimension of adaptive learning. **"Improved Performances and Motivation in Intelligent Tutoring Systems: Combining Machine Learning and Learner Choice"**, a large-scale randomised controlled trial with **265 students**, found that algorithmic personalisation alone is insufficient; combining adaptation with **learner agency** — allowing students some choice over their learning path — produced the best outcomes for both performance and motivation. This finding has significant implications for system design, particularly in LMIC contexts where fostering student autonomy is a key educational goal.

## What Is Being Measured

The field is overwhelmingly focussed on **prediction accuracy** as its primary metric. AUC (Area Under the Curve), accuracy, F1 scores, and RMSE dominate reporting across knowledge tracing studies. These metrics assess how well a model predicts whether a student will answer the next question correctly — a useful technical capability, but one that functions as a proxy for learning rather than a direct measure of it.

Beyond prediction, some studies measure **knowledge state estimates and mastery probabilities**, model calibration (Expected Calibration Error), convergence speed, and computational efficiency. A smaller subset reports on **learning gains** through pre-test to post-test comparisons, engagement metrics such as time-on-task and completion rates, and system usability scores. The **KT-PSP-25** dataset introduces process-level proficiency indicators — capturing how students solve problems, not just whether they get the right answer — and the **Response Discrimination Metric** quantifies how effectively questions differentiate students at varying mastery levels.

However, what is measured remains remarkably narrow given the ambition of the systems being built. Prediction of the next answer is treated as synonymous with understanding of the learner — an assumption that deserves far greater scrutiny.

## Critical Gaps

The most consequential gap across this body of work is the near-total absence of **longitudinal evaluation**. Almost no studies measure learning retention beyond immediate post-tests, let alone weeks or months later. Whether adaptive systems produce durable knowledge gains — or merely optimise short-term performance — remains an open question.

**Transfer of learning** to novel contexts is similarly unmeasured. If a student masters fractions within an adaptive maths platform, can they apply that understanding in a different context, with different representations, without AI support? The literature provides almost no evidence on this point.

**Equity and fairness** receive minimal systematic attention. Most benchmark datasets come from relatively homogeneous populations in high-income countries. Disaggregated analysis by socioeconomic status, language background, gender, or disability status is rare. Whether adaptive algorithms narrow or widen achievement gaps — a question of paramount importance for LMIC deployment — is largely unexamined.

**Teacher integration and classroom ecology** represent another significant blind spot. How adaptive systems affect teacher-student interactions, teacher workload, and the broader classroom environment is almost entirely absent from the literature. For LMIC contexts, where teacher capacity and classroom conditions differ markedly from the settings in which these systems are developed, this gap is particularly concerning.

Finally, **cost-effectiveness and scalability in resource-constrained settings** — arguably the most important consideration for LMIC deployment — is virtually unaddressed. Many sophisticated architectures assume computational resources and data volumes that may be unavailable in the contexts where personalised learning is most needed.

## Cognitive Offloading

Despite this category's explicit focus on adapting assistance to learner needs, only approximately **15 papers** address cognitive offloading concerns — and most do so tangentially. This represents a fundamental disconnect: the field builds systems designed to help learners, yet rarely asks whether that help undermines the cognitive processes that produce genuine learning.

The most substantive finding comes from the **Enhanced Cognitive Scaffolding** framework, which proposes **progressive autonomy** — initially providing high support that gradually transfers control to the learner to prevent dependency. This is a theoretically sound approach, but empirical validation remains thin. Research on teachable agents — where students teach an AI, reversing the typical assistance relationship — shows that students who teach engage in deeper reflection, though this requires carefully designed Socratic questioning to avoid superficial engagement.

Several papers note the tension between optimising for learner comfort and maintaining the **productive struggle** necessary for deep learning. The Duolingo-related study acknowledges targeting an approximately **80% success rate** as a "Goldilocks zone" balancing engagement and challenge, but the cognitive load implications of this design choice are not rigorously evaluated. Papers on spaced repetition observe that over-optimising for ease — always presenting questions the student is likely to get right — prevents the retrieval difficulty that strengthens long-term memory.

Perhaps most concerning, the literature identifies a risk of **LLM "sycophancy"** — where AI tutors agree with student misconceptions rather than providing corrective challenge. Few papers measure whether improved prediction accuracy translates to learning that persists without AI support, and the field shows **little empirical work on optimal levels of struggle** or how to detect when scaffolding should fade.

## Notable Benchmarks and Datasets

The **ASSISTments** dataset family (2009, 2015, 2017 versions) remains the most widely used benchmark in knowledge tracing, covering middle school mathematics interactions from a US-based tutoring platform. Its ubiquity enables cross-study comparison, but it has been criticised for data quality issues and limited contextual richness — and its exclusive focus on US middle school maths limits generalisability.

**EdNet**, with over **131 million interactions** from a Korean education platform, provides the largest public educational dataset. Its hierarchical structure captures diverse student behaviours — lecture watching, quiz solving, item purchasing — beyond simple question answering. **FoundationalASSIST** introduced **1.7 million K-12 maths interactions** with full question text and actual student responses aligned to Common Core standards, enabling the first LLM-based knowledge tracing approaches.

The **pyKT Benchmark Suite** addresses the field's reproducibility crisis by providing standardised preprocessing and evaluation protocols across seven datasets and ten model implementations. The **Eedi** dataset stands out as the only major benchmark explicitly designed to capture **misconceptions** rather than just correctness, through diagnostically designed multiple-choice distractors.

Newer benchmarks push into richer territory: **KT-PSP-25** captures problem-solving process data with step-level proficiency indicators; **ES-KT-24** introduces multimodal knowledge tracing combining educational game video, text, and interaction logs; and **CodeWorkout** enables evaluation of knowledge tracing for open-ended programming tasks. The **Calcularis** training data provides a rare example of controlled classroom experimentation measuring actual learning outcomes for students with dyscalculia.

Critically, no major benchmark dataset originates from an LMIC context, and none measures learning outcomes directly — they measure prediction of student responses, which is a fundamentally different thing.

## Methodological Trends

The field has undergone a clear architectural progression: from probabilistic models (BKT, IRT) to recurrent neural networks (LSTM, GRU-based DKT), to attention-based approaches (SAKT, AKT, SAINT), and now to Transformer architectures and graph neural networks that model prerequisite relationships between concepts. Hybrid approaches — combining neural networks with classical psychometric theories — represent an increasingly productive direction.

**Benchmark-driven evaluation** using public datasets with five-fold cross-validation has become standard practice. However, this creates a methodological monoculture: models are optimised for offline prediction on historical logs rather than validated through classroom deployment. Randomised controlled trials remain rare — the **265-student RCT** on learner choice and the **400-student validation** of multi-armed bandit sequencing are notable exceptions.

Emerging methodological trends include **uncertainty quantification** through Bayesian methods and probabilistic modelling, **contrastive learning** for question and skill representation, and **simulation-based evaluation** using synthetic student data when real-world deployment is infeasible. The integration of LLMs for content understanding represents a significant shift, though models available in 2023–2024 — including GPT-4 and Claude 2 — were the basis for most studies. These findings may need re-evaluation with current-generation models.

A notable concern is the dominance of **single-metric optimisation**, primarily AUC, with limited consideration of multiple outcome measures. The field would benefit from multi-objective evaluation frameworks that balance prediction accuracy with interpretability, fairness, computational efficiency, and alignment with learning goals.

## Recommendations

We recommend the following priorities for funders, researchers, and system developers working in personalised adaptive learning:

**Shift evaluation from prediction to learning.** The field should establish standard protocols requiring **delayed retention tests** (weeks or months post-intervention), transfer assessments using novel problem contexts, and measurement of independent problem-solving ability without AI support. Investment in longitudinal evaluation infrastructure — including multi-year studies examining sustained impact — should be a priority *(beginning immediately and ongoing)*.

**Invest in LMIC-relevant benchmarks and datasets.** We recommend funding the creation of benchmark datasets that represent diverse subjects, student populations, languages, and educational contexts beyond US middle school mathematics. These should include measures of actual learning outcomes — not just prediction accuracy — and be designed as **digital public goods** *(target: initial datasets by December 2026)*.

**Mandate equity audits for adaptive systems.** Funders should require disaggregated performance analysis across student demographics, learning contexts, and prior knowledge levels before supporting system deployment. The field should systematically evaluate whether adaptive algorithms narrow or widen achievement gaps.

**Develop scaffold fading protocols.** We recommend prioritising research on **progressive autonomy mechanisms** — where AI support explicitly decreases as competence increases — with validated metrics for assessing whether students maintain performance when support is removed. This directly addresses cognitive offloading concerns.

**Bridge the research-practice gap.** The field should invest in **teacher-AI collaboration** models that augment rather than replace teacher judgement, providing interpretable diagnostics and allowing teacher override. Practical deployment considerations — including computational efficiency, cost-effectiveness, and integration with existing classroom practices — should be co-primary evaluation criteria.

**Ground adaptation in learning science.** We recommend that adaptive systems be explicitly designed around established principles — spacing effects, retrieval practice, productive failure, desirable difficulty — rather than purely optimising prediction metrics. Systems should be required to demonstrate that their adaptive behaviour aligns with known learning phenomena *(ongoing)*.

**Address the cold-start problem for LMIC deployment.** Methods that work well with limited data should be prioritised, as real deployments in resource-constrained settings often face new students, new content, and minimal historical interaction data. Hybrid approaches combining LLM capabilities with structured educational models show particular promise here.

## Key Papers

- **Deep Knowledge Tracing** — The foundational paper applying deep learning to knowledge tracing, establishing DKT as the dominant paradigm. Essential reading for understanding the field's trajectory, despite known interpretability limitations.

- **pyKT: A Python Library to Benchmark Deep Learning based Knowledge Tracing Models** — Addresses the reproducibility crisis with standardised evaluation, revealing that many recent innovations show minimal improvement over DKT when rigorously evaluated. Critical for understanding actual versus claimed progress.

- **simpleKT: A Simple But Tough-to-Beat Baseline for Knowledge Tracing** — Demonstrates that simpler models can match complex architectures, challenging the field's emphasis on architectural novelty and highlighting the importance of standardised evaluation.

- **Problems With Large Language Models for Learner Modelling** — Essential critical evaluation showing LLMs lack temporal coherence for knowledge tracing and raising responsible AI concerns for K-12 deployment. A necessary counterweight to LLM enthusiasm.

- **FoundationalASSIST: An Educational Dataset for Foundational Knowledge Tracing** — The first large-scale KT dataset with full question text and actual student responses, enabling analysis of student thinking rather than just performance prediction.

- **Improved Performances and Motivation in Intelligent Tutoring Systems: Combining Machine Learning and Learner Choice** — Large-scale RCT demonstrating that learner agency combined with algorithmic personalisation outperforms either alone. Important evidence for system design.

- **Language Bottleneck Models for Qualitative Knowledge State Modeling** — Innovative approach generating interpretable natural-language knowledge state summaries, bridging prediction and explanation in ways that could support teacher decision-making.

- **EdNet: A Large-Scale Hierarchical Dataset in Education** — The largest public educational dataset (131M+ interactions), enabling reproducible research at scale with diverse student behaviours.

- **Enhanced Cognitive Scaffolding: The Architecture of Cognitive Amplification** — Provides the theoretical framework for progressive autonomy in human-AI interaction, directly addressing the comfort-growth paradox central to adaptive learning design.

- **Evaluation Methods for Intelligent Tutoring Systems Revisited** — Updates foundational ITS evaluation methodologies, highlighting persistent challenges and cautioning against methodological pitfalls. Essential context for understanding what constitutes rigorous evaluation in this field.