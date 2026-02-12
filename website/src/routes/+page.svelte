<script lang="ts">
	import { getAreaGroups, FRAMEWORK } from '$lib/data/framework';
	import { getBenchmarkCount, getAvailableYears, applyYearCutoff, filterBenchmarks } from '$lib/data/benchmarks';
	import { TOOL_TYPES } from '$lib/data/tool-types';
	import { CONCERN_LIST } from '$lib/data/concerns';
	import { reviewStore } from '$lib/stores/review.svelte';
	import { settingsStore, OLD_PAPER_CUTOFF } from '$lib/stores/settings.svelte';
	import BenchmarkRow from '$lib/components/BenchmarkRow.svelte';
	import YearFilter from '$lib/components/YearFilter.svelte';
	import ToggleSwitch from '$lib/components/ToggleSwitch.svelte';
	import type { PageData } from './$types';

	const PAGE_SIZE = 50;

	let { data }: { data: PageData } = $props();

	const areaGroups = getAreaGroups();
	const totalCategories = Object.keys(FRAMEWORK).length;

	let showDismissed = $state(false);
	let selectedYear = $state<number | null>(null);
	let searchQuery = $state('');
	let visibleCount = $state(PAGE_SIZE);

	// Base set after the hide-old-papers cutoff
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

<div class="mx-auto flex max-w-[1440px] flex-col items-center gap-8 px-4 py-8 sm:gap-11 sm:px-8 sm:py-12">
	<!-- Hero -->
	<div class="flex flex-col items-center gap-4 text-center">
		<h1 class="text-3xl font-medium text-black sm:text-5xl">
			Education Benchmarks and Evals Mapping
		</h1>
		<p class="max-w-[700px] text-base leading-relaxed text-text-secondary sm:text-xl sm:leading-[30px]">
			We searched <a href="https://www.semanticscholar.org/" target="_blank" rel="noopener noreferrer" class="text-accent underline underline-offset-2 transition-colors hover:text-accent/80">Semantic Scholar</a> for benchmarks and evals relevant to AI in education, and mapped them across {totalCategories} quality components. We used LLMs to classify {visibleBenchmarks.length.toLocaleString()} papers, which are shown below.
		</p>
	</div>

	<!-- Stats pills -->
	<div class="flex items-center gap-2 rounded-full border border-[#8e8d8d] bg-surface p-1.5">
		<a href="#categories" class="rounded-full bg-white px-4 py-2 text-sm font-medium text-black shadow-sm transition-colors hover:bg-accent/10 hover:text-accent">
			Quality Components
		</a>
		<a href="#tool-types" class="rounded-full px-4 py-2 text-sm text-muted transition-colors hover:bg-white hover:text-black hover:shadow-sm">
			Tools
		</a>
		<a href="#concerns" class="rounded-full px-4 py-2 text-sm text-muted transition-colors hover:bg-white hover:text-black hover:shadow-sm">
			Concerns
		</a>
		<a href="#benchmarks" class="rounded-full px-4 py-2 text-sm text-muted transition-colors hover:bg-white hover:text-black hover:shadow-sm">
			Benchmarks
		</a>
	</div>

	<!-- Framework table -->
	<div id="categories" class="w-full scroll-mt-24">
		<div class="overflow-x-auto rounded-[14px] border border-black/20 shadow-[0px_4px_6px_0px_rgba(0,0,0,0.1)]">
			<table class="w-full border-collapse">
				<thead>
					<tr class="border-b border-black/10 bg-surface">
						<th class="px-6 py-3 text-left text-sm font-semibold text-muted">Area</th>
						<th class="px-4 py-3 text-left text-sm font-semibold text-muted">ID</th>
						<th class="px-6 py-3 text-left text-sm font-semibold text-muted">Category</th>
						<th class="px-4 py-3 text-right text-sm font-semibold text-muted">Benchmarks</th>
						<th class="px-4 py-3 text-right text-sm font-semibold text-muted">Landscape Summary</th>
					</tr>
				</thead>
				<tbody>
					{#each areaGroups as group}
						{#each group.frameworks as fw, i}
							{@const count = getBenchmarkCount(visibleBenchmarks, fw.id)}
							<tr class="group border-b border-black/5 transition-colors last:border-b-0 hover:bg-surface/60">
								{#if i === 0}
									<td
										rowspan={group.frameworks.length}
										class="border-r border-black/5 px-6 py-4 align-top text-base font-semibold text-black"
									>
										{group.area}
									</td>
								{/if}
								<td class="px-4 py-4 text-center">
									<span class="inline-block min-w-[2.5rem] rounded-md bg-surface-alt px-2 py-1 text-sm font-semibold text-text-dim">
										{fw.id}
									</span>
								</td>
								<td class="px-6 py-4">
									<a
										href="/framework/{fw.id}"
										class="text-base font-medium text-black transition-colors hover:text-accent"
									>
										{fw.name}
									</a>
								</td>
							<td class="px-4 py-4 text-right">
								<a
									href="/framework/{fw.id}"
									class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium {count <= 2 ? 'bg-accent/10 text-accent' : 'bg-surface-alt text-text-dim'} transition-colors hover:bg-accent/10 hover:text-accent"
								>
									{count.toLocaleString()}
									{#if count <= 2}
										<svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
											<path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round" />
										</svg>
									{/if}
								</a>
							</td>
							<td class="px-4 py-4 text-right">
								{#if data.researchIds.has(fw.id)}
									<a
										href="/research/{fw.id}"
										class="inline-flex items-center gap-1.5 rounded-full bg-green-50 px-3 py-1 text-sm font-medium text-green-700 transition-colors hover:bg-green-100"
									>
										<svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
											<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-linecap="round" stroke-linejoin="round" />
										</svg>
										Read
									</a>
								{:else}
									<span class="text-xs text-muted/40">—</span>
								{/if}
							</td>
							</tr>
						{/each}
					{/each}
				</tbody>
			</table>
		</div>
	</div>

	<!-- Tool Types overview -->
	<section id="tool-types" class="flex w-full flex-col gap-5 scroll-mt-24">
		<h2 class="text-2xl font-medium text-black">Tool Types</h2>
		<div class="grid gap-5 sm:grid-cols-3">
			{#each Object.values(TOOL_TYPES) as toolType}
				<div
					class="group flex flex-col gap-3 rounded-[14px] border border-black/10 bg-white p-6 shadow-[0px_4px_6px_0px_rgba(0,0,0,0.1)] transition-all hover:border-accent/40 hover:shadow-[0px_4px_12px_0px_rgba(0,0,0,0.15)]"
				>
					<a href="/tool-type/{toolType.key}" class="flex flex-col gap-3">
						<h3 class="text-lg font-medium text-black group-hover:text-accent transition-colors">{toolType.name}</h3>
						<p class="text-sm leading-relaxed text-text-secondary">{toolType.description}</p>
						<div class="flex flex-wrap gap-1.5">
							{#each toolType.keyNeeds as need}
								<span class="rounded-full bg-accent/10 px-2.5 py-0.5 text-xs font-medium text-accent">
									{need}
								</span>
							{/each}
						</div>
					</a>
					{#if data.ttResearchIds.has(toolType.key)}
						<a
							href="/research/tool-type/{toolType.key}"
							class="mt-1 inline-flex w-fit items-center gap-1.5 rounded-full bg-green-50 px-3 py-1 text-xs font-medium text-green-700 transition-colors hover:bg-green-100"
						>
							<svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-linecap="round" stroke-linejoin="round" />
							</svg>
							Landscape Summary
						</a>
					{/if}
				</div>
			{/each}
		</div>
	</section>

	<!-- Concerns -->
	<section id="concerns" class="flex w-full flex-col gap-5 scroll-mt-24">
		<div class="flex flex-col gap-2">
			<h2 class="text-2xl font-medium text-black">Concerns</h2>
			<p class="text-sm leading-relaxed text-text-secondary">
				Cross-cutting risk themes identified across the research — what could go wrong when AI is used in education, and what do we know about it.
			</p>
		</div>
		<div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
			{#each CONCERN_LIST as concern}
				<a
					href="/research/concern/{concern.key}"
					class="group flex flex-col gap-3 rounded-[14px] border border-black/10 bg-white p-6 shadow-[0px_4px_6px_0px_rgba(0,0,0,0.1)] transition-all hover:border-red-400/40 hover:shadow-[0px_4px_12px_0px_rgba(0,0,0,0.15)]"
				>
					<div class="flex flex-col gap-3">
						<div class="flex items-center gap-2">
							<span class="inline-block rounded-md bg-red-50 px-2 py-0.5 text-xs font-semibold text-red-700">
								Concern
							</span>
						</div>
						<h3 class="text-lg font-medium text-black group-hover:text-red-700 transition-colors">{concern.name}</h3>
						<p class="text-sm leading-relaxed text-text-secondary">{concern.description}</p>
					</div>
					<span
						class="mt-1 inline-flex w-fit items-center gap-1.5 rounded-full bg-green-50 px-3 py-1 text-xs font-medium text-green-700 transition-colors group-hover:bg-green-100"
					>
						<svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-linecap="round" stroke-linejoin="round" />
						</svg>
						Landscape Summary
					</span>
				</a>
			{/each}
		</div>
	</section>

	<!-- All benchmarks -->
	<section id="benchmarks" class="flex w-full flex-col gap-5 scroll-mt-24">
		<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
			<div class="flex items-center gap-3">
				<h2 class="text-2xl font-medium text-black">All Benchmarks</h2>
				<span class="rounded-full bg-surface px-3 py-1 text-sm font-medium text-muted">
					{filteredBenchmarks.length.toLocaleString()}
				</span>
			</div>
			<div class="flex items-center gap-3">
				{#if reviewStore.count > 0}
					<span class="text-xs text-muted">{reviewStore.count} dismissed</span>
					<button
						onclick={() => (showDismissed = !showDismissed)}
						class="rounded-full border px-3 py-1.5 text-xs font-medium transition-colors
							{showDismissed
								? 'border-accent bg-accent/10 text-accent'
								: 'border-black/10 text-muted hover:border-accent/30 hover:text-accent'}"
					>
						{showDismissed ? 'Hide dismissed' : 'Show dismissed'}
					</button>
					<button
						onclick={() => {
							const blob = new Blob([reviewStore.exportJSON()], { type: 'application/json' });
							const url = URL.createObjectURL(blob);
							const a = document.createElement('a');
							a.href = url;
							a.download = 'dismissed-benchmarks.json';
							a.click();
							URL.revokeObjectURL(url);
						}}
						class="rounded-full border border-black/10 px-3 py-1.5 text-xs font-medium text-muted transition-colors hover:border-accent/30 hover:text-accent"
						title="Export dismissed list as JSON"
					>
						Export
					</button>
				{/if}
			</div>
		</div>

		<!-- Search + Year filter -->
		<div class="flex flex-col gap-3">
			<input
				type="text"
				placeholder="Search benchmarks (fuzzy matching, ranked by relevance)..."
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

		<div class="flex flex-col gap-3">
			{#each paginatedBenchmarks as benchmark (benchmark.slug)}
				<BenchmarkRow {benchmark} />
			{/each}
		</div>

		<!-- Show more / pagination -->
		{#if hasMore}
			<button
				onclick={() => (visibleCount += PAGE_SIZE)}
				class="mx-auto rounded-full border border-black/10 bg-white px-6 py-2.5 text-sm font-medium text-muted transition-colors hover:border-accent/30 hover:text-accent"
			>
				Show more ({(filteredBenchmarks.length - visibleCount).toLocaleString()} remaining)
			</button>
		{/if}
	</section>
</div>
