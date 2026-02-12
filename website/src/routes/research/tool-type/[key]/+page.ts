import { error } from '@sveltejs/kit';
import { TOOL_TYPES } from '$lib/data/tool-types';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const toolType = TOOL_TYPES[params.key];

	if (!toolType) {
		error(404, `Tool type "${params.key}" not found`);
	}

	const res = await fetch(`/research/tool-type/${params.key}.md`);

	if (!res.ok) {
		error(404, `Research report for "${toolType.name}" not available yet`);
	}

	const markdown = await res.text();

	return {
		toolType,
		markdown
	};
};
