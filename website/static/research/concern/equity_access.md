# Equity & Access

**50 papers matched** (12 directly addressing this concern)

## Executive Summary

The literature reveals significant equity and access concerns in AI-powered K-12 education systems, with evidence spanning digital divides, language bias, cost barriers, and disparate impacts on marginalized learners. Research shows that while AI tutoring systems hold promise for democratizing personalized learning—potentially addressing global teacher shortages and the 260 million children without schooling—current implementations often exacerbate existing inequalities. Studies consistently demonstrate that LLMs perform better in English than underrepresented languages, with models showing 6.5-18% accuracy drops for low-resource languages like Bangla and Arabic. Infrastructure gaps create access barriers, with only 20% of Sub-Saharan African schools having electricity and 69% of OECD teachers reporting inadequate training for differentiated instruction. Evidence suggests that even when access is provided, socioeconomic factors significantly influence participation rates, with student engagement in AI tutoring systems varying dramatically by economic background regardless of device availability.

However, the literature also identifies promising mitigation strategies and contextual factors that moderate these risks. Several studies show that carefully designed AI systems can improve outcomes for disadvantaged students when implemented with appropriate scaffolding. For instance, the CyberScholar system demonstrated that AI-assisted writing feedback helped diverse student populations when integrated with teacher rubrics, while the I-OnAR system improved performance for university students in Malaysia through intelligent adaptation. Critical design factors emerge including: prioritizing accessibility over computational power, embedding system-level protections rather than relying solely on user education, providing offline capability for connectivity-constrained contexts, and involving students from underrepresented groups in participatory design processes. The evidence suggests that architectural choices matter significantly—multi-agent systems better identify struggling students while single-agent systems are more cost-effective for general assessment—indicating that equity considerations should drive deployment decisions rather than treating all contexts as equivalent.

## Key Findings

### LLMs exhibit consistent linguistic bias, with English consistently outperforming low-resource languages by 6.5-26% in educational tasks

*Evidence type: empirical | 8 papers*

- LLMs are Biased Teachers: Evaluating LLM Bias in Personalized Education
- BanglaMATH: A Bangla benchmark dataset for testing LLM mathematical reasoning at grades 6, 7, and 8
- Investigating Bias: A Multilingual Pipeline for Generating, Solving, and Evaluating Math Problems with LLMs
- From Handwriting to Feedback: Evaluating VLMs and LLMs for AI-Powered Assessment in Indonesian Classrooms

### Infrastructure and connectivity barriers significantly limit access to AI educational tools, with only 20% of Sub-Saharan African schools having electricity and many students lacking reliable internet

*Evidence type: empirical | 6 papers*

- Discerning minds or generic tutors? Evaluating instructional guidance capabilities in Socratic LLMs
- Employment of Generative Artificial Intelligence in Classroom Environments to Improve Financial Education
- Intelligent tutoring systems for word problem solving in COVID-19 days

### Socioeconomic status predicts participation in AI tutoring systems independent of technology access, with student engagement varying by 40-60% across economic backgrounds

*Evidence type: empirical | 4 papers*

- Intelligent tutoring systems for word problem solving in COVID-19 days
- aiPlato: A Novel AI Tutoring and Step-wise Feedback System for Physics Homework
- Sebuah Kajian Pustaka

### DHH (deaf/Hard-of-Hearing) learners face specific barriers with LLM-based tutoring systems that lack multimodal support, particularly for sign language integration

*Evidence type: empirical | 1 papers*

- LLM-Powered AI Tutors with Personas for d/Deaf and Hard-of-Hearing Online Learners

### When students are involved in participatory design, they prioritize system-level accessibility features over advanced performance, advocating for device compatibility and offline capability

*Evidence type: empirical | 2 papers*

- "How can we learn and use AI at the same time?": Participatory Design of GenAI with High School Students
- LLM-Powered AI Tutors with Personas for d/Deaf and Hard-of-Hearing Online Learners

### Cost-effectiveness analysis shows 4x computational cost differences between multi-agent and single-agent systems, with implications for scalable deployment in resource-constrained settings

*Evidence type: empirical | 3 papers*

- Specialists or Generalists? Multi-Agent and Single-Agent LLMs for Essay Grading
- Can Large Language Models Match Tutoring System Adaptivity? A Benchmarking Study
- Ken Utilization Layer: Hebbian Replay Within a Student's Ken for Adaptive Exercise Recommendation

### Embeddings and encoders significantly affect semantic alignment and fairness, with different models producing systematically different outcomes for the same students

*Evidence type: empirical | 2 papers*

- Ken Utilization Layer: Hebbian Replay Within a Student's Ken for Adaptive Exercise Recommendation
- Towards Responsible and Trustworthy Educational Data Mining

### Teacher AI literacy gaps create implementation barriers, with 69% of teachers reporting need for professional development in AI-supported differentiated teaching

*Evidence type: empirical | 4 papers*

- Unifying AI Tutor Evaluation: An Evaluation Taxonomy for Pedagogical Ability Assessment
- The Promises and Pitfalls of Using Language Models to Measure Instruction Quality in Education
- Advancing Education through Tutoring Systems: A Systematic Literature Review

## Evidence For This Risk

- LLMs trained predominantly on English data consistently perform 6.5-26% worse on non-English educational tasks, with Arabic and Bangla showing largest performance gaps (BanglaMATH, Multilingual Math Pipeline studies)
- Student socioeconomic status significantly predicted participation in AI tutoring independent of device access during COVID-19, with low-SES students showing 40-60% lower engagement (ITS COVID-19 study)
- Only 20% of Sub-Saharan African schools have electricity access, fundamentally limiting deployment of AI educational tools requiring power (global education statistics cited in multiple papers)
- 69% of OECD teachers report lacking training in differentiated teaching practices essential for supporting diverse learners with AI tools (pedagogical knowledge gap studies)
- DHH students identified that current LLMs cannot support sign language communication despite this being their preferred modality, creating fundamental access barriers (DHH tutor personas study)
- Model bias analysis showed significant performance disparities by income (highest bias) and disability status, with some demographic groups receiving systematically lower-quality explanations (LLMs as Biased Teachers)
- Private school students (58.8% of sample) were overrepresented in participatory design study compared to 18.1% national average, suggesting self-selection effects in who shapes AI educational tools
- Automated essay scoring systems showed systematic bias, with models trained on human scores replicating rather than correcting human graders' tendency to reward length over quality regardless of errors
- Multi-agent systems require 4x computational resources compared to single-agent alternatives with only marginal performance gains, pricing out resource-constrained implementations
- Indonesian handwritten assessment study found VLM accuracy dropped significantly for 'naturally curly, diverse handwriting' from real classrooms, disadvantaging students with less standardized writing

## Mitigating Evidence

- CyberScholar system showed AI feedback was 'clear and factually correct' even when based on imperfect OCR input, and improved writing across diverse student populations when integrated with teacher rubrics
- I-OnAR system demonstrated 60% performance improvement for Malaysian university students through intelligent adaptive assessment, suggesting effectiveness in middle-income contexts
- Llama-3.3-70B achieved strong performance on pedagogical knowledge benchmarks at low inference cost ($0.01 per million tokens), enabling affordable deployment
- GPT-4o achieved 80%+ accuracy on K-12 math problems in multiple languages, demonstrating technical feasibility of multilingual support when properly designed
- aiPlato system showed students with higher engagement achieved 14-point higher exam scores regardless of prior performance, suggesting AI can help rather than hinder struggling students when well-implemented
- Participatory design with high school students revealed they understood AI limitations and advocated for transparent, system-level protections rather than accepting tools uncritically
- RADEC model integrated with AI showed significant improvements in financial literacy for Indonesian secondary students across multiple dimensions including planning and analysis
- Small open-source models (7B parameters) running locally achieved 62-64% accuracy on pedagogical tasks, enabling offline deployment without internet connectivity
- Neural-symbolic AI approaches showed better generalization in low-data conditions, achieving comparable performance to larger models while being more interpretable and less resource-intensive
- When DHH students were given agency to customize LLM personas and response styles, they successfully adapted tools to meet their diverse needs despite baseline accessibility limitations

## What Is Being Measured

- Language-specific accuracy gaps (percentage differences between English and other languages)
- Participation rates by socioeconomic status (SES) in online tutoring systems
- Infrastructure availability metrics (electricity access, internet connectivity, device ownership)
- Teacher preparedness indicators (professional development needs, AI literacy levels)
- Performance disparities by demographic groups (race, gender, disability, income) in AI assessment
- Cost per inference (tokens per million) for different model architectures and sizes
- Accessibility features present in systems (offline capability, device compatibility, multimodal support)
- Student engagement metrics across different socioeconomic contexts (time spent, completion rates)
- Model performance on low-resource languages using standardized benchmarks
- Bias metrics (Mean Absolute Bias, Maximum Difference Bias) across protected attributes
- Human-AI agreement rates across different student demographics
- Readability and comprehensibility scores across different language variants
- Inter-rater reliability between AI systems and human evaluators from diverse backgrounds

## Gaps — What Is NOT Being Measured

- Long-term learning outcomes for students using AI tools versus traditional instruction, disaggregated by SES and demographics
- Actual educational equity impacts—whether AI tools narrow or widen achievement gaps over multiple years
- Cost-benefit analyses that include total cost of ownership (devices, connectivity, training, maintenance) for schools in different economic contexts
- Psychological impacts of AI feedback on student self-efficacy and growth mindset, particularly for students from marginalized groups
- Teacher workload and time-use patterns when AI tools are introduced, and whether benefits accrue equally to teachers in under-resourced schools
- Cultural appropriateness and relevance of AI-generated content beyond language translation (values, examples, pedagogical approaches)
- Cumulative effects of using AI systems trained on biased data—how small biases compound over time and multiple interactions
- Student privacy practices and data protection compliance in real-world deployments, especially in low-income contexts with weak regulatory frameworks
- Opportunity costs—what students miss when AI tools replace other educational investments
- Intersectional effects—how multiple marginalization factors (e.g., low-income + ELL + disability) compound access barriers
- Actual usage patterns post-deployment in diverse schools (not just pilot studies with volunteer participants)
- Transfer effects—whether skills developed with AI support transfer to non-AI contexts students will encounter
- Family and community perspectives on AI in education from diverse cultural backgrounds
- Digital literacy prerequisites for effective AI tool use and whether these create hidden barriers

## Context Factors

- Language of instruction and LLM training data overlap—English-medium contexts show 15-25% better performance
- Socioeconomic status—affects participation independent of device access, with 40-60% engagement variation
- School resource levels—infrastructure (electricity, internet), teacher training, device availability all moderate effectiveness
- Student age and grade level—younger students (K-5) show different patterns than middle/high school
- Subject matter complexity—STEM subjects with clear right/wrong answers show different equity patterns than open-ended humanities
- Disability and learning difference status—DHH, dyscalculia, dyslexia all require specific accommodations rarely present
- Cultural and linguistic background—not just language proficiency but cultural relevance of examples and pedagogical approaches
- Prior academic performance—some studies show AI helps struggling students more, others show Matthew effects
- Device type and quality—mobile-only vs. laptop/desktop access affects usability
- Connectivity reliability—intermittent internet creates different challenges than consistent offline
- Teacher AI literacy and attitudes—heavily mediates implementation quality and student outcomes
- Deployment model—optional/voluntary use shows selection effects vs. mandatory integration
- Pedagogical approach—systems requiring active learning vs. passive content consumption differ in accessibility
- Assessment stakes—low-stakes formative vs. high-stakes summative assessment contexts
- Institutional support—presence/absence of IT support, professional development, leadership commitment

## Notable Studies

### LLMs are Biased Teachers: Evaluating LLM Bias in Personalized Education

**Design:** Evaluated 14 LLMs on 1,498 questions across multiple demographic groups using two bias metrics (MAB and MDB) with over 17,000 educational explanations
**Sample:** K-12 mathematics content across diverse demographic profiles (synthetic profiles representing different combinations of protected attributes)
**Key result:** Found highest bias along income levels (MAB) and both income and disability status (MDB); lowest bias for sex/gender and race/ethnicity. Both Gemini 2.5 Flash and DeepSeek V3 showed 6.5%+ performance improvement on English vs. non-English translated versions

### Intelligent tutoring systems for word problem solving in COVID-19 days

**Design:** Evaluated ITS implementation across 1,200 students in Spain during COVID-19 lockdown, comparing participation and outcomes by socioeconomic level
**Sample:** K-12 students in Spain, grades 4-8, mathematics word problems, during COVID-19 school closures
**Key result:** Student socioeconomic level was determining factor in participation rate regardless of whether administration guaranteed access to technological resources. Despite device provision, engagement varied by SES

### From Handwriting to Feedback: Evaluating VLMs and LLMs for AI-Powered Assessment in Indonesian Classrooms

**Design:** Evaluated state-of-the-art VLMs and LLMs on grading 14,000+ handwritten answers from grade-4 Indonesian students across Mathematics and English
**Sample:** Grade 4 students (N=14,000+ responses) from six Indonesian primary schools (3 rural, 3 urban), Mathematics and English subjects
**Key result:** VLMs struggled with 'naturally curly, diverse handwriting' from real classrooms causing error propagation in LLM grading, yet LLM feedback remained pedagogically useful despite imperfect visual inputs

### LLM-Powered AI Tutors with Personas for d/Deaf and Hard-of-Hearing Online Learners

**Design:** User study with 16 DHH learners interacting with LLM-powered tutors embodying different personas (DHH-centric university, DHH specialist, no DHH experience)
**Sample:** 16 DHH learners (ages 14-17+) interacting with ChatGPT-based tutors with varying DHH education experience personas
**Key result:** DHH participants identified critical gaps: LLMs cannot support sign language (visual or text), responses too long for some DHH users but not detailed enough for others, and needed transparent disclosure of AI limitations

### aiPlato: A Novel AI Tutoring and Step-wise Feedback System for Physics Homework

**Design:** Exploratory classroom study with university physics students using AI-enabled homework platform providing stepwise feedback over four optional assignments
**Sample:** University introductory physics students at University of Texas Arlington, 4 optional extra-credit assignments over one semester
**Key result:** High-engagement students scored 14 points higher on final exam (effect size 0.81) after controlling for prior performance; 60% rated platform helpful and well-aligned, though noted latency and restrictive code sanitization issues

### "How can we learn and use AI at the same time?": Participatory Design of GenAI with High School Students

**Design:** Participatory design workshop with 17 high school students co-designing GenAI tools and school policies to address concerns about bias, misinformation, over-reliance, and academic dishonesty
**Sample:** 17 high school students (ages 14-17, 58.8% private school vs. 18.1% national average) in U.S., recruited through AI/robotics interest groups
**Key result:** Students advocated for system-facing solutions (diverse training data, transparent citations, built-in safeguards) over user education; prioritized accessibility over computational power; showed sophisticated understanding of AI limitations

### BanglaMATH: A Bangla benchmark dataset for testing LLM mathematical reasoning at grades 6, 7, and 8

**Design:** Released benchmark of 1,700 Bangla math word problems from grades 6-8; evaluated 14 LLMs including commercial and open-source; augmented with distracting information and translated to English to test robustness and language bias
**Sample:** 1,700 grade 6-8 mathematics questions from Bangladeshi elementary school workbooks covering Arithmetic, Algebra, Geometry, and Logical Reasoning
**Key result:** Only Gemini 2.5 Flash and DeepSeek V3 achieved ≥80% accuracy; both showed 6.5%+ improvement when problems translated to English; models easily misled by irrelevant information; significant performance disparity for low-resource languages

### Towards Responsible and Trustworthy Educational Data Mining: Comparing Symbolic, Sub-Symbolic, and Neural-Symbolic AI Methods

**Design:** Compared symbolic, sub-symbolic, and neural-symbolic AI for predicting 7th-grade math performance using SRL data from Estonian students on balanced and imbalanced datasets
**Sample:** Estonian primary school students (7th grade), predicting national mathematics test performance using self-regulated learning questionnaire data
**Key result:** Neural-symbolic methods showed best generalizability in imbalanced datasets (common in real education) by compensating for underrepresented classes; symbolic and sub-symbolic emphasized different factors (cognitive/motivational vs. cognitive/demographic) but both overlooked metacognition

## Implications for LMICs

The equity and access concerns are particularly acute in low- and middle-income country (LMIC) contexts where multiple barriers compound. Infrastructure limitations are fundamental: only 20% of Sub-Saharan African schools have electricity access, which precludes deployment of most current AI educational tools. Even where connectivity exists, it is often unreliable, intermittent, or expensive, creating different usage patterns than in high-income contexts. Language barriers are severe—LMICs typically have multiple local languages that are dramatically underrepresented in LLM training data, leading to 15-25% performance drops. The Indonesian handwriting study demonstrates that even within middle-income countries, local variations in student work (handwriting styles, linguistic patterns) cause significant accuracy degradation in AI systems trained primarily on Western data. Teacher capacity gaps are wider in LMICs: 85% of teachers in developing countries lack training in inclusive teaching strategies that would be essential for supporting AI tool use. Cost structures differ fundamentally—while a 4x difference in computational cost between system architectures might be acceptable in high-income settings, it could determine feasibility entirely in resource-constrained contexts. The COVID-19 ITS study showed that even when governments guaranteed device access, socioeconomic factors still determined participation, suggesting that access is not merely technical but involves complex social and economic factors. Cultural appropriateness is rarely evaluated—most AI educational content is developed in Western contexts and may not align with local values, examples, or pedagogical traditions. Privacy and data protection risks are heightened where regulatory frameworks are weaker and students may lack understanding of data rights. Critically, the opportunity costs are higher—resources invested in AI tools could alternatively fund teacher salaries, infrastructure, or textbooks, and there is limited evidence that AI provides sufficient value to justify these tradeoffs in low-resource settings. The research base itself shows geographic bias, with most studies conducted in high-income countries, limiting understanding of how AI tools perform in LMIC contexts. Promising approaches include: prioritizing offline-capable tools using smaller models (7B parameters achieving 62-64% accuracy), ensuring systems work on low-end devices, involving local educators and students in participatory design, and focusing on complementing rather than replacing human instruction. The neural-symbolic approaches showing better low-data performance may be particularly relevant where training datasets are limited.

## Recommendations

- Prioritize accessibility over performance: Design systems that work on low-end devices with intermittent connectivity before optimizing for advanced features, as students advocated in participatory design studies
- Invest in multilingual model development: Allocate resources specifically to training and fine-tuning models on underrepresented languages, with evidence showing 15-25% performance gaps that disadvantage non-English speakers
- Implement mandatory embedding audits: Routinely audit encoder choices and semantic alignment across demographic groups, as different embeddings produce systematically different outcomes
- Provide teacher professional development: Address the 69% of teachers reporting inadequate AI training through structured, ongoing PD focusing on equitable implementation rather than just technical operation
- Build system-level protections: Embed safeguards like citation requirements, bias detection, and content filtering at the architecture level rather than relying on user vigilance
- Involve diverse students in participatory design: Include students from marginalized groups (DHH, low-SES, ELL) early in design processes, not just as end users
- Design for offline capability: Prioritize architectures that can function without constant internet (e.g., 7B parameter models achieving 62-64% accuracy locally) to reach connectivity-limited contexts
- Conduct cost-benefit analyses including total ownership: Evaluate not just model costs but full implementation costs including devices, connectivity, training, and opportunity costs of alternative investments
- Measure and report disaggregated outcomes: Require publication of performance metrics broken down by relevant demographic factors (SES, language, disability) rather than aggregate statistics
- Create language-specific pedagogical benchmarks: Develop assessment frameworks in multiple languages that test culturally relevant pedagogical knowledge, not just translated English content
- Implement transparency requirements: Require disclosure of training data composition, known limitations by demographic group, and model confidence in predictions
- Support hybrid approaches: Design systems that augment rather than replace human instruction, maintaining teacher judgment especially for marginalized students
- Establish ethical review for educational AI: Require independent review of equity implications before deployment, similar to medical device approval processes
- Build local capacity: Invest in training local developers and educators in LMIC contexts to adapt and customize tools rather than relying solely on imported solutions
- Create equitable evaluation standards: Develop benchmarks that test performance across diverse handwriting styles, language variants, and cultural contexts, not just standardized Western formats

## Top Papers

1. **LLMs are Biased Teachers: Evaluating LLM Bias in Personalized Education**
   First systematic evaluation of LLM bias across multiple demographic dimensions with novel metrics (MAB/MDB) and clear evidence of performance disparities by income and disability status

2. **Intelligent tutoring systems for word problem solving in COVID-19 days**
   Demonstrates that SES predicts AI tool participation independent of device access, revealing that equity barriers are social/economic not purely technical

3. **From Handwriting to Feedback: Evaluating VLMs and LLMs for AI-Powered Assessment in Indonesian Classrooms**
   Shows how AI systems trained on Western data fail on 'naturally curly, diverse handwriting' from real LMIC classrooms, exemplifying cultural/contextual bias

4. **LLM-Powered AI Tutors with Personas for d/Deaf and Hard-of-Hearing Online Learners**
   Provides detailed examination of accessibility barriers for DHH students including multimodal needs and reveals sophisticated user demands for transparency and customization

5. **"How can we learn and use AI at the same time?": Participatory Design of GenAI with High School Students**
   Shows students advocate for system-level solutions over user education and prioritize accessibility over performance, challenging developer assumptions

6. **BanglaMATH: A Bangla benchmark dataset for testing LLM mathematical reasoning at grades 6, 7, and 8**
   First benchmark documenting 6.5%+ language bias for low-resource language (Bangla) with systematic testing of robustness to distracting information

7. **Towards Responsible and Trustworthy Educational Data Mining: Comparing Symbolic, Sub-Symbolic, and Neural-Symbolic AI Methods**
   Demonstrates neural-symbolic approaches achieve better generalizability in low-data conditions common in LMIC contexts while providing interpretability


---

# Equity & Access

**25 papers matched** (12 directly addressing this concern)

## Executive Summary

The literature reveals a persistent and multifaceted equity challenge in AI/LLM deployment for K-12 education. Digital divides manifest at multiple levels: infrastructure (connectivity, devices), language (English dominance in training data and performance), cost (premium models, data requirements), and capacity (teacher training, digital literacy). Multiple papers demonstrate that LLM performance degrades significantly for low-resource languages, non-English speakers, and contexts without robust infrastructure. For instance, multilingual physics concept inventories show GPT-4o performs better in English than in other languages, and Korean mathematics assessments reveal similar patterns. Studies on rural education in India and vocational education in Indonesia highlight how infrastructure constraints, teacher readiness, parental skepticism, and language barriers compound access challenges.

Critically, the research shows that even when technical access exists, equity issues persist through model design and deployment. Automated essay scoring exhibits bias by economic status, tutoring systems show performance disparities across demographic groups, and knowledge tracing models can perpetuate inequitable learning pathways despite fair prediction metrics (AUC). Several papers demonstrate that majority-culture norms are embedded in AI systems: non-native English speakers struggle with prompt comprehension, culturally specific content may be misaligned with local contexts, and systems often fail to account for diverse educational approaches and resource constraints. The evidence suggests that without deliberate equity-centered design, AI tools risk widening existing educational gaps rather than closing them.

## Key Findings

### LLM performance degrades significantly for non-English and low-resource languages, with performance gaps of 10-30% compared to English across multiple tasks including mathematics, physics, and general question-answering

*Evidence type: empirical | 7 papers*

- Multilingual Performance of a Multimodal Artificial Intelligence System on Multisubject Physics Concept Inventories
- On the robustness of ChatGPT in teaching Korean Mathematics
- Estimating Exam Item Difficulty with LLMs: A Benchmark on Brazil's ENEM Corpus
- Automated evaluation of children's speech fluency for low-resource languages

### Infrastructure barriers (connectivity, devices, electricity) and digital literacy gaps are primary obstacles to AI adoption in low-resource settings, particularly rural and developing contexts

*Evidence type: empirical | 5 papers*

- The Impact of Large Language Models on K-12 Education in Rural India
- ChatGPT in Research and Education: Exploring Benefits and Threats
- Comprehensive Overview of the Concept and Applications of AI-based Adaptive Learning

### Automated assessment systems (AES, automated essay scoring) exhibit bias by economic status and demographic factors, with prompt-specific models showing greater bias than cross-prompt models

*Evidence type: empirical | 3 papers*

- Automatic Essay Scoring: Accuracy, Fairness, and Generalizability
- The Rise of Artificial Intelligence in Educational Measurement
- Antithesis of Human Rater: Psychometric Responding to Shifts Competency Test Assessment Using Automation

### Non-native English speakers face systematic disadvantages in both prompt comprehension and AI interaction, with success rates 10-20 percentage points lower than native speakers

*Evidence type: empirical | 4 papers*

- 'I Would Have Written My Code Differently': Beginners Struggle to Understand LLM-Generated Code
- The Impact of Large Language Models on K-12 Education in Rural India
- Multilingual Performance of a Multimodal Artificial Intelligence System on Multisubject Physics Concept Inventories

### Cost barriers exist at multiple levels: premium API access, computational requirements for training/deployment, data collection costs, and teacher training expenses disproportionately affect under-resourced institutions

*Evidence type: theoretical | 6 papers*

- The Rise of Artificial Intelligence in Educational Measurement
- Comprehensive Overview of the Concept and Applications of AI-based Adaptive Learning
- The Impact of Large Language Models on K-12 Education in Rural India

### Fairness in prediction metrics (e.g., AUC) does not guarantee equitable learning outcomes; knowledge tracing models can perpetuate inequitable curricula despite appearing 'fair' in traditional ML metrics

*Evidence type: empirical | 2 papers*

- Equity and Fairness of Bayesian Knowledge Tracing
- Measuring the Impact of Student Gaming Behaviors on Learner Modeling

### Teacher readiness and training gaps, combined with resistance from educators and parents, create implementation barriers that particularly affect under-resourced schools

*Evidence type: empirical | 5 papers*

- The Impact of Large Language Models on K-12 Education in Rural India
- ChatGPT in Research and Education: Exploring Benefits and Threats
- Comprehensive Overview of the Concept and Applications of AI-based Adaptive Learning

### Visual/multimodal content interpretation remains a significant weakness of current LLMs, disproportionately affecting students in domains requiring diagram interpretation (mathematics, sciences) and limiting accessibility for learners who rely on visual supports

*Evidence type: empirical | 4 papers*

- Multilingual Performance of a Multimodal Artificial Intelligence System on Multisubject Physics Concept Inventories
- On the robustness of ChatGPT in teaching Korean Mathematics
- 'I Would Have Written My Code Differently': Beginners Struggle to Understand LLM-Generated Code

### Open-source models may perform better than proprietary models in some contexts (e.g., multilingual settings) and offer greater accessibility, but require institutional capacity for deployment

*Evidence type: empirical | 3 papers*

- Estimating Exam Item Difficulty with LLMs: A Benchmark on Brazil's ENEM Corpus
- The ADAIO System at the BEA-2023 Shared Task
- Automated evaluation of children's speech fluency for low-resource languages

## Evidence For This Risk

- GPT-4o shows marked performance differences across languages on physics concept inventories, with English outperforming other languages by 15-25% on average, and Asian/non-Latin script languages showing the greatest degradation
- In Korean mathematics assessment, ChatGPT achieved only 66.72% accuracy, with systematic struggles on diagram-based questions and sequential reasoning that disadvantage non-English educational contexts
- Prompt-specific automated essay scoring models exhibited significantly greater bias toward students of different economic statuses compared to cross-prompt models, with differences reaching 8-10 percentage points
- Rural Indian student volunteers identified infrastructure (connectivity, devices), teacher training gaps, and parental skepticism as primary barriers, with 91% reporting connectivity issues as a major obstacle
- Non-native English speakers showed 10-20 percentage point lower success rates in prompt comprehension tasks with LLMs compared to native English speakers in CS1 programming contexts
- Only 5% of students in vocational education settings used paid ChatGPT versions despite potential benefits, indicating cost as a significant barrier to accessing premium AI capabilities
- Bayesian Knowledge Tracing models can create inequitable learning pathways that minimize time for some students while maximizing it for others, even when prediction fairness (AUC) appears balanced across groups
- LLM performance on ENEM (Brazil) showed 25% performance gap between English-translated questions versus original Portuguese, demonstrating persistent language bias
- In simulated low-resource knowledge tracing scenarios (50 students, 5 exercises), standard deep learning models showed 18-25% performance degradation, while frameworks designed for low-resource settings maintained effectiveness
- 73.89% to 75.09% accuracy improvement was observed when Korean mathematics questions were translated to English before LLM processing, demonstrating systematic disadvantage for non-English content

## Mitigating Evidence

- AUC-optimized knowledge tracing models (B2KT, COMAUC) showed improved performance under low-resource conditions (100 training instances) and greater robustness to imbalanced data compared to standard cross-entropy optimization
- Open-source multilingual models (e.g., Whisper for speech, open translation models) can achieve comparable performance to proprietary systems when properly fine-tuned, reducing cost barriers
- Simple machine learning models (SVM with carefully engineered features) sometimes outperform complex neural networks in low-resource settings, suggesting accessible approaches can be effective
- Supervised pre-training on rich-resource datasets followed by importance-mechanism fine-tuning enabled effective knowledge tracing in low-resource scenarios, providing a pathway for data-scarce contexts
- Student volunteers in rural India showed strong enthusiasm (92% positive) for AI tutoring despite infrastructure constraints, suggesting demand exists even in challenging contexts
- Few-shot prompting approaches reduced data requirements for some tasks, potentially lowering barriers to deployment in data-scarce environments
- Teachable agent systems successfully engaged students as young as 2nd grade (ages 7-8) across diverse settings, demonstrating accessibility across age ranges
- Post-hoc calibration techniques reduced global biases in automated assessment without requiring model retraining, offering a lower-cost equity improvement pathway
- Group formation algorithms leveraging knowledge tracing data enabled differentiated instruction without requiring expensive 1-on-1 tutoring, potentially scaling support in under-resourced classrooms

## What Is Being Measured

- Prediction accuracy/AUC across demographic groups (gender, economic status, language, race)
- Performance gaps between languages (often English vs. non-English)
- Infrastructure availability (internet connectivity, device access, electricity)
- Cost metrics (API pricing, computational requirements, data collection costs)
- Teacher readiness and training needs (surveys, self-reports)
- Digital literacy levels (pre-post assessments, task success rates)
- Model calibration and bias (fairness metrics like demographic parity, equalized odds)
- Prompt comprehension success rates by native language
- Learning gains in low-resource vs. high-resource settings
- Model performance degradation with limited training data
- Success rates on diagram-heavy vs. text-only content
- Disparities in hint-seeking, help-seeking, and gaming behaviors across groups

## Gaps — What Is NOT Being Measured

- Intersectional equity effects (combinations of language, economic status, disability, rural/urban)
- Long-term educational trajectory impacts of early AI exposure disparities
- Cultural relevance and appropriateness of AI-generated content across different educational contexts
- Opportunity costs for under-resourced schools investing in AI vs. other interventions
- Psychological impacts of AI performance gaps on student confidence and identity
- Accessibility for students with disabilities interacting with AI tutors
- Equity in data collection: whose learning data is being used to train these systems?
- Privacy differentials: which students/schools have data protections vs. those that don't
- Teacher agency and professional development equity in AI-supported classrooms
- Systemic exclusion: which languages, dialects, and content domains are systematically underrepresented in training data?
- Within-country disparities (urban/rural, public/private) in middle-income countries
- Sustainability and maintenance equity: who can afford ongoing model updates and system maintenance?
- Community and parental engagement disparities in AI adoption decisions
- Equity in error impacts: do model mistakes disproportionately harm marginalized students?
- Assessment validity across cultural contexts: are the constructs being measured culturally appropriate?

## Context Factors

- Language of instruction and primary language of students (English vs. non-English, high-resource vs. low-resource languages)
- Geographic context (urban vs. rural, high-income vs. low/middle-income countries)
- Infrastructure availability (connectivity quality, device access, electricity reliability)
- Economic status of students and schools
- Model type and cost (proprietary premium vs. open-source, API-based vs. locally deployed)
- Subject domain (language learning vs. mathematics vs. STEM, text-heavy vs. diagram-heavy)
- Student age and educational level (elementary vs. secondary, beginning vs. advanced)
- Teacher training and digital literacy levels
- Implementation model (1-on-1 tutoring vs. classroom support vs. assessment)
- Data availability for training and fine-tuning (high-resource vs. low-resource scenarios)
- Cultural context and educational system structure
- Parental education levels and attitudes toward technology
- School type (public vs. private, well-resourced vs. under-resourced)
- Policy environment (supportive vs. restrictive regulations around AI in education)
- Availability of local language training data and annotators

## Notable Studies

### Multilingual Performance of a Multimodal Artificial Intelligence System on Multisubject Physics Concept Inventories

**Design:** Benchmark study evaluating GPT-4o on 1,031 ENEM items across 11 languages using standardized physics concept inventories
**Sample:** Physics concept inventories from 11 languages across 7 language families, undergraduate to graduate level content
**Key result:** English consistently outperformed other languages; non-Latin script languages showed greatest performance degradation; diagram-based questions were 10-15% less accurate than text-only across all languages

### Automatic Essay Scoring: Accuracy, Fairness, and Generalizability

**Design:** Comparative study of 9 AES methods on 25,000+ essays with demographic information, testing prompt-specific vs. cross-prompt models
**Sample:** 25,000+ argumentative essays from students with documented gender, economic status, disability status, ELL status, and race information
**Key result:** Prompt-specific models achieved 25.61% higher accuracy but exhibited greater bias toward students of different economic statuses; cross-prompt models more fair but less accurate

### The Impact of Large Language Models on K-12 Education in Rural India

**Design:** Qualitative thematic analysis of semi-structured interviews with 23 student volunteers teaching in rural schools
**Sample:** 23 volunteer teachers in rural Rajasthan and Delhi schools, grades 2-8
**Key result:** Identified infrastructure (connectivity, devices), teacher training, digital literacy, and parental skepticism as primary barriers; 92% supported AI as supplemental tool but cited concerns about over-reliance

### Equity and Fairness of Bayesian Knowledge Tracing

**Design:** Theoretical and simulation study proposing B2KT model; compared equitable learning outcomes vs. prediction fairness (AUC)
**Sample:** Simulated tutoring scenarios and real-world knowledge tracing datasets
**Key result:** Fairness in AUC does not guarantee equitable learning outcomes; B2KT enabled individualized curricula that better maximized knowledge while minimizing effort across diverse learners

### 'I Would Have Written My Code Differently': Beginners Struggle to Understand LLM-Generated Code

**Design:** Lab study with 32 CS1 students measuring code comprehension vs. prompt comprehension for LLM outputs
**Sample:** 32 first-semester CS students, diverse demographics including non-native English speakers
**Key result:** 32.5% success rate on code comprehension vs. 59.3% on prompt comprehension; non-native English speakers showed significantly worse prompt comprehension; students struggled with unfamiliar Python idioms

### Estimating Exam Item Difficulty with LLMs: A Benchmark on Brazil's ENEM Corpus

**Design:** Benchmark of 10 LLMs on 1,031 Brazilian high-stakes exam questions, testing multilingual and multimodal performance with IRT-grounded difficulty labels
**Sample:** 1,031 ENEM questions across 4 subjects (Languages, Human Sciences, Natural Sciences, Mathematics)
**Key result:** English-translated questions improved accuracy from 73.89% to 75.09%; diagram questions showed 10-15% accuracy penalty; proprietary models outperformed open-source but gaps narrowing

## Implications for LMICs

The evidence reveals severe compounding equity challenges for low- and middle-income countries (LMICs). First, infrastructure deficits (connectivity, devices, electricity) create fundamental access barriers documented in rural India and Indonesia studies. Second, linguistic marginalization is acute: LLMs show 15-30% performance degradation for non-English languages, and low-resource languages prevalent in LMICs receive minimal training data and research attention. Third, cost structures are prohibitive: premium API access, computational requirements, and teacher training expenses systematically disadvantage under-resourced LMIC schools. Fourth, the 'data colonialism' dynamic is evident—LMIC students and contexts are underrepresented in training data, yet their educational data may be extracted without equivalent benefit. Fifth, cultural misalignment is systematic: AI systems embed Western educational norms and content that may be inappropriate for LMIC contexts. The research shows that even when technical access exists, effective use requires digital literacy, teacher capacity, and institutional support—all of which are constrained in LMIC settings. Critically, the evidence suggests that without deliberate intervention, AI deployment in education will widen global educational inequality. Promising directions include: prioritizing open-source models with local deployment options, investing in low-resource language NLP, developing context-appropriate content, building in-country AI capacity rather than depending on external vendors, and creating LMIC-led research and development initiatives that center local needs and values.

## Recommendations

- Prioritize and fund research on low-resource language NLP for education, with explicit focus on languages spoken in LMICs and marginalized communities
- Develop and validate open-source educational AI models that can be deployed locally without high-cost API dependencies
- Create equity audits as standard practice for educational AI deployment, measuring not just prediction fairness but learning outcome equity across demographic groups
- Invest in teacher professional development that explicitly addresses AI equity issues, including recognizing and mitigating bias, supporting diverse learners, and maintaining human oversight
- Design AI systems with explicit 'graceful degradation' for low-connectivity contexts (offline modes, low-bandwidth optimization, asynchronous interaction)
- Establish multi-stakeholder governance for educational AI that includes LMIC representation, teachers from under-resourced schools, and marginalized community voices
- Mandate transparency about training data composition, including language distribution, geographic origin, and demographic representation
- Create subsidized or free tiers of educational AI specifically for under-resourced schools and contexts, funded by premium users
- Develop culturally adaptive AI that can be localized not just linguistically but in content, pedagogical approach, and examples
- Support research on 'equity-by-design' approaches: features that actively reduce rather than perpetuate disparities (e.g., scaffolding for non-native speakers, low-resource optimization)
- Require disaggregated performance reporting by demographic factors as standard practice in educational AI evaluation
- Build in-country AI capacity in LMICs through training programs, partnerships, and technology transfer rather than creating dependency on external vendors
- Establish ethical guidelines that explicitly reject 'AI solutionism'—AI should supplement, not replace, investment in fundamental educational infrastructure, teacher salaries, and systemic equity initiatives
- Create early warning systems to detect equity degradation: continuous monitoring of AI impacts on different student populations with mechanisms to halt deployment if harms emerge

## Top Papers

1. **The Impact of Large Language Models on K-12 Education in Rural India**
   Provides rare empirical evidence on AI equity barriers in an LMIC context through direct stakeholder interviews

2. **Automatic Essay Scoring: Accuracy, Fairness, and Generalizability**
   Demonstrates systematic bias by economic status in automated assessment and the accuracy-fairness tradeoff

3. **Multilingual Performance of a Multimodal Artificial Intelligence System on Multisubject Physics Concept Inventories**
   Comprehensively documents language-based performance gaps across 11 languages in a standardized assessment context

4. **Equity and Fairness of Bayesian Knowledge Tracing**
   Reveals that prediction fairness metrics do not guarantee equitable learning outcomes and proposes alternative equity frameworks

5. **The Rise of Artificial Intelligence in Educational Measurement**
   Systematic review of ethical challenges including bias, fairness, and equity in AI-powered educational assessment
