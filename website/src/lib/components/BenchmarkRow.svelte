<script lang="ts">
	import type { Benchmark } from '$lib/types';
	import { getToolTypeName } from '$lib/data/tool-types';
	import { reviewStore } from '$lib/stores/review.svelte';
	import TagBadge from './TagBadge.svelte';

	let { benchmark, compact = false }: { benchmark: Benchmark; compact?: boolean } = $props();
	let isDismissed = $derived(reviewStore.isDismissed(benchmark.slug));

	function handleDismiss(e: MouseEvent) {
		e.preventDefault();
		e.stopPropagation();
		reviewStore.toggle(benchmark.slug);
	}
</script>

<div class="relative {isDismissed ? 'opacity-40' : ''}">
	<a
		href="/benchmark/{benchmark.slug}"
		class="group flex flex-col gap-2 rounded-[14px] border bg-white transition-all {compact ? 'p-3 sm:p-4' : 'p-4 sm:gap-3 sm:p-5'} {isDismissed
			? 'border-red-200 bg-red-50/30'
			: 'border-black/10 hover:border-accent/30 hover:shadow-[0px_4px_12px_0px_rgba(0,0,0,0.1)]'}"
	>
		<div class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between sm:gap-4">
			<h3 class="text-sm font-medium text-black group-hover:text-accent transition-colors {compact ? '' : 'sm:text-base'} {isDismissed ? 'line-through' : ''}">
				{benchmark.name}
			</h3>
			<div class="flex flex-wrap items-center gap-1.5">
				{#if benchmark.relevanceScore}
					<span
						class="shrink-0 rounded-full px-2 py-0.5 text-xs font-medium
							{benchmark.relevanceScore >= 8 ? 'bg-green-50 text-green-700' :
							 benchmark.relevanceScore >= 5 ? 'bg-yellow-50 text-yellow-700' :
							 'bg-gray-50 text-gray-500'}"
						title="Relevance to K-12 education ({benchmark.relevanceScore}/10)"
					>
						{benchmark.relevanceScore}/10
					</span>
				{/if}
				{#if benchmark.citationCount}
					<span class="shrink-0 rounded-full bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700" title="Citations">
						{benchmark.citationCount.toLocaleString()} cited
					</span>
				{/if}
				{#if benchmark.year}
					<span class="shrink-0 rounded-full bg-surface px-2 py-0.5 text-xs font-medium text-muted">
						{benchmark.year}
					</span>
				{/if}
				{#if !compact}
					<span class="shrink-0 rounded-full bg-surface-alt px-2 py-0.5 text-xs font-medium text-muted">
						{benchmark.sourceType}
					</span>
				{/if}
				{#if benchmark.pdfUrl}
					<button
						onclick={(e) => { e.preventDefault(); e.stopPropagation(); window.open(benchmark.pdfUrl, '_blank', 'noopener,noreferrer'); }}
						class="shrink-0 rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700 transition-colors hover:bg-blue-100"
						title="Open PDF"
					>
						PDF
					</button>
				{/if}
			</div>
		</div>

		{#if !compact && (benchmark.tldr || benchmark.description)}
			<p class="text-sm leading-relaxed text-text-secondary line-clamp-2">
				{benchmark.tldr || benchmark.description}
			</p>
		{:else if compact && benchmark.tldr}
			<p class="text-xs leading-relaxed text-text-secondary line-clamp-1">
				{benchmark.tldr}
			</p>
		{/if}

		{#if !compact}
			<div class="flex flex-wrap gap-1.5">
				{#each benchmark.toolTypes as tt}
					<TagBadge label={getToolTypeName(tt)} variant="accent" />
				{/each}
				{#each benchmark.tags.slice(0, 4) as tag}
					<TagBadge label={tag} />
				{/each}
			</div>
		{/if}
	</a>

	<!-- Dismiss / Restore button -->
	<button
		onclick={handleDismiss}
		class="absolute right-2 top-2 rounded-full p-1.5 text-xs font-medium transition-all
			{isDismissed
				? 'bg-green-100 text-green-700 hover:bg-green-200'
				: 'bg-red-50 text-red-400 opacity-0 hover:bg-red-100 hover:text-red-600 group-hover:opacity-100'}
			hover:opacity-100 focus:opacity-100"
		title={isDismissed ? 'Restore benchmark' : 'Mark as not relevant'}
	>
		{#if isDismissed}
			<!-- Undo icon -->
			<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M3 10h10a5 5 0 015 5v2M3 10l4-4M3 10l4 4" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
		{:else}
			<!-- X icon -->
			<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M18 6L6 18M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
		{/if}
	</button>
</div>
