import { error } from '@sveltejs/kit';
import { FRAMEWORK } from '$lib/data/framework';
import { loadBenchmarks, getBenchmarksByFramework } from '$lib/data/benchmarks';
import { loadResearchIds } from '$lib/data/research';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const framework = FRAMEWORK[params.id];

	if (!framework) {
		error(404, `Framework category "${params.id}" not found`);
	}

	const [allBenchmarks, researchIds] = await Promise.all([
		loadBenchmarks(fetch),
		loadResearchIds(fetch)
	]);
	const benchmarks = getBenchmarksByFramework(allBenchmarks, params.id);

	return {
		framework,
		benchmarks,
		hasResearch: researchIds.has(params.id)
	};
};
