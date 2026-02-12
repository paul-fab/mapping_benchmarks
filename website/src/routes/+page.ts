import { loadBenchmarks } from '$lib/data/benchmarks';
import { loadResearchIds, loadToolTypeResearchIds, loadConcernResearchIds } from '$lib/data/research';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const [benchmarks, researchIds, ttResearchIds, concernResearchIds] = await Promise.all([
		loadBenchmarks(fetch),
		loadResearchIds(fetch),
		loadToolTypeResearchIds(fetch),
		loadConcernResearchIds(fetch)
	]);
	return { benchmarks, researchIds, ttResearchIds, concernResearchIds };
};
