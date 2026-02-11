import { error } from '@sveltejs/kit';
import { FRAMEWORK } from '$lib/data/framework';
import { getBenchmarksByFramework } from '$lib/data/benchmarks';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => {
	const framework = FRAMEWORK[params.id];

	if (!framework) {
		error(404, `Framework category "${params.id}" not found`);
	}

	const benchmarks = getBenchmarksByFramework(params.id);

	return {
		framework,
		benchmarks
	};
};
