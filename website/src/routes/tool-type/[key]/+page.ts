import { error } from '@sveltejs/kit';
import { TOOL_TYPES } from '$lib/data/tool-types';
import { loadBenchmarks, getBenchmarksByToolType } from '$lib/data/benchmarks';
import { loadToolTypeResearchIds } from '$lib/data/research';
import { FRAMEWORK } from '$lib/data/framework';
import type { PageLoad } from './$types';

/** Extract the Executive Summary section from the markdown report. */
function extractExecutiveSummary(md: string): string | null {
	const match = md.match(/## Executive Summary\s*\n([\s\S]*?)(?=\n## |\n$)/);
	return match ? match[1].trim() : null;
}

export const load: PageLoad = async ({ params, fetch }) => {
	const toolType = TOOL_TYPES[params.key];

	if (!toolType) {
		error(404, `Tool type "${params.key}" not found`);
	}

	const [allBenchmarks, ttResearchIds] = await Promise.all([
		loadBenchmarks(fetch),
		loadToolTypeResearchIds(fetch)
	]);
	const benchmarks = getBenchmarksByToolType(allBenchmarks, params.key);
	const keyNeedFrameworks = toolType.keyNeeds.map((id) => FRAMEWORK[id]).filter(Boolean);
	const hasResearch = ttResearchIds.has(params.key);

	// Fetch executive summary from the research report if available
	let executiveSummary: string | null = null;
	if (hasResearch) {
		try {
			const res = await fetch(`/research/tool-type/${params.key}.md`);
			if (res.ok) {
				const md = await res.text();
				executiveSummary = extractExecutiveSummary(md);
			}
		} catch {
			// Silently fail — summary is optional
		}
	}

	return {
		toolType,
		benchmarks,
		keyNeedFrameworks,
		hasResearch,
		executiveSummary
	};
};
