import type { Framework, AreaGroup } from '$lib/types';

export const FRAMEWORK: Record<string, Framework> = {
	'1': {
		id: '1',
		area: 'General reasoning',
		name: 'General reasoning',
		description:
			'Benchmarks measuring general cognitive and reasoning abilities (logic, math, reading comprehension, problem-solving).'
	},
	'2.1': {
		id: '2.1',
		area: 'Pedagogy',
		name: 'Pedagogical knowledge',
		description:
			'Benchmarks measuring knowledge about teaching — instructional strategies, learning theories, curriculum design.'
	},
	'2.2': {
		id: '2.2',
		area: 'Pedagogy',
		name: 'Pedagogy of generated outputs',
		description:
			'Benchmarks evaluating the pedagogical quality of AI-generated explanations, hints, and instructional content.'
	},
	'2.3': {
		id: '2.3',
		area: 'Pedagogy',
		name: 'Pedagogical interactions',
		description:
			'Benchmarks evaluating interactive teaching behaviours — Socratic questioning, scaffolding, adaptive dialogue.'
	},
	'3.1': {
		id: '3.1',
		area: 'Educational content',
		name: 'Content knowledge',
		description: 'Benchmarks measuring mastery of subject-matter content (STEM, humanities, etc.).'
	},
	'3.2': {
		id: '3.2',
		area: 'Educational content',
		name: 'Content alignment',
		description:
			'Benchmarks measuring alignment of content to curricula, standards, or learning objectives.'
	},
	'4.1': {
		id: '4.1',
		area: 'Assessment',
		name: 'Scoring and grading',
		description: 'Benchmarks evaluating automated scoring, grading, and rubric application.'
	},
	'4.2': {
		id: '4.2',
		area: 'Assessment',
		name: 'Feedback with reasoning',
		description:
			'Benchmarks evaluating quality of feedback — explanations, reasoning traces, actionable suggestions.'
	},
	'5': {
		id: '5',
		area: 'Ethics and bias',
		name: 'Ethics and bias',
		description:
			'Benchmarks measuring fairness, bias, safety, and ethical behaviour in educational contexts.'
	},
	'6.1': {
		id: '6.1',
		area: 'Digitisation / accessibility',
		name: 'Multimodal capabilities',
		description:
			'Benchmarks evaluating vision, audio, diagram understanding, and multimodal reasoning for education.'
	},
	'6.2': {
		id: '6.2',
		area: 'Digitisation / accessibility',
		name: 'Multilingual capabilities',
		description:
			'Benchmarks evaluating performance across languages and cross-lingual educational tasks.'
	}
};

export function getAreaGroups(): AreaGroup[] {
	// Sort by numeric ID to guarantee correct order (1, 2.1, 2.2, ... 5, 6.1, 6.2)
	const sorted = Object.values(FRAMEWORK).sort(
		(a, b) => parseFloat(a.id) - parseFloat(b.id)
	);
	const grouped = new Map<string, Framework[]>();
	for (const fw of sorted) {
		const list = grouped.get(fw.area) ?? [];
		list.push(fw);
		grouped.set(fw.area, list);
	}
	return Array.from(grouped.entries()).map(([area, frameworks]) => ({ area, frameworks }));
}
