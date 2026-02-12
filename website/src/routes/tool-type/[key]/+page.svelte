<script lang="ts">
	import { marked } from 'marked';
	import BenchmarkRow from '$lib/components/BenchmarkRow.svelte';
	import ToggleSwitch from '$lib/components/ToggleSwitch.svelte';
	import { applyYearCutoff, filterBenchmarks } from '$lib/data/benchmarks';
	import { FRAMEWORK } from '$lib/data/framework';
	import { reviewStore } from '$lib/stores/review.svelte';
	import { settingsStore, OLD_PAPER_CUTOFF } from '$lib/stores/settings.svelte';
	import type { Benchmark } from '$lib/types';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let showDismissed = $state(false);
	let searchQuery = $state('');

	// Render the executive summary markdown
	let summaryHtml = $derived(
		data.executiveSummary ? (marked(data.executiveSummary) as string) : ''
	);

	// Base set after the hide-old-papers cutoff
	let visibleBenchmarks = $derived(
		settingsStore.hideOldPapers
			? applyYearCutoff(data.benchmarks, OLD_PAPER_CUTOFF)
			: data.benchmarks
	);

	// Apply search + relevance + dismissed filters
	let filteredBenchmarks = $derived(
		filterBenchmarks(visibleBenchmarks, {
			searchQuery,
			dismissedSlugs: reviewStore.dismissed,
			showDismissed,
			minRelevance: settingsStore.minRelevance
		})
	);

	// Group filtered benchmarks by framework category
	interface FrameworkGroup {
		id: string;
		name: string;
		area: string;
		benchmarks: Benchmark[];
	}

	let groupedBenchmarks = $derived.by(() => {
		const groups: FrameworkGroup[] = [];
		const seen = new Set<string>();

		// First, create groups for the key framework needs (in order)
		for (const fw of data.keyNeedFrameworks) {
			const benchmarksInGroup = filteredBenchmarks.filter((b) =>
				b.frameworkIds.includes(fw.id)
			);
			if (benchmarksInGroup.length > 0) {
				groups.push({
					id: fw.id,
					name: fw.name,
					area: fw.area,
					benchmarks: benchmarksInGroup
				});
				for (const b of benchmarksInGroup) seen.add(b.slug);
			}
		}

		// Then, check for any other framework categories that appear in the benchmarks
		const otherFwIds = new Set<string>();
		for (const b of filteredBenchmarks) {
			if (!seen.has(b.slug)) {
				for (const fid of b.frameworkIds) {
					if (!data.keyNeedFrameworks.some((fw) => fw.id === fid)) {
						otherFwIds.add(fid);
					}
				}
			}
		}

		for (const fid of [...otherFwIds].sort((a, b) => parseFloat(a) - parseFloat(b))) {
			const fw = FRAMEWORK[fid];
			if (!fw) continue;
			const benchmarksInGroup = filteredBenchmarks.filter(
				(b) => b.frameworkIds.includes(fid) && !seen.has(b.slug)
			);
			if (benchmarksInGroup.length > 0) {
				groups.push({
					id: fw.id,
					name: fw.name,
					area: fw.area,
					benchmarks: benchmarksInGroup
				});
				for (const b of benchmarksInGroup) seen.add(b.slug);
			}
		}

		// Finally, any benchmarks without framework categories
		const uncategorized = filteredBenchmarks.filter((b) => !seen.has(b.slug));
		if (uncategorized.length > 0) {
			groups.push({
				id: 'other',
				name: 'Other',
				area: '',
				benchmarks: uncategorized
			});
		}

		return groups;
	});

	// Track which sections are expanded (all open by default)
	let expandedGroups = $state<Set<string>>(new Set(data.keyNeedFrameworks.map((fw) => fw.id)));

	function toggleGroup(id: string) {
		const next = new Set(expandedGroups);
		if (next.has(id)) {
			next.delete(id);
		} else {
			next.add(id);
		}
		expandedGroups = next;
	}

	// Expand all groups when search is active
	$effect(() => {
		if (searchQuery) {
			expandedGroups = new Set(groupedBenchmarks.map((g) => g.id));
		}
	});
</script>

<div class="mx-auto flex max-w-[1440px] flex-col gap-8 px-4 py-8 sm:gap-10 sm:px-8 sm:py-12">
	<!-- Breadcrumb -->
	<nav class="flex flex-wrap items-center gap-2 text-sm text-muted">
		<a href="/" class="transition-colors hover:text-black">Home</a>
		<span>/</span>
		<a href="/#tool-types" class="transition-colors hover:text-black">Tool Types</a>
		<span>/</span>
		<span class="text-black">{data.toolType.name}</span>
	</nav>

	<!-- Header -->
	<div class="flex flex-col gap-4">
		<h1 class="text-2xl font-medium text-black sm:text-4xl">
			{data.toolType.name}
		</h1>
		<p class="max-w-[700px] text-lg leading-relaxed text-text-secondary">
			{data.toolType.description}
		</p>
	</div>

	<!-- Executive Summary -->
	{#if summaryHtml}
		<div class="rounded-[14px] border border-black/10 bg-white p-5 shadow-[0px_2px_8px_0px_rgba(0,0,0,0.05)] sm:p-6">
			<div class="mb-3 flex items-center gap-2">
				<span class="text-lg">📋</span>
				<h2 class="text-base font-semibold text-black sm:text-lg">Research Summary</h2>
			</div>
			<div class="prose text-text-secondary">
				{@html summaryHtml}
			</div>
			{#if data.hasResearch}
				<a
					href="/research/tool-type/{data.toolType.key}"
					class="mt-4 inline-flex items-center gap-2 rounded-full border border-black/10 px-4 py-2 text-sm font-medium text-muted transition-colors hover:border-accent/30 hover:text-accent"
				>
					<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-linecap="round" stroke-linejoin="round" />
					</svg>
					Read full evidence summary
				</a>
			{/if}
		</div>
	{/if}

	<!-- Search + filters bar -->
	<div class="flex flex-col gap-3">
		<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
			<input
				type="text"
				placeholder="Search benchmarks..."
				bind:value={searchQuery}
				class="w-full rounded-[14px] border border-black/10 bg-white px-5 py-3 text-sm text-black placeholder:text-muted/60 transition-colors focus:border-accent/40 focus:outline-none focus:ring-2 focus:ring-accent/10 sm:flex-1"
			/>
			<div class="flex shrink-0 items-center gap-4">
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

		<!-- Summary stats -->
		<div class="flex flex-wrap items-center gap-3">
			<span class="text-sm text-muted">
				{filteredBenchmarks.length.toLocaleString()} benchmarks across {groupedBenchmarks.length} categories
			</span>
			{#if reviewStore.count > 0}
				<button
					onclick={() => (showDismissed = !showDismissed)}
					class="rounded-full border px-3 py-1 text-xs font-medium transition-colors
						{showDismissed
							? 'border-accent bg-accent/10 text-accent'
							: 'border-black/10 text-muted hover:border-accent/30 hover:text-accent'}"
				>
					{showDismissed ? 'Hide dismissed' : `Show dismissed (${reviewStore.count})`}
				</button>
			{/if}
		</div>
	</div>

	<!-- Benchmarks grouped by framework category -->
	<div class="flex flex-col gap-4">
		{#each groupedBenchmarks as group (group.id)}
			{@const isExpanded = expandedGroups.has(group.id)}
			<div
				class="rounded-[14px] border transition-colors
					{isExpanded ? 'border-black/15 bg-white shadow-[0px_2px_8px_0px_rgba(0,0,0,0.05)]' : 'border-black/10 bg-white hover:border-black/20'}"
			>
				<!-- Group header -->
				<button
					onclick={() => toggleGroup(group.id)}
					class="flex w-full items-center gap-3 px-5 py-4 text-left sm:px-6"
					aria-expanded={isExpanded}
				>
					{#if group.id !== 'other'}
						<span class="inline-block min-w-[2.5rem] rounded-md bg-accent/10 px-2 py-1 text-center text-sm font-semibold text-accent">
							{group.id}
						</span>
					{/if}
					<div class="flex flex-1 flex-col gap-0.5 sm:flex-row sm:items-center sm:gap-3">
						<h2 class="text-base font-semibold text-black">{group.name}</h2>
						{#if group.area && group.id !== 'other'}
							<span class="text-xs text-muted">{group.area}</span>
						{/if}
					</div>
					<span class="shrink-0 rounded-full bg-surface px-2.5 py-0.5 text-xs font-medium text-muted">
						{group.benchmarks.length}
					</span>
					<svg
						class="h-5 w-5 shrink-0 text-muted transition-transform duration-200
							{isExpanded ? 'rotate-180' : ''}"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" />
					</svg>
				</button>

				<!-- Group benchmarks -->
				{#if isExpanded}
					<div class="flex flex-col gap-2 border-t border-black/5 px-3 py-3 sm:px-4">
						{#each group.benchmarks.slice(0, 20) as benchmark (benchmark.slug)}
							<BenchmarkRow {benchmark} compact />
						{/each}
						{#if group.benchmarks.length > 20}
							<a
								href="/framework/{group.id}"
								class="py-2 text-center text-sm font-medium text-muted transition-colors hover:text-accent"
							>
								View all {group.benchmarks.length} benchmarks in {group.name} →
							</a>
						{/if}
					</div>
				{/if}
			</div>
		{/each}
	</div>
</div>

<style>
	:global(.prose) {
		color: #555;
		line-height: 1.8;
		font-size: 0.925rem;
	}

	:global(.prose p) {
		margin-top: 0.5rem;
		margin-bottom: 0.5rem;
	}

	:global(.prose strong) {
		font-weight: 600;
		color: #1a1a1a;
	}
</style>
