<script lang="ts">
	import BenchmarkRow from '$lib/components/BenchmarkRow.svelte';
	import YearFilter from '$lib/components/YearFilter.svelte';
	import ToggleSwitch from '$lib/components/ToggleSwitch.svelte';
	import { getAvailableYears, applyYearCutoff, filterBenchmarks } from '$lib/data/benchmarks';
	import { reviewStore } from '$lib/stores/review.svelte';
	import { settingsStore, OLD_PAPER_CUTOFF } from '$lib/stores/settings.svelte';
	import type { PageData } from './$types';

	const PAGE_SIZE = 50;

	let { data }: { data: PageData } = $props();
	let showDismissed = $state(false);
	let selectedYear = $state<number | null>(null);
	let searchQuery = $state('');
	let visibleCount = $state(PAGE_SIZE);

	let visibleBenchmarks = $derived(
		settingsStore.hideOldPapers
			? applyYearCutoff(data.benchmarks, OLD_PAPER_CUTOFF)
			: data.benchmarks
	);

	let availableYears = $derived(getAvailableYears(visibleBenchmarks));

	let filteredBenchmarks = $derived(
		filterBenchmarks(visibleBenchmarks, {
			selectedYear,
			searchQuery,
			dismissedSlugs: reviewStore.dismissed,
			showDismissed,
			minRelevance: settingsStore.minRelevance
		})
	);

	let paginatedBenchmarks = $derived(filteredBenchmarks.slice(0, visibleCount));
	let hasMore = $derived(visibleCount < filteredBenchmarks.length);

	// Reset pagination when any filter changes
	$effect(() => {
		void selectedYear;
		void showDismissed;
		void searchQuery;
		void settingsStore.hideOldPapers;
		void settingsStore.minRelevance;
		visibleCount = PAGE_SIZE;
	});
</script>

<div class="mx-auto flex max-w-[1440px] flex-col gap-8 px-4 py-8 sm:gap-10 sm:px-8 sm:py-12">
	<!-- Breadcrumb -->
	<nav class="flex items-center gap-2 text-sm text-muted">
		<a href="/" class="transition-colors hover:text-black">Framework</a>
		<span>/</span>
		<span class="text-black">{data.framework.name}</span>
	</nav>

	<!-- Header -->
	<div class="flex flex-col gap-4">
		<div class="flex items-center gap-3">
			<span class="rounded-full bg-surface-alt px-4 py-1.5 text-lg font-semibold text-text-dim">
				{data.framework.id}
			</span>
			<span class="rounded-full bg-accent/10 px-3 py-1 text-sm font-medium text-accent">
				{data.framework.area}
			</span>
		</div>
		<h1 class="text-2xl font-medium text-black sm:text-4xl">
			{data.framework.name}
		</h1>
		<p class="max-w-[700px] text-lg leading-relaxed text-text-secondary">
			{data.framework.description}
		</p>
		{#if data.hasResearch}
			<a
				href="/research/{data.framework.id}"
				class="inline-flex w-fit items-center gap-2 rounded-full bg-green-50 px-4 py-2 text-sm font-medium text-green-700 transition-colors hover:bg-green-100"
			>
				<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-linecap="round" stroke-linejoin="round" />
				</svg>
				Read SoTA Research Report
			</a>
		{/if}
	</div>

	<!-- Benchmark count -->
	<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
		<div class="flex items-center gap-3">
			<h2 class="text-xl font-medium text-black">Benchmarks</h2>
			<span class="rounded-full bg-surface px-3 py-1 text-sm font-medium text-muted">
				{filteredBenchmarks.length.toLocaleString()}
			</span>
		</div>
		{#if reviewStore.count > 0}
			<button
				onclick={() => (showDismissed = !showDismissed)}
				class="rounded-full border px-3 py-1.5 text-xs font-medium transition-colors
					{showDismissed
						? 'border-accent bg-accent/10 text-accent'
						: 'border-black/10 text-muted hover:border-accent/30 hover:text-accent'}"
			>
				{showDismissed ? 'Hide dismissed' : 'Show dismissed ({reviewStore.count})'}
			</button>
		{/if}
	</div>

	<!-- Search + Year filter -->
	<div class="flex flex-col gap-3">
		<input
			type="text"
			placeholder="Search benchmarks..."
			bind:value={searchQuery}
			class="w-full rounded-[14px] border border-black/10 bg-white px-5 py-3 text-sm text-black placeholder:text-muted/60 transition-colors focus:border-accent/40 focus:outline-none focus:ring-2 focus:ring-accent/10"
		/>
		<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between sm:gap-4">
			{#if availableYears.length > 1}
				<YearFilter years={availableYears} bind:selectedYear />
			{/if}
			<div class="flex items-center gap-4">
				<div class="flex shrink-0 items-center gap-2">
					<span class="text-xs text-muted">Min relevance</span>
					<select
						bind:value={settingsStore.minRelevance}
						class="rounded-lg border border-black/10 bg-white px-2 py-1 text-xs text-black transition-colors focus:border-accent/40 focus:outline-none"
						aria-label="Minimum relevance score filter"
					>
						<option value={0}>All</option>
						{#each [3, 5, 7, 8, 9] as score}
							<option value={score}>{score}+</option>
						{/each}
					</select>
				</div>
				<ToggleSwitch
					label="Hide pre-{OLD_PAPER_CUTOFF}"
					bind:checked={settingsStore.hideOldPapers}
				/>
			</div>
		</div>
	</div>

	<!-- Benchmark list -->
	{#if filteredBenchmarks.length === 0}
		<div class="flex flex-col items-center gap-4 rounded-[14px] border border-dashed border-accent/40 bg-accent/5 p-12 text-center">
			<svg class="h-10 w-10 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			<p class="text-lg font-medium text-accent">Gap area</p>
			<p class="max-w-md text-sm text-text-secondary">
				No benchmarks have been mapped to this category yet. This represents a gap in available evaluations for education AI.
			</p>
		</div>
	{:else}
		<div class="flex flex-col gap-3">
			{#each paginatedBenchmarks as benchmark (benchmark.slug)}
				<BenchmarkRow {benchmark} />
			{/each}
		</div>

		{#if hasMore}
			<button
				onclick={() => (visibleCount += PAGE_SIZE)}
				class="mx-auto rounded-full border border-black/10 bg-white px-6 py-2.5 text-sm font-medium text-muted transition-colors hover:border-accent/30 hover:text-accent"
			>
				Show more ({(filteredBenchmarks.length - visibleCount).toLocaleString()} remaining)
			</button>
		{/if}
	{/if}
</div>
