import { error } from '@sveltejs/kit';
import { FRAMEWORK } from '$lib/data/framework';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const framework = FRAMEWORK[params.id];

	if (!framework) {
		error(404, `Framework category "${params.id}" not found`);
	}

	// Load the research report markdown from static/research/{id}.md
	const res = await fetch(`/research/${params.id}.md`);

	if (!res.ok) {
		error(404, `Research report for "${framework.name}" not available yet`);
	}

	const markdown = await res.text();

	return {
		framework,
		markdown
	};
};
