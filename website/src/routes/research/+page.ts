import { loadResearchIds, loadToolTypeResearchIds } from '$lib/data/research';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const [researchIds, ttResearchIds] = await Promise.all([
		loadResearchIds(fetch),
		loadToolTypeResearchIds(fetch)
	]);
	return { researchIds, ttResearchIds };
};
