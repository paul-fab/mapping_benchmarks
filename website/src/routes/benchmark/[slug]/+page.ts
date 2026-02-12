import { error } from '@sveltejs/kit';
import { loadBenchmarks, getBenchmarkBySlug } from '$lib/data/benchmarks';
import { FRAMEWORK } from '$lib/data/framework';
import { TOOL_TYPES } from '$lib/data/tool-types';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const allBenchmarks = await loadBenchmarks(fetch);
	const benchmark = getBenchmarkBySlug(allBenchmarks, params.slug);

	if (!benchmark) {
		error(404, `Benchmark "${params.slug}" not found`);
	}

	const frameworks = benchmark.frameworkIds.map((id) => FRAMEWORK[id]).filter(Boolean);
	const toolTypes = benchmark.toolTypes.map((key) => TOOL_TYPES[key]).filter(Boolean);

	return {
		benchmark,
		frameworks,
		toolTypes
	};
};
