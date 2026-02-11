import { error } from '@sveltejs/kit';
import { getBenchmarkBySlug } from '$lib/data/benchmarks';
import { FRAMEWORK } from '$lib/data/framework';
import { TOOL_TYPES } from '$lib/data/tool-types';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => {
	const benchmark = getBenchmarkBySlug(params.slug);

	if (!benchmark) {
		error(404, `Benchmark "${params.slug}" not found`);
	}

	const frameworks = benchmark.frameworkIds
		.map((id) => FRAMEWORK[id])
		.filter(Boolean);

	const toolTypes = benchmark.toolTypes
		.map((key) => TOOL_TYPES[key])
		.filter(Boolean);

	return {
		benchmark,
		frameworks,
		toolTypes
	};
};
