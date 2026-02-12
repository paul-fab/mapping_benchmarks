import type { Concern } from '$lib/types';

export const CONCERNS: Record<string, Concern> = {
	cognitive_offloading: {
		key: 'cognitive_offloading',
		name: 'Cognitive Offloading & Over-reliance',
		description:
			'When AI does the thinking for learners — reducing effort, bypassing productive struggle, and creating dependency.'
	},
	productive_struggle: {
		key: 'productive_struggle',
		name: 'Productive Struggle & Scaffolding',
		description:
			'The balance between helpful AI scaffolding and over-scaffolding that removes the desirable difficulty learners need to grow.'
	},
	metacognition: {
		key: 'metacognition',
		name: 'Metacognition & Self-regulation',
		description:
			'Whether AI tools help or hinder learners\u2019 ability to monitor their own understanding and self-regulate.'
	},
	critical_thinking: {
		key: 'critical_thinking',
		name: 'Critical Thinking & Higher-order Skills',
		description:
			'Impact of AI on higher-order cognitive skills — analysis, evaluation, synthesis, and creative problem-solving.'
	},
	equity_access: {
		key: 'equity_access',
		name: 'Equity & Access',
		description:
			'Risks of AI widening existing education gaps — digital divide, language bias, cost barriers, and disparate impact.'
	}
};

export const CONCERN_LIST: Concern[] = Object.values(CONCERNS);

export function getConcernName(key: string): string {
	return CONCERNS[key]?.name ?? key;
}
