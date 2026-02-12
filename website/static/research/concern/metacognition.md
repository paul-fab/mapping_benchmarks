# Metacognition & Self-regulation

**45 papers matched** (18 directly addressing this concern)

## Executive Summary

The research literature reveals a critical tension: while AI tools can theoretically support metacognitive development through scaffolding and feedback, their current implementations often undermine self-regulated learning processes. Multiple empirical studies document 'cognitive offloading' effects where students delegate thinking to AI systems, resulting in reduced reflection, diminished need for understanding, and weaker strategic thinking. Students show consistent over-reliance on AI-generated outputs even when they possess sufficient knowledge to solve problems independently, with some studies finding acceptance rates of incorrect AI suggestions as high as 52.1%. This over-reliance is particularly pronounced among students with higher technophilic traits and those who trust AI systems more, creating a paradoxical situation where the students most enthusiastic about technology may be most vulnerable to its cognitive costs.

However, carefully designed AI systems that explicitly target metacognitive processes show promise. Systems incorporating Socratic questioning, error-based learning through erroneous examples, explicit self-assessment prompts, and adaptive scaffolding within students' Zone of Proximal Development demonstrate significant improvements in metacognitive awareness and self-regulatory behaviors. The key distinction appears to be between AI tools designed to provide answers (which promote passivity) versus those designed to prompt thinking (which develop agency). Effective implementations combine AI capabilities with human oversight, use structured pedagogical frameworks, and deliberately require cognitive effort from students rather than minimizing it. The evidence suggests that metacognitive outcomes depend critically on design choices: the same underlying technology can either enhance or erode self-regulated learning depending on how it is implemented and pedagogically framed.

## Key Findings

### Trust-driven routine use of generative AI significantly reduces cognitive engagement (reflection, need for understanding, critical thinking) in STEM coursework, with effect sizes ranging from small (f²=0.12) to large (f²=0.51)

*Evidence type: empirical | 3 papers*

- Why Johnny Can't Think: GenAI's Impacts on Cognitive Engagement
- ChatGPT produces more "lazy" thinkers: Evidence of cognitive engagement decline
- Short-term AI literacy intervention does not reduce over-reliance on incorrect ChatGPT suggestions

### Students exhibit systematic over-reliance on AI outputs even when incorrect, with acceptance rates of wrong suggestions ranging from 41.7% to 52.1%, and this behavior persists despite AI literacy interventions

*Evidence type: empirical | 5 papers*

- MetaCLASS: Metacognitive Coaching for Learning with Adaptive Self-regulation Support
- Short-term AI literacy intervention does not reduce over-reliance on incorrect ChatGPT suggestions
- Investigating Middle School Students Question-Asking and Answer-Evaluation Skills When Using ChatGPT
- Why it is worth making an effort with GenAI

### AI tutoring systems that explicitly incorporate metacognitive scaffolding (self-assessment prompts, error detection, Socratic questioning) significantly improve metacognitive awareness and self-regulatory behaviors compared to systems providing direct answers

*Evidence type: empirical | 8 papers*

- Metacognitive Practice Makes Perfect: Improving Students' Self-Assessment Skills With an Intelligent Tutoring System
- MetaCLASS: Metacognitive Coaching for Learning with Adaptive Self-regulation Support
- GPT-3-Driven Pedagogical Agents to Train Children's Curious Question-Asking Skills
- BEETLE II: Deep Natural Language Understanding and Automatic Feedback Generation
- Enhancing Critical Thinking in Education by means of a Socratic Chatbot

### Erroneous examples (showing mistakes for students to find and fix) lead to deeper learning and better delayed retention compared to traditional problem-solving, particularly when combined with self-explanation prompts

*Evidence type: empirical | 2 papers*

- Delayed Learning Effects with Erroneous Examples: a Study of Learning Decimals with a Web-Based Tutor
- Using Generative AI and Multi-Agents to Provide Automatic Feedback

### Students with higher technophilic motivations, greater computer self-efficacy, and higher risk tolerance show significantly greater vulnerability to AI-related cognitive disengagement

*Evidence type: empirical | 2 papers*

- Why Johnny Can't Think: GenAI's Impacts on Cognitive Engagement
- ChatGPT produces more "lazy" thinkers: Evidence of cognitive engagement decline

### Middle school students struggle with effective questioning (86.6% produce only emotion words or simple modifiers) and critical evaluation (low recall, inability to detect AI hallucinations) when using ChatGPT, even in domains where they report strong prior knowledge

*Evidence type: empirical | 2 papers*

- Investigating Middle School Students Question-Asking and Answer-Evaluation Skills When Using ChatGPT
- ChatGPT-5 in Secondary Education: A Mixed-Methods Analysis

### Adaptive systems using reinforcement learning to maintain tasks within students' Zone of Proximal Development show improvements in metacognitive skills and self-regulated learning compared to fixed-difficulty systems

*Evidence type: empirical | 3 papers*

- AI-based adaptive personalized content presentation and exercises navigation
- Improved Performances and Motivation in Intelligent Tutoring Systems: Combining Machine Learning and Learner Choice
- UCO: A Multi-Turn Interactive Reinforcement Learning Method for Adaptive Teaching

### Fine-tuned LLMs for educational assessment can predict student performance but struggle with knowledge tracing (identifying when students truly understand vs. memorize) and providing pedagogically appropriate feedback that promotes metacognition

*Evidence type: empirical | 4 papers*

- FoundationalASSIST: An Educational Dataset for Foundational Knowledge Tracing
- Problems With Large Language Models for Learner Modelling
- A Chain-of-Thought Prompting Approach with LLMs for Evaluating Students' Formative Assessment Responses
- BD at BEA 2025 Shared Task: MPNet Ensembles for Pedagogical Mistake Identification

### Automated writing evaluation systems reduce teacher workload but students tend to focus on scores rather than learning from feedback, potentially undermining metacognitive engagement with revision processes

*Evidence type: empirical | 3 papers*

- Effectiveness of automated writing evaluation systems in school settings
- AI-Enhanced Writing Self-Assessment: Empowering Student Revision with AI Tools
- Generative AI in K-12 Education: The CyberScholar Initiative

### Students develop 'epistemic safeguarding' strategies after encountering AI hallucinations, restricting AI use to domains where they already have knowledge—a metacognitive adaptation that limits over-reliance but also constrains AI's potential to introduce new knowledge

*Evidence type: empirical | 2 papers*

- ChatGPT-5 in Secondary Education: A Mixed-Methods Analysis
- Investigating Middle School Students Question-Asking and Answer-Evaluation Skills When Using ChatGPT

## Evidence For This Risk

- Quantitative studies document systematic cognitive disengagement: students using ChatGPT show 66% reduction in reflection, 21% reduction in need for understanding, and 41% reduction in critical thinking (Choudhuri et al.)
- Neurophysiological evidence shows LLM use reduces neural connectivity, memory recall, and sense of ownership compared to brain-only and search-based approaches (Kosmyna et al., 2025)
- Students accept incorrect AI suggestions 52.1% of the time despite knowing better, and AI literacy interventions fail to reduce this over-reliance (Short-term AI literacy intervention study)
- Middle school students demonstrate inability to critically evaluate AI responses: only 9% of prompts reach sophisticated levels of questioning, and students fail to identify hallucinations even in familiar domains
- 59.3% reduction in debugging time when using AI tutors correlates with reduced opportunity to develop problem-solving metacognition
- Students report decreased mental effort, attention, and strategic thinking when routinely using AI for academic tasks, with correlation coefficients showing strong negative associations (r = -0.66 for reflection)
- Even when AI provides pedagogically sound feedback, students' focus on scores rather than learning processes undermines metacognitive engagement with revision
- Over-reliance is amplified in high-trust, routine-use scenarios: students who trust AI more show even lower cognitive engagement when usage is high
- LLMs fine-tuned for education struggle with knowledge tracing—distinguishing genuine understanding from memorization—achieving only 43.2% accuracy on metacognitive coaching tasks
- Students develop surface-level interactions with AI, prioritizing task completion over understanding, particularly when systems optimize for efficiency rather than cognitive engagement

## Mitigating Evidence

- Intelligent tutoring systems explicitly designed for metacognition show large effect sizes: self-assessment tutor improved students' ability to identify knowledge strengths/weaknesses with transfer to unsupported sections
- Socratic chatbots increase students' cognitive engagement from 2.95 to 4.19 on 5-point scale when using structured questioning frameworks
- Erroneous examples combined with self-explanation produce better delayed retention (d=0.33) and reduce misconceptions more effectively than traditional problem-solving
- Knowledge-building dialogues in IntelliChain framework enable LLMs to support deeper inquiry when combined with knowledge graphs and structured pedagogical principles
- Adaptive systems using ZPD-aligned scaffolding show 34% improvement in coding proficiency and better metacognitive skill development
- Multi-LoRA fine-tuning with pedagogical frameworks improves MLLM alignment from 0.468 to 0.653 correlation with expert educational assessments
- Human-in-the-loop oversight significantly improves AI tutoring outcomes: supervised AI tutoring matches or exceeds human-only tutoring (66.2% vs 60.7% success rate)
- Students who interact with AI systems that deliberately introduce errors and require detection/correction show enhanced critical thinking and metacognitive awareness
- Gamification combined with adaptive personalization (Odychess approach) shows students can develop metacognitive chess skills when AI acts as Socratic tutor rather than answer provider
- Teacher training in prompt engineering and pedagogical AI integration can mitigate risks: educators report AI tools enhance rather than replace their instructional role when properly implemented
- Systems that require students to critique and improve AI outputs (rather than passively accept them) show preservation of cognitive engagement and critical thinking
- Hybrid human-AI approaches where AI provides scaffolding but humans maintain pedagogical control show better metacognitive outcomes than fully automated systems

## What Is Being Measured

- Cognitive engagement scales measuring reflection, need for understanding, critical thinking, mental effort, attention, and strategic thinking
- Self-assessment accuracy: students' ability to evaluate their own knowledge relative to actual performance
- Help-seeking appropriateness: whether students request assistance at pedagogically optimal moments
- Metacognitive monitoring: students' ability to judge when they understand vs. when confused
- Self-explanation quality: depth and accuracy of students' reasoning about their work
- Question-asking sophistication: use of cognitive taxonomy (Bloom's) to classify question depth and specificity
- Critical evaluation skills: ability to detect errors, hallucinations, and inconsistencies in AI outputs
- Time on task and debugging time as proxies for cognitive effort
- Over-reliance rates: frequency of accepting incorrect AI suggestions when student could solve independently
- Trust calibration: alignment between confidence in AI and actual AI accuracy
- Knowledge tracing accuracy: systems' ability to distinguish genuine understanding from memorization
- Transfer of learning: performance on novel problems after AI-assisted practice
- Delayed retention: learning persistence measured days/weeks after intervention
- Metacognitive strategy use: frequency of planning, monitoring, and evaluation behaviors
- Self-efficacy and perceived competence in learning domains
- Epistemic curiosity and intrinsic motivation measures
- Neural connectivity patterns (fMRI/EEG) during AI-assisted vs. independent learning

## Gaps — What Is NOT Being Measured

- Long-term developmental trajectories of metacognitive skills: most studies are short-term (weeks to months) rather than following students across years
- Transfer of metacognitive skills across domains: whether learning to self-regulate in one subject (e.g., math) transfers to others (e.g., science)
- Metacognitive discourse quality in classroom settings: how AI tools affect students' ability to explain thinking to peers and teachers
- Development of epistemic agency: students' sense of themselves as knowledge producers rather than knowledge consumers
- Metacognitive calibration accuracy over time: whether students improve at judging when they need help vs. when they understand
- Opportunity costs: what metacognitive skills are NOT developed due to time spent with AI vs. traditional methods
- Social metacognition: how AI use affects collaborative metacognitive processes and peer learning
- Motivational dynamics: how initial engagement with AI evolves into routine dependence or mature, strategic use
- Cultural variations in metacognitive development with AI: most studies are WEIRD populations (Western, Educated, Industrialized, Rich, Democratic)
- Metacognitive strategy sophistication: progression from simple monitoring to complex self-regulated learning cycles
- Attribution patterns: whether students credit learning to themselves vs. AI, and how this affects self-concept
- Resilience and productive struggle: whether AI reduces students' tolerance for difficulty and uncertainty
- Real-time metacognitive monitoring during AI use: most measures are post-hoc self-reports rather than in-situ observations
- Comparative effectiveness across AI types: systematic comparison of chatbots vs. ITS vs. RAG systems vs. copilots for metacognitive outcomes
- Threshold effects: minimum cognitive effort required for skill development and whether AI crosses that threshold

## Context Factors

- Age/developmental stage: younger students (elementary) show different patterns than adolescents and adults; metacognitive skills are still developing in K-12
- Prior domain knowledge: students with stronger knowledge show better critical evaluation but may also show greater over-reliance if highly trusting
- Cognitive styles: technophilic students, those with higher computer self-efficacy, and risk-tolerant individuals are more vulnerable to cognitive disengagement
- Trust in AI: higher trust predicts more routine use which predicts lower cognitive engagement (mediation effect)
- Task structure: open-ended vs. closed problems, with open-ended showing greater vulnerability to over-reliance
- AI system design: answer-providing vs. questioning systems produce dramatically different metacognitive outcomes
- Pedagogical framing: whether AI is presented as tutor, tool, or partner affects student engagement patterns
- Presence of human oversight: supervised AI tutoring shows better outcomes than fully autonomous systems
- Feedback type: immediate correctness feedback vs. metacognitive prompts (e.g., 'explain your thinking') produce different learning
- Cultural context: collectivist vs. individualist educational cultures may interact differently with AI scaffolding
- Assessment pressure: high-stakes testing environments may increase over-reliance compared to low-stakes learning
- Subject domain: mathematics shows different patterns than writing or science; some domains more amenable to metacognitive AI support
- Curriculum alignment: systems matching teachers' pedagogical goals vs. generic AI tools show different engagement patterns
- Duration of use: short-term studies show different patterns than longer classroom integration
- Resource availability: access to human teacher support moderates AI effects on metacognition
- Language proficiency: EFL/ESL contexts show different metacognitive challenges with language-based AI tools

## Notable Studies

### Why Johnny Can't Think: GenAI's Impacts on Cognitive Engagement

**Design:** Structural equation modeling of survey data using Partial Least Squares-SEM
**Sample:** 299 STEM university students across five North American universities
**Key result:** Trust-driven routine GenAI use predicted large negative effects on reflection (β=-0.66, f²=0.51), with students showing reduced mental effort, attention, and strategic thinking

### MetaCLASS: Metacognitive Coaching for Learning with Adaptive Self-regulation Support

**Design:** Framework evaluation with turn-level annotation of 1,015 conversations (7,711 turns) validated against teacher judgments
**Sample:** Middle school Earth Science curriculum; synthetic student-tutor dialogues with validation by 31 teachers
**Key result:** Fine-tuned Mistral-7B achieved only 43.2% accuracy on predicting appropriate metacognitive coach moves, with severe compulsive intervention bias (predicted restraint only 4.2% of times when needed)

### Short-term AI literacy intervention does not reduce over-reliance on incorrect ChatGPT suggestions

**Design:** Experimental study with control vs. intervention (AI literacy training) groups on math puzzle tasks
**Sample:** 340 high school seniors (age 16) in Greek high schools
**Key result:** Students accepted incorrect ChatGPT suggestions 52.1% of the time; AI literacy intervention failed to reduce over-reliance and instead increased rejection of correct recommendations

### Delayed Learning Effects with Erroneous Examples: a Study of Learning Decimals with a Web-Based Tutor

**Design:** Randomized controlled trial comparing erroneous examples vs. problem-solving, with immediate and delayed posttests
**Sample:** 390 middle school students learning decimals
**Key result:** Erroneous examples group showed superior delayed retention (d=0.33) despite lower liking ratings, demonstrating 'desirable difficulty' effects

### Metacognitive Practice Makes Perfect: Improving Students' Self-Assessment Skills With an Intelligent Tutoring System

**Design:** Classroom study with intelligent tutoring system providing self-assessment practice, measuring transfer to unsupported tasks
**Sample:** 84 students (Grades 7-8) in three middle schools
**Key result:** Students improved ability to identify knowledge strengths/weaknesses and showed significant transfer to Geometry Cognitive Tutor sections without SA support

### Investigating Middle School Students Question-Asking and Answer-Evaluation Skills When Using ChatGPT

**Design:** Mixed-methods study analyzing question quality, answer evaluation, and learning outcomes with ChatGPT for science investigation
**Sample:** 63 middle school students (ages 14-15) in French schools
**Key result:** 86.6% of prompts were low-quality (emotion words/simple modifiers); students showed weak critical evaluation with 56.2% resolving misconceptions vs. 66.2% with effective prompting; self-reported AI understanding negatively correlated with actual skills

### AI tutoring can safely and effectively support students: An exploratory RCT in UK classrooms

**Design:** Randomized controlled trial with supervised AI tutoring (human tutors reviewed all AI messages) vs. human-only tutoring
**Sample:** 165 UK secondary school mathematics students
**Key result:** Supervised AI tutoring showed 5.5 percentage point improvement in knowledge transfer to novel problems (66.2% vs 60.7%) compared to human-only tutoring

### GPT-3-Driven Pedagogical Agents to Train Children's Curious Question-Asking Skills

**Design:** Field study comparing human-generated vs. GPT-3-generated pedagogical content with choice conditions, measuring question quality using Bloom's taxonomy
**Sample:** 75 children aged 9-10 in French primary schools
**Key result:** Open-ended GPT-3 cues (allowing multiple questions) produced better question-asking performance than closed cues or human-generated content; students with higher curiosity trait showed stronger correlation with QA skills only in open condition

### ONLINE Functional literacy, iNTELLIGENT TUTORING SYSTEMS AND SCIENCE EDUCATION

**Design:** Comparison of intelligent tutoring system (TECH8) vs. conventional teaching using national assessment data
**Sample:** 77 elementary school students (8th grade) in Technology and Science course
**Key result:** ITS achieved large effect size (d>1σ) improvement for students who followed rules, but 24.7% of students exhibited gaming behaviors (random clicking, minimal time), highlighting metacognitive self-regulation challenges

### ChatGPT-5 in Secondary Education: A Mixed-Methods Analysis

**Design:** Mixed-methods evaluation of ChatGPT use across multiple task modalities with SATAI and AIAS measures plus interviews
**Sample:** 109 sixteen-year-old students from three Greek high schools
**Key result:** Students developed 'epistemic safeguarding' strategy after encountering hallucinations, restricting AI use to domains where they could verify answers; 75.3% achieved better results but 24.7% showed concerning patterns

## Implications for LMICs

The metacognitive risks of AI tools may be amplified in LMIC contexts through several mechanisms. First, overcrowded classrooms with limited teacher supervision increase reliance on autonomous AI systems without the human oversight shown to be critical for metacognitive development. Studies show supervised AI tutoring produces better outcomes than unsupervised use, but LMIC settings often lack sufficient teachers to provide this supervision. Second, infrastructure constraints (intermittent connectivity, shared devices) may push students toward efficiency-focused interactions rather than reflective engagement. Third, when AI tools are introduced as 'solutions' to teacher shortages rather than complementary supports, students may develop dependencies without developing metacognitive skills that would enable independent learning. Fourth, cultural contexts emphasizing teacher authority and exam performance may reduce students' critical evaluation of AI outputs—the 'epistemic safeguarding' strategy documented in European contexts may not emerge if students are socialized to accept rather than question authoritative sources. Fifth, language barriers and use of AI systems trained primarily on Global North languages may reduce students' ability to critically evaluate outputs or articulate metacognitive processes. However, LMIC contexts also present opportunities: some educational cultures place stronger emphasis on collaborative learning and peer interaction, which could mitigate individual over-reliance if AI tools are integrated into group work. Additionally, resource constraints may prevent the 'compulsive intervention bias' seen in well-resourced contexts if AI access is rationed. The key implication is that LMIC implementation of AI tools must explicitly design for metacognitive development rather than assuming it will emerge naturally, particularly given reduced availability of human mediation that research shows is critical for productive AI use in education.

## Recommendations

- Design AI educational tools with explicit metacognitive scaffolding: incorporate self-assessment prompts, require students to explain reasoning before receiving AI support, and use Socratic questioning rather than direct answer provision
- Implement human-in-the-loop systems rather than fully autonomous AI: research shows supervised AI tutoring outperforms unsupervised, and teacher oversight is critical for metacognitive development
- Use 'productive struggle' design: deliberately maintain appropriate difficulty within students' ZPD rather than minimizing cognitive load; incorporate erroneous examples and error detection tasks
- Train students in metacognitive strategies before AI tool introduction: explicit instruction in self-monitoring, strategic questioning, and critical evaluation of AI outputs
- Avoid designing for efficiency optimization: systems should require cognitive effort rather than minimizing it, as 'desirable difficulties' produce better learning even when students report lower satisfaction
- Conduct routine embedding audits for bias and alignment: when using open-response assessment with AI, systematically evaluate semantic encoders for demographic fairness and pedagogical appropriateness
- Implement transparency mechanisms: provide students with explanations of why specific exercises or feedback are recommended, supporting metacognitive understanding of learning processes
- Design hybrid human-AI systems: position AI as tool that augments rather than replaces teacher judgment, with clear delineation of when human intervention is needed
- Create longitudinal monitoring systems: track not just performance but metacognitive indicators (question quality, evaluation accuracy, help-seeking appropriateness) over time
- Establish pedagogical guardrails: use structured frameworks (e.g., Bloom's taxonomy, ZPD principles, knowledge tracing) to constrain AI behavior toward metacognitively productive interactions
- Provide teachers with professional development in AI pedagogy: educators need training in recognizing over-reliance, supporting metacognitive development with AI tools, and balancing efficiency with cognitive engagement
- Implement features that require student critique of AI outputs: design interactions where students must evaluate, improve, or justify AI suggestions rather than passively accept them
- Use adaptive personalization that maintains challenge: systems should adjust difficulty to keep students in productive struggle zone rather than adapting to eliminate errors
- Design for knowledge-building dialogue rather than answer-seeking: incorporate features that support iterative refinement, multiple perspectives, and conceptual understanding rather than solution delivery
- Develop and validate metacognitive assessment instruments specific to AI-mediated learning: current measures may not capture unique patterns of self-regulation in AI contexts

## Top Papers

1. **Why Johnny Can't Think: GenAI's Impacts on Cognitive Engagement**
   Largest-scale quantitative study documenting systematic cognitive disengagement effects with rigorous structural equation modeling and identification of vulnerability factors

2. **MetaCLASS: Metacognitive Coaching for Learning with Adaptive Self-regulation Support**
   Operationalizes metacognitive tutoring as interpretable action space aligned to self-regulated learning theory, revealing LLMs' systematic failures at metacognitive coaching despite strong content knowledge

3. **Short-term AI literacy intervention does not reduce over-reliance on incorrect ChatGPT suggestions**
   Demonstrates that awareness-based interventions fail to mitigate over-reliance, challenging assumption that the problem can be solved through user education

4. **Investigating Middle School Students Question-Asking and Answer-Evaluation Skills When Using ChatGPT**
   First comprehensive study of metacognitive evaluation skills in middle school students using ChatGPT, documenting severe deficits even in domains of reported strong knowledge

5. **Metacognitive Practice Makes Perfect: Improving Students' Self-Assessment Skills With an Intelligent Tutoring System**
   Shows that explicitly designed self-assessment tutoring can improve metacognitive skills with transfer to unsupported learning contexts, demonstrating what works

6. **Delayed Learning Effects with Erroneous Examples: a Study of Learning Decimals with a Web-Based Tutor**
   Demonstrates 'desirable difficulty' principle with AI tutoring: making learning harder (error detection) produces better long-term outcomes despite lower immediate satisfaction

7. **AI tutoring can safely and effectively support students: An exploratory RCT in UK classrooms**
   Rigorous RCT showing that human-supervised AI tutoring can match/exceed human-only outcomes, establishing the importance of hybrid approaches

8. **ChatGPT-5 in Secondary Education: A Mixed-Methods Analysis**
   Documents 'epistemic safeguarding' as adaptive metacognitive response to AI hallucinations, showing students can develop protective strategies but with limitations


---

# Metacognition & Self-regulation

**49 papers matched** (12 directly addressing this concern)

## Executive Summary

The literature reveals a complex relationship between AI/LLM tools and students' metacognitive and self-regulatory capabilities. While some studies demonstrate AI systems explicitly designed to support self-regulated learning (SRL)—through features like adaptive scaffolding, personalized feedback, and metacognitive prompting—other research raises concerns about cognitive offloading and 'metacognitive laziness.' The most direct evidence comes from studies examining AI tutoring systems, intelligent learning environments, and generative AI tools in educational contexts. Key findings suggest that AI can support metacognition when intentionally designed with scaffolding for planning, monitoring, and reflection, but passive or over-reliant use may reduce students' engagement with these critical self-regulatory processes. The concern is particularly salient with generative AI tools like ChatGPT, where students may bypass effortful metacognitive processes by accepting AI-generated solutions without critical evaluation or self-assessment. However, the evidence base remains limited, with most studies focusing on system design rather than longitudinal impacts on metacognitive development.

Critically, the literature distinguishes between AI systems that 'do metacognition for students' versus those that 'support students doing metacognition.' Systems incorporating explicit metacognitive scaffolds—such as prompts for self-explanation, reflection, goal-setting, and progress monitoring—show more promise for supporting rather than replacing metacognitive engagement. Several papers highlight the importance of maintaining 'desirable difficulties' and ensuring students retain agency over their learning process. The risk appears highest when AI provides complete solutions or takes over regulatory functions without requiring student engagement in planning, monitoring, or evaluative processes. Context factors matter significantly: younger learners, novices in a domain, and students with weaker self-regulatory skills may be more vulnerable to over-reliance. The integration of AI into formative assessment and the design of 'AI-aware' learning activities emerge as critical areas requiring further research and careful instructional design.

## Key Findings

### AI systems can support self-regulated learning when explicitly designed with metacognitive scaffolding features (prompts for planning, monitoring, self-assessment, reflection)

*Evidence type: empirical | 8 papers*

- Learning to Live with AI: How Students Develop AI Literacy Through Naturalistic ChatGPT Interaction
- A Practical Guide for Supporting Formative Assessment and Feedback Using Generative AI
- RPKT: Learning What You Don't Know - Recursive Prerequisite Knowledge Tracing
- Learner and Instructor Needs in AI-Supported Programming Learning Tools

### Overreliance on AI may lead to 'metacognitive laziness' or cognitive offloading, where learners bypass effortful self-monitoring and self-evaluation processes

*Evidence type: empirical | 5 papers*

- Beware of Metacognitive Laziness: Effects of Generative Artificial Intelligence on Learning Motivation, Processes, and Performance
- When Peers Outperform AI (and When They Don't): Interaction Quality Over Modality
- extraheric AI
- Challenges and opportunities for classroom-based formative assessment and AI

### AI-assisted learning can reduce perceived task difficulty and effort, potentially leading to less engagement with metacognitive processes like self-monitoring and strategy adjustment

*Evidence type: empirical | 3 papers*

- Beware of Metacognitive Laziness: Effects of Generative Artificial Intelligence on Learning Motivation, Processes, and Performance
- When Peers Outperform AI (and When They Don't): Interaction Quality Over Modality
- Exploring User Perspectives on ChatGPT: Applications, Perceptions, and Implications for AI-Integrated Education

### AI can improve knowledge confidence and procedural performance without necessarily enhancing deeper metacognitive skills or knowledge transfer

*Evidence type: empirical | 4 papers*

- Beware of Metacognitive Laziness: Effects of Generative Artificial Intelligence on Learning Motivation, Processes, and Performance
- When Peers Outperform AI (and When They Don't): Interaction Quality Over Modality
- Principles of cognitive science in education: The effects of generation, errors, and feedback
- KARL: Knowledge-Aware Retrieval and Representations aid Retention and Learning in Students

### Systems incorporating user control, transparency, and opportunities for self-assessment show better outcomes for maintaining metacognitive engagement

*Evidence type: empirical | 6 papers*

- Learner and Instructor Needs in AI-Supported Programming Learning Tools
- A Practical Guide for Supporting Formative Assessment and Feedback Using Generative AI
- Learning to Live with AI: How Students Develop AI Literacy Through Naturalistic ChatGPT Interaction
- Fine-Tuned Large Language Model for Visualization System: A Study on Self-Regulated Learning in Education

### The type of feedback and level of scaffolding matter: task-level feedback alone is insufficient; process-level and self-regulation feedback are needed to support metacognitive development

*Evidence type: theoretical | 3 papers*

- A Practical Guide for Supporting Formative Assessment and Feedback Using Generative AI
- Feedback Generation through Artificial Intelligence
- Improving Assessment of Tutoring Practices using Retrieval-Augmented Generation

### Students develop 'repair literacy' and metacognitive awareness through experiencing and resolving AI system failures or limitations

*Evidence type: empirical | 2 papers*

- Learning to Live with AI: How Students Develop AI Literacy Through Naturalistic ChatGPT Interaction
- Learner and Instructor Needs in AI-Supported Programming Learning Tools

### High-quality peer collaboration generates more curiosity, metacognitive engagement, and deeper learning than AI interaction, though AI provides more consistent knowledge delivery

*Evidence type: empirical | 2 papers*

- When Peers Outperform AI (and When They Don't): Interaction Quality Over Modality
- A Computational Model of Inclusive Pedagogy: From Understanding to Application

## Evidence For This Risk

- Experimental evidence showing AI users exhibited fewer metacognitive processes (evaluation, orientation) and more closed-loop interaction with AI compared to those working with human experts (Beware of Metacognitive Laziness)
- AI group showed significantly improved essay scores but no significant differences in knowledge gain or transfer, suggesting surface-level performance improvement without deeper learning (Beware of Metacognitive Laziness)
- Students reported less curiosity and deeper engagement when using AI compared to high-quality peer collaboration, indicating reduced metacognitive activation (When Peers Outperform AI)
- AI users exhibited 'confidence without curiosity' pattern—increased procedural confidence but decreased exploration and question-asking behaviors (When Peers Outperform AI, Beware of Metacognitive Laziness)
- Temporal analysis of learning behaviors showed AI users formed closed loops between content and AI consultation, with fewer transitions to planning, monitoring, and evaluation processes (Beware of Metacognitive Laziness)
- Qualitative reports of students preferring AI over critical thinking, with concerns about 'encouraging superficial learning habits and eroding students' social and critical thinking skills' (Exploring User Perspectives on ChatGPT)
- Evidence that AI reduces perceived difficulty and cognitive disfluency, potentially preventing activation of deeper analytical reasoning (System 2 processes) (Beware of Metacognitive Laziness)
- Students treating AI as transactional information source rather than collaborative partner, ignoring prompts designed to encourage metacognitive engagement (When Peers Outperform AI)

## Mitigating Evidence

- AI systems explicitly designed with metacognitive scaffolding (reflection prompts, progress monitoring, self-assessment tools) successfully support self-regulated learning (Fine-Tuned LLM for Visualization System, RPKT, A Practical Guide for Supporting Formative Assessment)
- Students who developed 'repair literacy' through handling AI failures showed enhanced metacognitive awareness and critical evaluation skills (Learning to Live with AI)
- Hybrid human-AI approaches that preserve student agency while providing AI support show promise for maintaining metacognitive engagement (Learner and Instructor Needs in AI-Supported Programming Learning)
- Context-aware and personalized AI systems that adapt to individual metacognitive needs can enhance rather than replace self-regulation (Fine-Tuned LLM for Visualization System)
- Instructor guidance and structured learning activities can mitigate risks by ensuring students use AI as scaffolding rather than replacement (A Practical Guide for Supporting Formative Assessment)
- AI can support metacognitive monitoring through visualization of learning progress and knowledge gaps (Fine-Tuned LLM for Visualization System, KARL)
- Longitudinal naturalistic use studies suggest students develop increasingly sophisticated strategic use of AI over time, including metacognitive genre portfolios (Learning to Live with AI)
- Explicit AI literacy instruction helps students understand AI limitations and maintains critical evaluation stance (Learning to Live with AI)

## What Is Being Measured

- Frequency of metacognitive processes (planning, monitoring, evaluation) during learning sessions using temporal process mining and learning trace analysis
- Self-reported intrinsic motivation and perceived competence using instruments like the Intrinsic Motivation Inventory (IMI)
- Knowledge transfer performance on novel tasks versus immediate task performance
- Curiosity and engagement indicators (question-asking frequency, exploration of new ideas, self-reported interest)
- Learning behavior sequences and transitions between cognitive and metacognitive processes
- Self-efficacy and confidence measures through pre/post surveys
- Accuracy of self-assessment and calibration (comparing students' judgments of learning with actual performance)
- Time allocation and effort investment patterns across learning activities
- Discourse features indicating metacognitive engagement (self-explanation quality, reflection depth)
- Preferences for learner control versus system control in adaptive learning environments

## Gaps — What Is NOT Being Measured

- Longitudinal impacts on metacognitive skill development over months/years of AI tool use
- Transfer of metacognitive skills across domains and contexts (from AI-supported to non-AI contexts)
- Developmental differences in metacognitive vulnerability across age groups (elementary vs. secondary vs. tertiary)
- Interaction effects between individual differences in metacognitive ability and AI tool design features
- Quality of metacognitive strategies developed (not just frequency) and their sophistication over time
- Impact on epistemic cognition—how students think about knowledge and knowing when using AI
- Effects on academic self-concept and learner identity related to metacognitive competence
- Comparison of metacognitive engagement across different AI tool types (tutoring systems vs. generative AI vs. assessment tools)
- Real-world consequences of reduced metacognitive engagement (e.g., performance in high-stakes assessments, workplace learning)
- Remediation effectiveness—whether and how metacognitive skills can be recovered after extended AI-dependent learning
- Cultural and contextual factors affecting metacognitive engagement with AI tools
- Interaction patterns with AI that distinguish surface-level use from deeper metacognitive engagement

## Context Factors

- Age and developmental stage: younger learners may have less developed metacognitive skills to maintain against AI dependency
- Domain expertise: novices vs. experts show different patterns of AI reliance and metacognitive engagement
- Task type: procedural vs. conceptual learning, knowledge acquisition vs. knowledge application
- AI tool design: presence/absence of metacognitive scaffolds, level of system control vs. learner control
- Interaction modality: whether AI provides complete solutions vs. prompts/questions vs. adaptive scaffolding
- Instructional framing: whether AI is positioned as tool vs. tutor vs. collaborator
- Individual differences: students' baseline self-regulatory skills, motivation, self-efficacy
- Quality of alternative support: availability of peer collaboration or instructor guidance
- Assessment context: formative vs. summative, low-stakes practice vs. high-stakes testing
- Time pressure and workload: increased pressure may drive more AI dependency
- Subject area: domains with clear right answers (math, programming) vs. open-ended (writing, design)
- Educational level: K-12 vs. higher education vs. professional training
- Duration of AI use: short-term experimental settings vs. sustained classroom integration
- Cultural factors: educational traditions emphasizing memorization vs. critical thinking

## Notable Studies

### Beware of Metacognitive Laziness: Effects of Generative Artificial Intelligence on Learning Motivation, Processes, and Performance

**Design:** Randomized experimental study comparing university students (N=117) learning with ChatGPT, human experts, writing analytics tools, or no support on an essay task. Used temporal process mining and learning trace analysis to examine self-regulated learning processes.
**Sample:** 117 university students (70% female), undergraduate level, 30-45 minute writing task
**Key result:** ChatGPT group showed significantly improved essay scores but no knowledge transfer gains. Exhibited fewer metacognitive processes (evaluation, orientation) and more closed-loop AI interaction patterns. Suggested 'metacognitive laziness' where learners offload cognitive effort to AI.

### When Peers Outperform AI (and When They Don't): Interaction Quality Over Modality

**Design:** Comparative study of 36 undergraduate students learning graph theory through peer-peer collaboration (n=24) or AI assistance (n=12). Used discourse analysis to identify interaction patterns and compared outcomes on multiple dimensions.
**Sample:** 36 undergraduate students in graph theory course, university level
**Key result:** High-quality peer interactions generated significantly higher curiosity and engagement than AI. AI built confidence without curiosity ('confidence without curiosity' pattern). AI users showed less metacognitive process associations compared to human tutoring.

### Learning to Live with AI: How Students Develop AI Literacy Through Naturalistic ChatGPT Interaction

**Design:** Longitudinal analysis of 10,536 ChatGPT messages from 36 undergraduates over one academic year. Identified five use genres including 'metacognitive partner' and examined development of 'repair literacy'.
**Sample:** 36 undergraduate students, naturalistic use over full academic year, ages 18-22
**Key result:** Students developed sophisticated genre portfolios for strategic AI use, including metacognitive facilitation. 'Repair literacy' through handling AI breakdowns produced substantial learning about AI capabilities. Supports view that competence emerges through relational negotiation rather than one-time adoption.

### Learner and Instructor Needs in AI-Supported Programming Learning Tools

**Design:** Participatory design study with 15 undergraduate novice programmers and 10 instructors, plus follow-up survey (N=172). Explored desired help features and learner-system control preferences through qualitative analysis.
**Sample:** 15 undergraduate programmers (novices) and 10 instructors, plus 172 survey respondents, K-12 computer programming context
**Key result:** Learners with higher self-efficacy desired greater control over level of help. Preferences for control varied by metacognitive factors. Highlighted importance of balanced learner-system control to maintain metacognitive engagement while providing support.

### Fine-Tuned Large Language Model for Visualization System: A Study on Self-Regulated Learning in Education

**Design:** Development and evaluation of Tailor-Mind system using fine-tuned LLM for AI beginners. Included model performance evaluation and user study examining self-regulated learning outcomes.
**Sample:** AI education beginners, university level, system design and evaluation study
**Key result:** System supporting SRL through receive, respond, value, organize, and internalise stages showed effectiveness in promoting scientific, active, and iterative self-regulated learning. Demonstrated that explicit SRL scaffolding in AI systems supports metacognitive engagement.

### A Practical Guide for Supporting Formative Assessment and Feedback Using Generative AI

**Design:** Framework paper synthesizing research on using LLMs for formative assessment. Provides guiding principles and example prompts for supporting different levels of feedback (task, process, self-regulation).
**Sample:** Framework and guidance paper, not empirical study
**Key result:** Distinguishes between task-level, process-level, and self-regulation feedback. Argues current LLM applications often focus on task feedback, missing critical metacognitive support. Provides framework for designing metacognitive prompts.

## Implications for LMICs

The metacognition and self-regulation concern has particularly critical implications for low- and middle-income countries (LMICs). First, educational contexts in many LMICs already emphasize rote learning and memorization over metacognitive skill development, meaning students may have less robust metacognitive foundations to maintain against AI dependency. Second, if AI tools become primary learning resources due to teacher shortages or large class sizes—a common LMIC challenge—students may have fewer opportunities for the high-quality peer collaboration and human scaffolding shown to support metacognitive development. Third, the 'digital divide' may create a 'metacognitive divide' where students with AI access develop dependency while those without maintain traditional learning approaches, though neither group develops strong self-regulatory skills. Fourth, assessment systems in many LMICs focus on high-stakes examinations testing factual recall rather than metacognitive processes, providing less incentive for developing these skills. Fifth, teacher professional development on supporting metacognition is often limited in resource-constrained contexts, making it harder to implement the guided AI use shown to mitigate risks. However, well-designed AI systems could potentially democratize access to metacognitive scaffolding (reflection prompts, progress monitoring) currently available mainly through expert tutoring. The key is ensuring AI tools deployed in LMICs are intentionally designed to support rather than replace metacognitive engagement, with particular attention to contexts where students may lack alternative sources of metacognitive support.

## Recommendations

- Design AI tools with explicit metacognitive scaffolding: include prompts for planning, monitoring, self-assessment, and reflection at appropriate points in the learning process
- Maintain desirable difficulties: ensure students engage in effortful retrieval, self-explanation, and problem-solving rather than accepting AI-generated solutions without cognitive engagement
- Implement hybrid human-AI approaches that preserve student agency and control, allowing learners to decide when and how to use AI support
- Provide teacher professional development on facilitating metacognitive engagement when AI tools are present, including how to detect and address over-reliance
- Develop AI literacy curricula that explicitly teach students about AI limitations, appropriate use cases, and strategies for maintaining metacognitive control
- Design formative assessments that specifically target metacognitive processes, not just final performance, to monitor students' self-regulatory engagement
- Create 'productive failures' by allowing students to struggle appropriately before providing AI assistance, building metacognitive awareness of knowledge gaps
- Use AI to make metacognition visible: provide dashboards showing learning progress, knowledge gaps, and strategy effectiveness to support self-monitoring
- Distinguish between AI for 'doing tasks' versus AI for 'learning': guide students to use AI generatively rather than as answer-providers
- Conduct longitudinal monitoring of metacognitive skill development, not just immediate task performance, when evaluating AI-integrated instruction
- Implement adaptive systems that adjust support levels based on learners' metacognitive competence, providing more scaffolding for those with weaker self-regulation
- Foster peer collaboration alongside AI use, as high-quality peer interactions show stronger metacognitive benefits than AI interaction alone
- Build in reflection opportunities where students explicitly consider their learning process, strategy effectiveness, and areas for improvement
- Design assessment contexts that prevent AI-dependent strategies in high-stakes situations where metacognitive skills are critical
- Research and document best practices for maintaining metacognitive engagement across different AI tool types, subjects, and age groups

## Top Papers

1. **Beware of Metacognitive Laziness: Effects of Generative Artificial Intelligence on Learning Motivation, Processes, and Performance**
   Provides strongest direct empirical evidence of 'metacognitive laziness' phenomenon with rigorous temporal analysis of learning processes.

2. **When Peers Outperform AI (and When They Don't): Interaction Quality Over Modality**
   Demonstrates critical distinction between interaction quality versus modality, showing peer collaboration generates more metacognitive engagement than AI.

3. **Learning to Live with AI: How Students Develop AI Literacy Through Naturalistic ChatGPT Interaction**
   Only longitudinal naturalistic study showing how metacognitive engagement with AI develops over extended use, introducing concept of 'repair literacy'.

4. **A Practical Guide for Supporting Formative Assessment and Feedback Using Generative AI**
   Provides actionable framework distinguishing task-, process-, and self-regulation-level feedback essential for metacognitive support.

5. **Learner and Instructor Needs in AI-Supported Programming Learning Tools**
   Addresses critical question of learner-system control balance and shows how metacognitive factors influence control preferences.
