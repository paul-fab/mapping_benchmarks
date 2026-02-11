<script lang="ts">
	import TagBadge from '$lib/components/TagBadge.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="mx-auto flex max-w-[1440px] flex-col gap-10 px-8 py-12">
	<!-- Breadcrumb -->
	<nav class="flex items-center gap-2 text-sm text-muted">
		<a href="/" class="transition-colors hover:text-black">Framework</a>
		<span>/</span>
		<a href="/framework/{data.frameworks[0]?.id ?? ''}" class="transition-colors hover:text-black">
			{data.frameworks[0]?.name ?? 'Category'}
		</a>
		<span>/</span>
		<span class="text-black">{data.benchmark.name}</span>
	</nav>

	<!-- Main card -->
	<div class="flex flex-col gap-8 rounded-[14px] border border-black/20 bg-white p-8 shadow-[0px_4px_6px_0px_rgba(0,0,0,0.1)]">
		<!-- Header -->
		<div class="flex flex-col gap-4">
			<div class="flex items-start justify-between gap-4">
				<h1 class="text-3xl font-medium text-black">
					{data.benchmark.name}
				</h1>
				<span class="shrink-0 rounded-full bg-surface-alt px-3 py-1 text-sm font-medium text-muted">
					{data.benchmark.sourceType}
				</span>
			</div>
			<p class="max-w-[800px] text-lg leading-relaxed text-text-secondary">
				{data.benchmark.description}
			</p>
		</div>

		<!-- Source link -->
		<div class="flex flex-col gap-2">
			<h3 class="text-sm font-semibold uppercase tracking-wide text-muted">Source</h3>
			<a
				href={data.benchmark.sourceUrl}
				target="_blank"
				rel="noopener noreferrer"
				class="inline-flex items-center gap-2 rounded-full border border-accent px-5 py-2.5 text-sm font-medium text-black transition-colors hover:bg-accent/5"
			>
				<svg class="h-4 w-4 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3" stroke-linecap="round" stroke-linejoin="round" />
				</svg>
				View on HuggingFace
			</a>
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
