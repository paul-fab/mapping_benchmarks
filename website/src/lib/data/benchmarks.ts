import type { Benchmark } from '$lib/types';

function slugify(name: string): string {
	return name
		.toLowerCase()
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-|-$/g, '');
}

export const BENCHMARKS: Benchmark[] = [
	{
		name: 'MMLU (Massive Multitask Language Understanding)',
		slug: slugify('MMLU'),
		sourceUrl: 'https://huggingface.co/datasets/cais/mmlu',
		sourceType: 'dataset',
		description:
			'57 subjects across STEM, humanities, social sciences, and more. Tests breadth and depth of knowledge.',
		frameworkIds: ['1', '3.1'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['general', 'knowledge', 'multi-subject']
	},
	{
		name: 'MMLU-Pro',
		slug: slugify('MMLU-Pro'),
		sourceUrl: 'https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro',
		sourceType: 'dataset',
		description:
			'Harder, expert-level version of MMLU with 10 answer choices and more reasoning-focused questions.',
		frameworkIds: ['1', '3.1'],
		toolTypes: ['ai_tutor'],
		tags: ['general', 'reasoning', 'expert']
	},
	{
		name: 'ARC (AI2 Reasoning Challenge)',
		slug: slugify('ARC'),
		sourceUrl: 'https://huggingface.co/datasets/allenai/ai2_arc',
		sourceType: 'dataset',
		description:
			'Grade-school science questions requiring reasoning. Challenge set focuses on questions that simple retrieval fails on.',
		frameworkIds: ['1', '3.1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['reasoning', 'science', 'grade-school']
	},
	{
		name: 'HellaSwag',
		slug: slugify('HellaSwag'),
		sourceUrl: 'https://huggingface.co/datasets/Rowan/hellaswag',
		sourceType: 'dataset',
		description:
			'Commonsense reasoning via sentence completion. Tests understanding of everyday situations.',
		frameworkIds: ['1'],
		toolTypes: ['ai_tutor'],
		tags: ['commonsense', 'reasoning']
	},
	{
		name: 'GPQA (Graduate-Level Google-Proof QA)',
		slug: slugify('GPQA'),
		sourceUrl: 'https://huggingface.co/datasets/Idavidrein/gpqa',
		sourceType: 'dataset',
		description:
			"Expert-level science questions that are 'Google-proof' -- require deep reasoning, not just retrieval.",
		frameworkIds: ['1', '3.1'],
		toolTypes: ['ai_tutor'],
		tags: ['expert', 'reasoning', 'graduate-level']
	},
	{
		name: 'BIG-Bench Hard (BBH)',
		slug: slugify('BIG-Bench Hard BBH'),
		sourceUrl: 'https://huggingface.co/datasets/maveriq/bigbenchhard',
		sourceType: 'dataset',
		description:
			'23 challenging tasks from BIG-Bench where LLMs previously underperformed -- logic, math, language understanding.',
		frameworkIds: ['1'],
		toolTypes: ['ai_tutor'],
		tags: ['reasoning', 'hard', 'diverse']
	},
	{
		name: 'TutorEval',
		slug: slugify('TutorEval'),
		sourceUrl: 'https://huggingface.co/papers/2402.08070',
		sourceType: 'paper',
		description:
			'Evaluates LLMs as tutors across multiple dimensions: pedagogical quality, accuracy, helpfulness in tutoring dialogues.',
		frameworkIds: ['2.2', '2.3'],
		toolTypes: ['ai_tutor'],
		tags: ['tutoring', 'pedagogy', 'dialogue']
	},
	{
		name: 'MathDial',
		slug: slugify('MathDial'),
		sourceUrl: 'https://huggingface.co/datasets/eth-nlped/mathdial',
		sourceType: 'dataset',
		description:
			'Math tutoring dialogues grounded in student misconceptions. Tests ability to identify and address student errors through dialogue.',
		frameworkIds: ['2.3', '4.2'],
		toolTypes: ['ai_tutor'],
		tags: ['math', 'tutoring', 'dialogue', 'misconception']
	},
	{
		name: 'GSM8K',
		slug: slugify('GSM8K'),
		sourceUrl: 'https://huggingface.co/datasets/openai/gsm8k',
		sourceType: 'dataset',
		description:
			'8.5K grade-school math word problems requiring multi-step reasoning. Widely used for math ability benchmarking.',
		frameworkIds: ['3.1', '1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['math', 'grade-school', 'word-problems']
	},
	{
		name: 'MATH',
		slug: slugify('MATH benchmark'),
		sourceUrl: 'https://huggingface.co/datasets/lighteval/MATH',
		sourceType: 'dataset',
		description:
			'12.5K competition-level math problems across 7 subjects (algebra, geometry, number theory, etc.).',
		frameworkIds: ['3.1'],
		toolTypes: ['ai_tutor'],
		tags: ['math', 'competition', 'advanced']
	},
	{
		name: 'SciQ',
		slug: slugify('SciQ'),
		sourceUrl: 'https://huggingface.co/datasets/allenai/sciq',
		sourceType: 'dataset',
		description:
			'13.7K science exam questions with supporting passages. Covers physics, chemistry, biology.',
		frameworkIds: ['3.1'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['science', 'exam', 'multiple-choice']
	},
	{
		name: 'OpenBookQA',
		slug: slugify('OpenBookQA'),
		sourceUrl: 'https://huggingface.co/datasets/allenai/openbookqa',
		sourceType: 'dataset',
		description:
			'Elementary science questions modelled after open-book exams -- requires combining a core science fact with broad commonsense.',
		frameworkIds: ['3.1', '1'],
		toolTypes: ['ai_tutor'],
		tags: ['science', 'open-book', 'commonsense']
	},
	{
		name: 'MedQA',
		slug: slugify('MedQA'),
		sourceUrl: 'https://huggingface.co/datasets/bigbio/med_qa',
		sourceType: 'dataset',
		description:
			'USMLE-style medical exam questions. Tests medical content knowledge at professional level.',
		frameworkIds: ['3.1'],
		toolTypes: ['ai_tutor'],
		tags: ['medical', 'professional', 'exam']
	},
	{
		name: 'MAmmoTH',
		slug: slugify('MAmmoTH'),
		sourceUrl: 'https://huggingface.co/datasets/TIGER-Lab/MathInstruct',
		sourceType: 'dataset',
		description:
			'Large-scale math instruction dataset combining CoT and PoT (program-of-thought) rationales across diverse math topics.',
		frameworkIds: ['3.1', '2.2'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['math', 'instruction', 'chain-of-thought']
	},
	{
		name: 'ASAP (Automated Student Assessment Prize)',
		slug: slugify('ASAP'),
		sourceUrl: 'https://huggingface.co/datasets/mpalaval/ASAP_Essay_dataset',
		sourceType: 'dataset',
		description:
			'Essay scoring dataset from Kaggle competition. 8 prompt sets with human-scored essays on different rubrics.',
		frameworkIds: ['4.1'],
		toolTypes: ['teacher_support'],
		tags: ['essay', 'scoring', 'grading', 'rubric']
	},
	{
		name: 'ASAP-SAS (Short Answer Scoring)',
		slug: slugify('ASAP-SAS'),
		sourceUrl: 'https://huggingface.co/datasets/marianna13/ASAP-SAS',
		sourceType: 'dataset',
		description:
			'Short answer scoring dataset -- human-graded short responses to content-area questions.',
		frameworkIds: ['4.1'],
		toolTypes: ['teacher_support', 'pal'],
		tags: ['short-answer', 'scoring', 'grading']
	},
	{
		name: 'FEEDBACKQA',
		slug: slugify('FEEDBACKQA'),
		sourceUrl: 'https://huggingface.co/datasets/McGill-NLP/feedbackqa',
		sourceType: 'dataset',
		description:
			'QA dataset with interactive feedback. Tests ability to provide helpful feedback on incorrect answers.',
		frameworkIds: ['4.2'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['feedback', 'QA', 'interactive']
	},
	{
		name: 'BBQ (Bias Benchmark for QA)',
		slug: slugify('BBQ'),
		sourceUrl: 'https://huggingface.co/datasets/heegyu/bbq',
		sourceType: 'dataset',
		description:
			'Tests social biases in QA across 11 categories (age, gender, race, disability, etc.).',
		frameworkIds: ['5'],
		toolTypes: ['ai_tutor', 'pal', 'teacher_support'],
		tags: ['bias', 'fairness', 'social']
	},
	{
		name: 'TruthfulQA',
		slug: slugify('TruthfulQA'),
		sourceUrl: 'https://huggingface.co/datasets/truthfulqa/truthful_qa',
		sourceType: 'dataset',
		description:
			'Tests whether models generate truthful answers. Critical for education where misinformation is harmful.',
		frameworkIds: ['5', '3.1'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['truthfulness', 'misinformation', 'safety']
	},
	{
		name: 'RealToxicityPrompts',
		slug: slugify('RealToxicityPrompts'),
		sourceUrl: 'https://huggingface.co/datasets/allenai/real-toxicity-prompts',
		sourceType: 'dataset',
		description:
			'100K prompts for measuring toxic language generation. Relevant to keeping educational content safe.',
		frameworkIds: ['5'],
		toolTypes: ['ai_tutor', 'pal', 'teacher_support'],
		tags: ['toxicity', 'safety', 'content-moderation']
	},
	{
		name: 'CrowS-Pairs',
		slug: slugify('CrowS-Pairs'),
		sourceUrl: 'https://huggingface.co/datasets/BigScienceBiasEval/crows_pairs_multilingual',
		sourceType: 'dataset',
		description:
			'Stereotype detection benchmark covering 9 bias categories. Multilingual version available.',
		frameworkIds: ['5', '6.2'],
		toolTypes: ['ai_tutor', 'pal', 'teacher_support'],
		tags: ['bias', 'stereotypes', 'multilingual']
	},
	{
		name: 'MathVista',
		slug: slugify('MathVista'),
		sourceUrl: 'https://huggingface.co/datasets/AI4Math/MathVista',
		sourceType: 'dataset',
		description:
			'Math reasoning with visual context -- charts, geometry, scientific figures. 6,141 examples from 28 datasets.',
		frameworkIds: ['6.1', '3.1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['multimodal', 'math', 'visual']
	},
	{
		name: 'MMMU (Massive Multi-discipline Multimodal Understanding)',
		slug: slugify('MMMU'),
		sourceUrl: 'https://huggingface.co/datasets/MMMU/MMMU',
		sourceType: 'dataset',
		description:
			'11.5K expert-level multimodal questions across 30 subjects. Tests college-level understanding with images.',
		frameworkIds: ['6.1', '3.1', '1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['multimodal', 'expert', 'multi-subject']
	},
	{
		name: 'ScienceQA',
		slug: slugify('ScienceQA'),
		sourceUrl: 'https://huggingface.co/datasets/derek-thomas/ScienceQA',
		sourceType: 'dataset',
		description:
			'21K multimodal science questions with lectures and explanations. Spans diverse science topics with images.',
		frameworkIds: ['6.1', '3.1', '2.2'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['multimodal', 'science', 'explanations']
	},
	{
		name: 'EXAMS',
		slug: slugify('EXAMS multilingual'),
		sourceUrl: 'https://huggingface.co/datasets/mhardalov/exams',
		sourceType: 'dataset',
		description:
			'Multilingual high-school exam questions across 16 languages and 26 subjects. Tests cross-lingual educational knowledge.',
		frameworkIds: ['6.2', '3.1'],
		toolTypes: ['pal', 'teacher_support'],
		tags: ['multilingual', 'exams', 'high-school']
	},
	{
		name: 'MGSM (Multilingual Grade School Math)',
		slug: slugify('MGSM'),
		sourceUrl: 'https://huggingface.co/datasets/juletxara/mgsm',
		sourceType: 'dataset',
		description:
			'GSM8K translated into 10 languages. Tests math reasoning across languages.',
		frameworkIds: ['6.2', '3.1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['multilingual', 'math', 'grade-school']
	},
	{
		name: 'BELEBELE',
		slug: slugify('BELEBELE'),
		sourceUrl: 'https://huggingface.co/datasets/facebook/belebele',
		sourceType: 'dataset',
		description:
			'Reading comprehension benchmark in 122 languages. Tests multilingual understanding for education accessibility.',
		frameworkIds: ['6.2', '1'],
		toolTypes: ['pal'],
		tags: ['multilingual', 'reading-comprehension', '122-languages']
	},
	{
		name: 'MMMLU (Multilingual MMLU)',
		slug: slugify('MMMLU'),
		sourceUrl: 'https://huggingface.co/datasets/openai/MMMLU',
		sourceType: 'dataset',
		description:
			'Professional translations of MMLU into 14 languages. Evaluates whether educational knowledge transfers across languages.',
		frameworkIds: ['6.2', '3.1', '1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['multilingual', 'knowledge', 'multi-subject']
	},
	{
		name: 'C-Eval',
		slug: slugify('C-Eval'),
		sourceUrl: 'https://huggingface.co/datasets/ceval/ceval-exam',
		sourceType: 'dataset',
		description:
			'Chinese educational knowledge across 52 disciplines spanning middle school through professional levels.',
		frameworkIds: ['6.2', '3.1'],
		toolTypes: ['pal', 'teacher_support'],
		tags: ['multilingual', 'chinese', 'curriculum-aligned']
	},
	{
		name: 'EduBench',
		slug: slugify('EduBench'),
		sourceUrl: 'https://huggingface.co/datasets/DirectionAI/EduBench',
		sourceType: 'dataset',
		description:
			'Educational benchmark featuring Student-Oriented Scenarios (QA, Error Correction) across subjects and difficulty levels. Chinese and English.',
		frameworkIds: ['2.1', '2.2', '3.1'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['education', 'pedagogy', 'multi-subject', 'bilingual']
	},
	{
		name: 'FairytaleQA',
		slug: slugify('FairytaleQA'),
		sourceUrl: 'https://huggingface.co/datasets/WorkInTheDark/FairytaleQA',
		sourceType: 'dataset',
		description:
			'10,580 QA pairs from 278 children\'s stories. Designed for educational question generation evaluation targeting narrative comprehension skills.',
		frameworkIds: ['2.2', '3.1'],
		toolTypes: ['teacher_support', 'ai_tutor'],
		tags: ['reading', 'question-generation', 'narrative', 'children']
	},
	{
		name: 'Socratic Benchmark',
		slug: slugify('Socratic Benchmark'),
		sourceUrl: 'https://huggingface.co/datasets/koutch/socratic_benchmark',
		sourceType: 'dataset',
		description:
			'Tutor-student programming interactions with bug identification and Socratic dialogue. 3 versions covering code debugging pedagogy.',
		frameworkIds: ['2.3', '4.2'],
		toolTypes: ['ai_tutor'],
		tags: ['Socratic', 'tutoring', 'programming', 'dialogue', 'feedback']
	},
	{
		name: 'PACT Socratic Coding Tutor',
		slug: slugify('PACT Socratic Coding Tutor'),
		sourceUrl: 'https://huggingface.co/datasets/AndreiSobo/PACT-Socratic-Coding-Tutor',
		sourceType: 'dataset',
		description:
			'227 high-quality synthetic examples for fine-tuning LLMs on Socratic pedagogy in CS education, pairing student errors with Socratic hints.',
		frameworkIds: ['2.3', '2.2'],
		toolTypes: ['ai_tutor'],
		tags: ['Socratic', 'coding', 'CS-education', 'hints']
	},
	{
		name: 'Engagement Socratic Rated',
		slug: slugify('Engagement Socratic Rated'),
		sourceUrl: 'https://huggingface.co/datasets/Jennny/engagement-socratic-rated',
		sourceType: 'dataset',
		description:
			'9.3K Socratic dialogue examples with engagement quality ratings. Evaluates educational dialogue quality.',
		frameworkIds: ['2.3'],
		toolTypes: ['ai_tutor'],
		tags: ['Socratic', 'engagement', 'rated', 'dialogue']
	},
	{
		name: 'FreedomIntelligence Socratic',
		slug: slugify('FreedomIntelligence Socratic'),
		sourceUrl: 'https://huggingface.co/datasets/FreedomIntelligence/Socratic',
		sourceType: 'dataset',
		description:
			'34.4K multi-turn Socratic conversations between human and AI. Apache 2.0 licensed.',
		frameworkIds: ['2.3'],
		toolTypes: ['ai_tutor'],
		tags: ['Socratic', 'multi-turn', 'dialogue']
	},
	{
		name: 'AGIEval',
		slug: slugify('AGIEval'),
		sourceUrl: 'https://huggingface.co/datasets/baber/agieval',
		sourceType: 'dataset',
		description:
			'Performance on human-centric standardized exams (SAT, LSAT, GRE, GMAT, civil service, law, math competitions).',
		frameworkIds: ['3.1', '1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['exams', 'standardized', 'multi-subject']
	},
	{
		name: 'TheoremQA',
		slug: slugify('TheoremQA'),
		sourceUrl: 'https://huggingface.co/datasets/wenhu/TheoremQA',
		sourceType: 'dataset',
		description:
			'800 questions requiring application of mathematical theorems. Covers math, physics, EE, CS, and finance.',
		frameworkIds: ['3.1'],
		toolTypes: ['ai_tutor'],
		tags: ['theorems', 'STEM', 'advanced']
	},
	{
		name: 'IFEval (Instruction-Following Eval)',
		slug: slugify('IFEval'),
		sourceUrl: 'https://huggingface.co/datasets/google/IFEval',
		sourceType: 'dataset',
		description:
			'Tests whether models can follow specific, verifiable instructions. Relevant to pedagogical formatting requirements.',
		frameworkIds: ['1', '2.2'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['instruction-following', 'formatting']
	},
	{
		name: 'WinoGrande',
		slug: slugify('WinoGrande'),
		sourceUrl: 'https://huggingface.co/datasets/allenai/winogrande',
		sourceType: 'dataset',
		description:
			'Large-scale Winograd Schema Challenge testing commonsense reasoning via pronoun resolution.',
		frameworkIds: ['1'],
		toolTypes: ['ai_tutor'],
		tags: ['commonsense', 'reasoning']
	},
	{
		name: 'RACE (Reading Comprehension)',
		slug: slugify('RACE'),
		sourceUrl: 'https://huggingface.co/datasets/ehovy/race',
		sourceType: 'dataset',
		description:
			'28K passages and 100K questions from English learner exams. Grade-leveled content (middle school and high school).',
		frameworkIds: ['3.2', '3.1'],
		toolTypes: ['pal', 'teacher_support'],
		tags: ['reading', 'grade-leveled', 'curriculum']
	},
	{
		name: 'Nigeria Learning Outcomes Mapping',
		slug: slugify('Nigeria Learning Outcomes Mapping'),
		sourceUrl:
			'https://huggingface.co/datasets/electricsheepafrica/nigeria-education-learning-outcomes-mapping',
		sourceType: 'dataset',
		description:
			"100K curriculum learning outcomes mapped to Bloom's taxonomy and assessment methods. Nigerian curriculum.",
		frameworkIds: ['3.2', '2.1'],
		toolTypes: ['teacher_support'],
		tags: ['curriculum', 'blooms-taxonomy', 'learning-outcomes', 'africa']
	},
	{
		name: 'BEA 2019 GEC Shared Task',
		slug: slugify('BEA 2019 GEC'),
		sourceUrl: 'https://huggingface.co/datasets/wi_locness',
		sourceType: 'dataset',
		description:
			'Grammatical error correction dataset from English learner writing samples. Relevant to automated writing feedback.',
		frameworkIds: ['4.2', '4.1'],
		toolTypes: ['teacher_support', 'ai_tutor'],
		tags: ['grammar', 'error-correction', 'writing', 'feedback']
	},
	{
		name: 'WinoBias',
		slug: slugify('WinoBias'),
		sourceUrl: 'https://huggingface.co/datasets/wino_bias',
		sourceType: 'dataset',
		description:
			'Gender bias in coreference resolution related to professional roles. Relevant to gender equity in educational interactions.',
		frameworkIds: ['5'],
		toolTypes: ['ai_tutor', 'pal', 'teacher_support'],
		tags: ['bias', 'gender', 'coreference']
	},
	{
		name: 'BOLD (Bias in Open-Ended Language Generation)',
		slug: slugify('BOLD'),
		sourceUrl: 'https://huggingface.co/datasets/AlexaAI/bold',
		sourceType: 'dataset',
		description:
			'Tests for biased text generation across demographic groups. Relevant to equitable educational content generation.',
		frameworkIds: ['5'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['bias', 'generation', 'demographic']
	},
	{
		name: 'HolisticBias',
		slug: slugify('HolisticBias'),
		sourceUrl: 'https://huggingface.co/datasets/facebook/holistic_bias',
		sourceType: 'dataset',
		description:
			'Nearly 600 descriptor terms across 13 demographic axes. Most comprehensive bias evaluation available.',
		frameworkIds: ['5'],
		toolTypes: ['ai_tutor', 'pal', 'teacher_support'],
		tags: ['bias', 'comprehensive', 'demographic']
	},
	{
		name: 'DecodingTrust',
		slug: slugify('DecodingTrust'),
		sourceUrl: 'https://huggingface.co/datasets/AI-Secure/DecodingTrust',
		sourceType: 'dataset',
		description:
			'Multi-dimensional trustworthiness evaluation across toxicity, stereotype bias, robustness, fairness, privacy, and ethics.',
		frameworkIds: ['5'],
		toolTypes: ['ai_tutor', 'pal', 'teacher_support'],
		tags: ['trustworthiness', 'multi-dimensional', 'safety']
	},
	{
		name: 'AI2D (AI2 Diagrams)',
		slug: slugify('AI2D'),
		sourceUrl: 'https://huggingface.co/datasets/lmms-lab/ai2d',
		sourceType: 'dataset',
		description:
			'Questions about scientific/educational diagrams. Directly relevant to visual STEM education.',
		frameworkIds: ['6.1', '3.1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['multimodal', 'diagrams', 'science']
	},
	{
		name: 'ChartQA',
		slug: slugify('ChartQA'),
		sourceUrl: 'https://huggingface.co/datasets/ahmed-masry/ChartQA',
		sourceType: 'dataset',
		description:
			'Questions requiring understanding of charts and graphs. Relevant to data literacy education.',
		frameworkIds: ['6.1', '3.1'],
		toolTypes: ['ai_tutor', 'teacher_support'],
		tags: ['multimodal', 'charts', 'data-literacy']
	},
	{
		name: 'XCOPA',
		slug: slugify('XCOPA'),
		sourceUrl: 'https://huggingface.co/datasets/xcopa',
		sourceType: 'dataset',
		description:
			'Causal reasoning across 11 languages. Tests whether educational AI can reason effectively in multiple languages.',
		frameworkIds: ['6.2', '1'],
		toolTypes: ['ai_tutor', 'pal'],
		tags: ['multilingual', 'causal-reasoning', '11-languages']
	},
	{
		name: 'KMMLU (Korean MMLU)',
		slug: slugify('KMMLU'),
		sourceUrl: 'https://huggingface.co/datasets/HAERAE-HUB/KMMLU',
		sourceType: 'dataset',
		description: 'Korean-language knowledge evaluation across academic subjects.',
		frameworkIds: ['6.2', '3.1'],
		toolTypes: ['pal'],
		tags: ['multilingual', 'korean', 'knowledge']
	}
];

export function getBenchmarksByFramework(frameworkId: string): Benchmark[] {
	return BENCHMARKS.filter((b) => b.frameworkIds.includes(frameworkId));
}

export function getBenchmarkBySlug(slug: string): Benchmark | undefined {
	return BENCHMARKS.find((b) => b.slug === slug);
}

export function getBenchmarkCount(frameworkId: string): number {
	return BENCHMARKS.filter((b) => b.frameworkIds.includes(frameworkId)).length;
}

export function getBenchmarksByToolType(toolTypeKey: string): Benchmark[] {
	return BENCHMARKS.filter((b) => b.toolTypes.includes(toolTypeKey));
}
