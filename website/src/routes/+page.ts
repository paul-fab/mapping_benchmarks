import { loadBenchmarks } from '$lib/data/benchmarks';
import { loadResearchIds, loadToolTypeResearchIds } from '$lib/data/research';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const [benchmarks, researchIds, ttResearchIds] = await Promise.all([
		loadBenchmarks(fetch),
		loadResearchIds(fetch),
		loadToolTypeResearchIds(fetch)
	]);
	return { benchmarks, researchIds, ttResearchIds };
};
