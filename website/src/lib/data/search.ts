/**
 * Full-text search powered by MiniSearch.
 *
 * Provides ranked, fuzzy, prefix-aware search over benchmark name, description,
 * tags, and TLDR. Results are scored by relevance (BM25-based) with field boosting:
 *   - name:  3×  (most important — benchmark titles are highly specific)
 *   - tags:  2×  (framework/tool labels, query terms)
 *   - tldr:  1.5× (AI-generated summary — concise, high signal)
 *   - description: 1×  (longer text, lower signal-to-noise)
 *
 * Usage:
 *   1. Call `buildSearchIndex(benchmarks)` once after loading data.
 *   2. Call `searchBenchmarks(query)` to get a Map<slug, score> of matches.
 *   3. Pass the map to `filterBenchmarks` which handles ranking + other filters.
 */

import MiniSearch from 'minisearch';
import type { Benchmark } from '$lib/types';

/** Internal index — built lazily via `buildSearchIndex`. */
let index: MiniSearch | null = null;

/**
 * Build (or rebuild) the search index from a full benchmark list.
 * Call once after `loadBenchmarks()` resolves.
 */
export function buildSearchIndex(benchmarks: Benchmark[]): void {
	index = new MiniSearch({
		fields: ['name', 'description', 'tagsText', 'tldr'],
		storeFields: ['slug'],
		// Default search options applied to every query
		searchOptions: {
			boost: { name: 3, tagsText: 2, tldr: 1.5, description: 1 },
			fuzzy: 0.2,
			prefix: true
		}
	});

	const documents = benchmarks.map((b, i) => ({
		id: i,
		slug: b.slug,
		name: b.name,
		description: b.description,
		tagsText: b.tags.join(' '),
		tldr: b.tldr ?? ''
	}));

	index.addAll(documents);
}

/**
 * Search benchmarks by query string.
 *
 * @returns A Map of `slug → relevance score` for matching benchmarks,
 *          or `null` if the query is empty / index not built.
 *          Higher scores = more relevant.
 */
export function searchBenchmarks(query: string): Map<string, number> | null {
	if (!index || !query.trim()) return null;

	const results = index.search(query);

	if (results.length === 0) {
		// Fall back to a more permissive search: prefix-only, higher fuzziness
		const fuzzyResults = index.search(query, {
			fuzzy: 0.4,
			prefix: true,
			combineWith: 'OR'
		});
		if (fuzzyResults.length > 0) {
			return new Map(fuzzyResults.map((r) => [r.slug as string, r.score]));
		}
		return new Map(); // empty map = query was entered but nothing matched
	}

	return new Map(results.map((r) => [r.slug as string, r.score]));
}

/** Check whether the search index has been built. */
export function isIndexReady(): boolean {
	return index !== null;
}
