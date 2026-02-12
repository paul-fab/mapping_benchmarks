import { error } from '@sveltejs/kit';
import { CONCERNS } from '$lib/data/concerns';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const concern = CONCERNS[params.key];

	if (!concern) {
		error(404, `Concern "${params.key}" not found`);
	}

	const res = await fetch(`/research/concern/${params.key}.md`);

	if (!res.ok) {
		error(404, `Research report for "${concern.name}" not available yet`);
	}

	const markdown = await res.text();

	return {
		concern,
		markdown
	};
};
