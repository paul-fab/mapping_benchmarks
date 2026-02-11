import { error } from '@sveltejs/kit';
import { TOOL_TYPES } from '$lib/data/tool-types';
import { getBenchmarksByToolType } from '$lib/data/benchmarks';
import { FRAMEWORK } from '$lib/data/framework';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => {
	const toolType = TOOL_TYPES[params.key];

	if (!toolType) {
		error(404, `Tool type "${params.key}" not found`);
	}

	const benchmarks = getBenchmarksByToolType(params.key);
	const keyNeedFrameworks = toolType.keyNeeds
		.map((id) => FRAMEWORK[id])
		.filter(Boolean);

	return {
		toolType,
		benchmarks,
		keyNeedFrameworks
	};
};
