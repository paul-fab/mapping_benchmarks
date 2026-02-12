# Knowledge Tracing and Student Modelling: Benchmarking AI's Ability to Understand What Learners Know

## Executive Summary

Knowledge tracing (KT) — the task of modelling students' evolving knowledge states and predicting their future performance based on historical interaction data — sits at the foundation of AI-enabled personalised education. Our analysis of **44 papers** reveals a field that has undergone rapid architectural transformation, moving from traditional probabilistic models such as Bayesian Knowledge Tracing (BKT) to sophisticated deep learning approaches employing attention mechanisms, graph neural networks, and memory-augmented architectures. Models now routinely achieve **75–85% AUC** on benchmark datasets, a level of predictive accuracy that appears impressive on the surface.

However, this body of research raises deeply troubling questions about what these models are actually measuring. Several critical papers demonstrate that models can achieve high performance by memorising question difficulty patterns rather than tracking genuine knowledge acquisition; that untrained random networks can perform nearly as well as trained models on some tasks; and that students can exploit system features — hint abuse, rapid clicking, trial-and-error guessing — without these behaviours being detected or accounted for. The field faces a fundamental tension between complex black-box models that achieve incrementally higher accuracy and simpler interpretable models that provide pedagogically meaningful insights to educators.

For education funders and policymakers — particularly those focussed on low- and middle-income countries (LMICs) — this matters enormously. Knowledge tracing underpins the personalisation engines of intelligent tutoring systems and adaptive learning platforms increasingly being deployed across sub-Saharan Africa, South Asia, and beyond. If these models are optimising for the wrong objective — predicting answers rather than understanding learning — the entire adaptive education value chain is built on uncertain foundations. The research also remains overwhelmingly focussed on mathematics in high-income contexts, with almost no benchmarks or evaluation protocols designed for LMIC educational settings.

## Key Themes

### The Deep Learning Arms Race — and Its Diminishing Returns

The largest cluster of research — **28 papers** — focusses on advancing deep learning architectures for knowledge tracing. The field has progressed through several waves: from recurrent neural networks (Deep Knowledge Tracing) to memory networks (Dynamic Key-Value Memory Networks, or DKVMN), to attention-based approaches such as the Self-Attentive Knowledge Tracing model (SAKT) and the Attentive Knowledge Tracing model (AKT), and most recently to graph neural networks including GKT, GIKT, and DAGKT. Each wave claims incremental improvements in prediction accuracy.

Yet the benchmarking library **pyKT** — which provides standardised evaluation across models — reveals that many recent architectures show **minimal improvements over the original Deep Knowledge Tracing model** when evaluated under consistent conditions. The paper "How Deep is Knowledge Tracing?" goes further, demonstrating that an enhanced version of traditional BKT can match deep learning performance, and that much of the apparent gain from deep learning may stem from high-dimensional projection rather than learning meaningful knowledge trajectories. This finding fundamentally challenges the assumption that more complex models yield better educational insights.

### Personalisation and Individual Differences

Approximately **15 papers** tackle the challenge of modelling student-specific characteristics — learning rates, forgetting behaviours, ability levels, and even emotional states. The LANA model, for instance, distinguishes between interactive sequences to create personalised knowledge representations, while the Dual-State Personalised Knowledge Tracing model incorporates emotional incorporation into its predictions. The DKVMN-KAPS framework separately models knowledge-absorption ability and problem-solving ability, acknowledging that these are distinct cognitive dimensions.

This work represents a meaningful advance over one-size-fits-all approaches. However, personalisation remains largely confined to adjusting model parameters rather than genuinely adapting pedagogical strategy. Models personalise *predictions* but rarely personalise *recommendations* in ways that educators can act upon.

### Forgetting and Temporal Dynamics

**12 papers** address the critical role of forgetting in learning — incorporating forgetting curves, time decay effects, and temporal patterns. The Deep Graph Memory Networks for Forgetting-Robust Knowledge Tracing and the Temporal Graph Memory Networks represent sophisticated attempts to model knowledge retention and loss over time. The Personalised Forgetting Mechanism with Concept-Driven Knowledge Tracing paper introduces per-student, per-concept forgetting rates.

This theme is particularly relevant for LMIC contexts, where learners may experience irregular access to technology and extended gaps between learning sessions. Yet none of these models have been validated in settings characterised by intermittent connectivity or irregular attendance patterns — conditions that are common across many low-resource educational environments.

### Model Robustness Under Real-World Conditions

A cluster of **9 papers** investigates how models perform when confronted with the messiness of real educational data. The paper "Investigating the Robustness of Knowledge Tracing Models in the Presence of Student Concept Drift" provides the first longitudinal study across five consecutive academic years, revealing that **all knowledge tracing models degrade over time** — with simpler models proving more robust than their complex counterparts. "Measuring the Impact of Student Gaming Behaviors on Learner Modeling" conceptualises gaming behaviours as data poisoning attacks, showing **15.2% AUC degradation** when random errors are introduced. The paper "Do We Fully Understand Students' Knowledge States?" demonstrates that models memorise question difficulty patterns rather than tracking genuine knowledge, proposing counterfactual reasoning as a mitigation strategy.

These findings have profound implications for deployment. Models trained on historical data may become increasingly unreliable, and students who learn to exploit system features can undermine personalisation quality without any visible signal to educators or system administrators.

## What Is Being Measured

The field overwhelmingly measures **binary prediction accuracy** — whether a student will answer the next question correctly — using AUC (Area Under the Curve) and accuracy as primary metrics, supplemented by Root Mean Squared Error (RMSE). Models are evaluated on their ability to track knowledge state trajectories over time for individual knowledge concepts, with attention weights and relevance of historical interactions serving as secondary indicators.

Beyond core prediction, researchers measure forgetting rates and knowledge decay parameters, student ability levels and learning rates, question difficulty and discrimination parameters, and concept relationships and prerequisite structures. The field has developed standardised cross-validation protocols on benchmark datasets including the **ASSISTments** family (2009, 2015, 2017), **EdNet-KT1**, **Statics2011**, and **Junyi Academy**. Transfer learning effectiveness across different courses and domains is an emerging evaluation dimension, alongside computational efficiency metrics relevant to scalability.

Prediction calibration and confidence measures receive attention in a subset of papers, though uncertainty quantification remains underexplored. The ASSIST2009-SSR benchmark adds expert-labelled skill-to-skill relationship graphs, enabling evaluation of prerequisite modelling — a step toward more educationally meaningful assessment.

## Critical Gaps

The most consequential gap is the absence of measurement of **actual student learning gains**. The entire field optimises for next-question prediction, yet no standard protocol exists to verify whether high-performing models produce better educational outcomes when used to drive instruction. This disconnect between prediction accuracy and learning impact represents the single most important investment opportunity for education funders.

**Long-term educational outcomes** remain almost entirely unexamined. Models predict the next interaction but provide no evidence about knowledge retention weeks or months later, transfer of learning to novel contexts, or development of independent problem-solving skills. Relatedly, **metacognitive skills, self-regulation, and learning strategies** — the capacities that determine whether students become effective lifelong learners — fall entirely outside current measurement frameworks.

The field also neglects **fairness and equity dimensions**. Few papers examine whether models perform equitably across demographic groups or whether they might perpetuate existing educational inequalities — a concern that should be central to any deployment in LMICs where educational access is already uneven. **Teacher usability** of model outputs is similarly unstudied; no papers evaluate whether the insights generated by knowledge tracing models are actionable in real classroom settings.

The **domain coverage** of existing research is remarkably narrow. The overwhelming focus on mathematics limits generalisability, with minimal exploration of science, language learning, creative domains, or complex professional skills. **Multimodal learning behaviours** — video watching, reading patterns, forum participation, collaborative learning — are ignored despite being central to modern online education. And **economic deployment costs**, critical for LMIC contexts, receive no attention whatsoever.

## Cognitive Offloading

Explicit attention to cognitive offloading — whether AI-driven support helps or hinders genuine learning — is strikingly limited across these 44 papers. Only **3 papers** engage with this concern in any meaningful way, and none frame it in terms of cognitive offloading directly.

The most relevant work is "Measuring the Impact of Student Gaming Behaviors on Learner Modeling," which documents how hint abuse, random guessing, and rapid clicking represent problematic reliance patterns that contaminate data quality. These gaming behaviours are conceptualised as data poisoning attacks rather than as signals of over-dependence on AI scaffolding, but the underlying concern is the same: students can interact with adaptive systems in ways that generate correct responses without genuine learning occurring.

More fundamentally, knowledge tracing models **fail to distinguish between genuine mastery and lucky guesses**, or between carelessness and conceptual gaps. No papers in the corpus measure whether AI-driven personalisation reduces productive struggle or undermines development of independent problem-solving skills. This is a significant blind spot. As adaptive learning platforms become more prevalent in LMICs — often serving as the primary instructional resource rather than a supplement — understanding whether these systems build or erode learner independence becomes critical.

## Notable Benchmarks and Datasets

The **ASSISTments2009** dataset remains the most widely used benchmark, comprising 325,637 interactions from 4,151 students across 110 mathematics skills. Its longevity enables direct comparison across decades of research, though its relatively small scale and narrow domain constrain generalisability. The **ASSISTments2015** and **ASSISTments2017** variants expand the student population (19,840 and 1,709 students respectively) and include richer metadata.

**EdNet-KT1** stands apart in scale, with approximately **780,000 students** and millions of interactions on TOEIC-like English questions. This is by far the largest benchmark available and offers a diverse international student population, making it the closest existing resource to an LMIC-relevant evaluation framework — though it remains focussed on a single assessment format.

The **Statics2011** dataset, with 189,297 interactions across 1,223 engineering statics problems from 333 students, provides a rare window into complex multi-step reasoning. The **POJ (Peking Online Judge)** dataset, featuring programming competition problems, is notable for being exceptionally difficult — models achieve only **60–65% AUC** — demonstrating the limitations of current approaches on genuinely challenging cognitive tasks.

The **ASSIST2009-SSR** benchmark, augmented with expert-labelled skill-to-skill relationship graphs, represents an important step toward pedagogically grounded evaluation. The **Synthetic-5** dataset — 4,000 simulated students with known ground truth — enables verification of whether models learn intended patterns, though it obviously lacks the complexity of real educational data. The **ASSIST2009-2017 Multi-Year** dataset enables study of concept drift across five consecutive academic years, providing the only longitudinal evaluation framework in the field.

## Methodological Trends

The dominant methodological trajectory is a shift from hand-crafted probabilistic models toward end-to-end deep learning with learned representations. Attention mechanisms and Transformer architectures, adapted from natural language processing, have become the default approach, with graph neural networks increasingly used to model relationships between questions, concepts, and students.

Memory-augmented architectures such as DKVMN explicitly maintain concept-level knowledge states, offering a degree of structural interpretability. Multi-task learning — combining prediction with auxiliary objectives such as concept discovery or student clustering — is gaining traction as a way to extract richer representations. Contrastive learning and data augmentation techniques address the challenge of generalisation with limited data, while pre-training on large datasets followed by fine-tuning for specific courses represents a promising transfer learning paradigm.

Notably, there is growing use of **adversarial training and robustness evaluation** against noisy or biased data, reflecting awareness that educational data is inherently messy. Visualisation techniques including t-SNE, UMAP, and attention maps are employed for interpretability, though these remain more illustrative than rigorously validated. The development of standardised benchmarking frameworks — most notably pyKT and pyBKT — represents a welcome move toward reproducibility, addressing a crisis in which many papers reported inconsistent results for the same model on the same data.

Simulation-based evaluation using synthetic students and Generative Adversarial Imitation Learning (GAIL) approaches offers a pathway to controlled experimentation, though validation against real learner behaviour remains limited.

## Recommendations

We recommend that education funders and development partners prioritise the following actions to strengthen the evidence base for knowledge tracing in education:

**Reorient evaluation toward learning outcomes.** The field should establish standardised protocols for measuring whether model-driven instruction produces better learning gains — not merely better predictions. We recommend funding controlled studies comparing student learning outcomes between model-driven and human-designed instruction *(by end of 2027)*.

**Develop LMIC-specific benchmarks.** Current benchmarks are drawn almost exclusively from high-income country platforms. The field urgently needs datasets capturing the realities of LMIC education — irregular attendance, multilingual learners, limited connectivity, and diverse curricula. We aim to support the creation of at least two such benchmarks through our ecosystem *(by 2028)*.

**Require interpretability as standard practice.** We recommend that funders mandate interpretability analysis — attention visualisations, feature importance, and qualitative review by domain experts — as a condition for supporting knowledge tracing research. AUC alone is insufficient.

**Invest in robustness and fairness evaluation.** Models that degrade over time or perform inequitably across demographic groups should not be deployed in educational systems serving vulnerable populations. The field should establish fairness and bias evaluation standards as a prerequisite for real-world deployment.

**Expand beyond mathematics.** Funders should incentivise development of knowledge tracing approaches for science, language learning, and complex problem-solving domains — areas of high relevance for LMIC education systems.

**Bridge the research-practice gap.** We recommend partnering with real educators — particularly in LMIC contexts — to understand what insights they need from student models and whether current model outputs are actionable in classroom settings *(ongoing)*.

**Investigate the impact of large language models.** The widespread availability of LLMs such as GPT-4, Claude, and Gemini fundamentally changes the assumptions underlying knowledge tracing. Students may use these tools to complete exercises without developing underlying competence. Research should urgently investigate how LLM availability affects the validity of knowledge tracing models.

## Key Papers

- **"How Deep is Knowledge Tracing?"** — Critical examination demonstrating that enhanced BKT can match deep learning performance, suggesting that much of the complexity in modern architectures may be unnecessary. Essential reading for anyone evaluating AI-EdTech products that claim sophisticated student modelling.

- **"On the Interpretability of Deep Learning Based Models for Knowledge Tracing"** — Reveals that deep learning models learn a general 'ability model' rather than tracking individual skills, and that untrained random networks achieve similar performance. Exposes fundamental limitations in how the field validates its claims.

- **"Measuring the Impact of Student Gaming Behaviors on Learner Modeling"** — First systematic study of gaming behaviours as data poisoning attacks, demonstrating 15% performance degradation and establishing the need for robustness evaluation in educational AI systems.

- **"Do We Fully Understand Students' Knowledge States?"** — Demonstrates that models memorise question difficulty rather than tracking knowledge, and proposes counterfactual reasoning as a mitigation approach. Addresses fundamental validity concerns.

- **"pyKT: A Python Library to Benchmark Deep Learning based Knowledge Tracing Models"** — Provides standardised evaluation revealing minimal improvements of many recent models over the original Deep Knowledge Tracing. Essential infrastructure for reproducible research.

- **"Investigating the Robustness of Knowledge Tracing Models in the Presence of Student Concept Drift"** — First longitudinal study showing universal model degradation over time, with simpler models proving more robust. Critical for deployment planning.

- **"Improving Low-Resource Knowledge Tracing Tasks by Supervised Pre-training and Importance Mechanism Fine-tuning"** — Demonstrates 5% AUC gains with only 25% of training data through transfer learning — directly relevant to data-scarce LMIC deployment contexts.

- **"Knowledge Tracing for Complex Problem Solving"** — Addresses the limitation of single-concept questions by proposing adaptive aggregation for noisy complex problem-solving data, pointing toward more educationally realistic evaluation.