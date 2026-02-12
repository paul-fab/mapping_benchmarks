<script lang="ts">
	import TagBadge from '$lib/components/TagBadge.svelte';
	import { reviewStore } from '$lib/stores/review.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let isDismissed = $derived(reviewStore.isDismissed(data.benchmark.slug));
</script>

<div class="mx-auto flex max-w-[1440px] flex-col gap-8 px-4 py-8 sm:gap-10 sm:px-8 sm:py-12">
	<!-- Breadcrumb -->
	<nav class="flex flex-wrap items-center gap-2 text-sm text-muted">
		<a href="/" class="shrink-0 transition-colors hover:text-black">Framework</a>
		<span class="shrink-0">/</span>
		<a href="/framework/{data.frameworks[0]?.id ?? ''}" class="shrink-0 transition-colors hover:text-black">
			{data.frameworks[0]?.name ?? 'Category'}
		</a>
		<span class="shrink-0">/</span>
		<span class="text-black line-clamp-1">{data.benchmark.name}</span>
	</nav>

	<!-- Main card -->
	<div class="flex flex-col gap-6 rounded-[14px] border border-black/20 bg-white p-4 shadow-[0px_4px_6px_0px_rgba(0,0,0,0.1)] sm:gap-8 sm:p-8">
		<!-- Header -->
		<div class="flex flex-col gap-4">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between sm:gap-4">
				<h1 class="text-xl font-medium text-black sm:text-3xl {isDismissed ? 'line-through opacity-50' : ''}">
					{data.benchmark.name}
				</h1>
				<div class="flex flex-wrap items-center gap-2">
					<button
						onclick={() => reviewStore.toggle(data.benchmark.slug)}
						class="shrink-0 rounded-full px-4 py-1.5 text-sm font-medium transition-colors
							{isDismissed
								? 'bg-green-100 text-green-700 hover:bg-green-200'
								: 'bg-red-50 text-red-500 hover:bg-red-100'}"
					>
						{isDismissed ? '↩ Restore' : '✕ Not relevant'}
					</button>
					{#if data.benchmark.relevanceScore}
						<span
							class="shrink-0 rounded-full px-3 py-1 text-sm font-medium
								{data.benchmark.relevanceScore >= 8 ? 'bg-green-50 text-green-700' :
								 data.benchmark.relevanceScore >= 5 ? 'bg-yellow-50 text-yellow-700' :
								 'bg-gray-50 text-gray-500'}"
							title="Relevance to K-12 education ({data.benchmark.relevanceScore}/10)"
						>
							Relevance: {data.benchmark.relevanceScore}/10
						</span>
					{/if}
					{#if data.benchmark.citationCount}
						<span class="shrink-0 rounded-full bg-amber-50 px-3 py-1 text-sm font-medium text-amber-700" title="Citations">
							{data.benchmark.citationCount.toLocaleString()} cited
						</span>
					{/if}
					{#if data.benchmark.year}
						<span class="shrink-0 rounded-full bg-surface px-3 py-1 text-sm font-medium text-muted">
							{data.benchmark.year}
						</span>
					{/if}
					<span class="shrink-0 rounded-full bg-surface-alt px-3 py-1 text-sm font-medium text-muted">
						{data.benchmark.sourceType}
					</span>
				</div>
			</div>
			{#if data.benchmark.tldr}
				<p class="max-w-[800px] rounded-lg bg-surface/60 px-4 py-3 text-base leading-relaxed text-black">
					{data.benchmark.tldr}
				</p>
			{/if}
			{#if data.benchmark.description}
				<p class="max-w-[800px] text-lg leading-relaxed text-text-secondary">
					{data.benchmark.description}
				</p>
			{/if}
		</div>

		<!-- Source links -->
		<div class="flex flex-col gap-2">
			<h3 class="text-sm font-semibold uppercase tracking-wide text-muted">Source</h3>
			<div class="flex flex-wrap gap-3">
				<a
					href={data.benchmark.sourceUrl}
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center gap-2 rounded-full border border-accent px-5 py-2.5 text-sm font-medium text-black transition-colors hover:bg-accent/5"
				>
					<svg class="h-4 w-4 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3" stroke-linecap="round" stroke-linejoin="round" />
					</svg>
					View source
				</a>
				{#if data.benchmark.pdfUrl}
					<a
						href={data.benchmark.pdfUrl}
						target="_blank"
						rel="noopener noreferrer"
						class="inline-flex items-center gap-2 rounded-full border border-blue-400 px-5 py-2.5 text-sm font-medium text-blue-700 transition-colors hover:bg-blue-50"
					>
						<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke-linecap="round" stroke-linejoin="round" />
							<polyline points="14 2 14 8 20 8" stroke-linecap="round" stroke-linejoin="round" />
							<line x1="16" y1="13" x2="8" y2="13" stroke-linecap="round" stroke-linejoin="round" />
							<line x1="16" y1="17" x2="8" y2="17" stroke-linecap="round" stroke-linejoin="round" />
						</svg>
						Open PDF
					</a>
				{/if}
			</div>
		</div>

		<!-- Framework categories -->
		<div class="flex flex-col gap-3">
			<h3 class="text-sm font-semibold uppercase tracking-wide text-muted">Framework Categories</h3>
			<div class="flex flex-wrap gap-2">
				{#each data.frameworks as fw}
					<a
						href="/framework/{fw.id}"
						class="flex items-center gap-2 rounded-[14px] border border-black/10 bg-surface px-4 py-3 transition-colors hover:border-accent/30"
					>
						<span class="rounded-full bg-white px-2.5 py-0.5 text-sm font-semibold text-text-dim shadow-sm">
							{fw.id}
						</span>
						<span class="text-sm font-medium text-black">{fw.name}</span>
					</a>
				{/each}
			</div>
		</div>

		<!-- Tool types -->
		<div class="flex flex-col gap-3">
			<h3 class="text-sm font-semibold uppercase tracking-wide text-muted">Tool Types</h3>
			<div class="flex flex-wrap gap-2">
				{#each data.toolTypes as tt}
					<div class="flex flex-col gap-1 rounded-[14px] border border-accent/20 bg-accent/5 px-4 py-3">
						<span class="text-sm font-medium text-accent">{tt.name}</span>
						<span class="text-xs text-text-secondary">{tt.description}</span>
					</div>
				{/each}
			</div>
		</div>

		<!-- Tags -->
		<div class="flex flex-col gap-3">
			<h3 class="text-sm font-semibold uppercase tracking-wide text-muted">Tags</h3>
			<div class="flex flex-wrap gap-1.5">
				{#each data.benchmark.tags as tag}
					<TagBadge label={tag} />
				{/each}
			</div>
		</div>
	</div>
</div>
