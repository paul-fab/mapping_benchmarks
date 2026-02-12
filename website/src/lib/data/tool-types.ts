import type { ToolType } from '$lib/types';

export const TOOL_TYPES: Record<string, ToolType> = {
	ai_tutor: {
		key: 'ai_tutor',
		name: 'AI Tutors',
		description:
			'1-to-1 conversational tutoring systems.',
		keyNeeds: ['2.3', '2.2', '4.2', '3.1', '1']
	},
	pal: {
		key: 'pal',
		name: 'Personalised Adaptive Learning',
		description:
			'Systems that adapt content and difficulty to individual learners.',
		keyNeeds: ['3.2', '2.1', '4.1', '4.2', '6.1', '6.2']
	},
	teacher_support: {
		key: 'teacher_support',
		name: 'Teacher Support Tools',
		description:
			'Tools that assist teachers — lesson planning, content generation, grading, analytics.',
		keyNeeds: ['2.1', '3.1', '3.2', '4.1', '4.2', '5']
	}
};

export function getToolTypeName(key: string): string {
	return TOOL_TYPES[key]?.name ?? key;
}
