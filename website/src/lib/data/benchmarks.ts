import type { Benchmark } from '$lib/types';
import { buildSearchIndex, searchBenchmarks } from './search';

let _cache: Promise<Benchmark[]> | null = null;

/**
 * Load all benchmarks from the static JSON file.
 * Caches in memory after the first fetch so subsequent calls are instant.
 * Also builds the MiniSearch full-text index on first load.
 */
export function loadBenchmarks(fetchFn: typeof fetch): Promise<Benchmark[]> {
	if (!_cache) {
		_cache = fetchFn('/benchmarks.json')
			.then((r) => {
				if (!r.ok) throw new Error(`Failed to load benchmarks: ${r.status}`);
				return r.json() as Promise<Benchmark[]>;
			})
			.then((benchmarks) => {
				// Sort by relevance score (highest first) as default order
				benchmarks.sort((a, b) => (b.relevanceScore ?? 0) - (a.relevanceScore ?? 0));
				buildSearchIndex(benchmarks);
				return benchmarks;
			})
			.catch((err) => {
				_cache = null; // clear cache so next call retries
				throw err;
			});
	}
	return _cache;
}

/* ---------- lookup helpers ---------- */

export function getBenchmarksByFramework(benchmarks: Benchmark[], frameworkId: string): Benchmark[] {
	return benchmarks.filter((b) => b.frameworkIds.includes(frameworkId));
}

export function getBenchmarkBySlug(benchmarks: Benchmark[], slug: string): Benchmark | undefined {
	return benchmarks.find((b) => b.slug === slug);
}

export function getBenchmarkCount(benchmarks: Benchmark[], frameworkId: string): number {
	return benchmarks.filter((b) => b.frameworkIds.includes(frameworkId)).length;
}

export function getBenchmarksByToolType(benchmarks: Benchmark[], toolTypeKey: string): Benchmark[] {
	return benchmarks.filter((b) => b.toolTypes.includes(toolTypeKey));
}

/* ---------- filter helpers ---------- */

/** Extract the distinct years present in a benchmark list, sorted newest-first. */
export function getAvailableYears(benchmarks: Benchmark[]): number[] {
	const years = new Set<number>();
	for (const b of benchmarks) {
		if (b.year) years.add(b.year);
	}
	return [...years].sort((a, b) => b - a);
}

/** Remove benchmarks published before `cutoffYear`. Benchmarks without a year are kept. */
export function applyYearCutoff(benchmarks: Benchmark[], cutoffYear: number): Benchmark[] {
	return benchmarks.filter((b) => !b.year || b.year >= cutoffYear);
}

export interface BenchmarkFilterOptions {
	selectedYear?: number | null;
	searchQuery?: string;
	dismissedSlugs?: Set<string>;
	showDismissed?: boolean;
	minRelevance?: number;
}

/**
 * Apply user-facing filters (year, search, dismissed) to a benchmark list.
 * This is the single source of truth for list-page filtering logic.
 *
 * When a search query is provided, uses MiniSearch for ranked full-text search
 * with fuzzy matching, prefix search, and field boosting (name > tags > description).
 * Results are sorted by relevance score when a query is active.
 */
export function filterBenchmarks(benchmarks: Benchmark[], opts: BenchmarkFilterOptions): Benchmark[] {
	const { selectedYear = null, searchQuery = '', dismissedSlugs, showDismissed = false, minRelevance = 0 } = opts;

	// Get ranked search results (null = no query, empty Map = query with no matches)
	const searchScores = searchQuery ? searchBenchmarks(searchQuery) : null;

	let filtered = benchmarks.filter((b) => {
		if (!showDismissed && dismissedSlugs?.has(b.slug)) return false;
		if (selectedYear !== null && b.year !== selectedYear) return false;
		if (searchScores !== null && !searchScores.has(b.slug)) return false;
		if (minRelevance > 0 && (b.relevanceScore ?? 0) < minRelevance) return false;
		return true;
	});

	// Sort by search relevance when a query is active, else by relevanceScore (default from load)
	if (searchScores && searchScores.size > 0) {
		filtered.sort((a, b) => (searchScores.get(b.slug) ?? 0) - (searchScores.get(a.slug) ?? 0));
	}

	return filtered;
}
