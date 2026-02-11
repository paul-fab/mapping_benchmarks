<script lang="ts">
	import type { Benchmark } from '$lib/types';
	import { getToolTypeName } from '$lib/data/tool-types';
	import TagBadge from './TagBadge.svelte';

	let { benchmark }: { benchmark: Benchmark } = $props();
</script>

<a
	href="/benchmark/{benchmark.slug}"
	class="group flex flex-col gap-3 rounded-[14px] border border-black/10 bg-white p-5 transition-all hover:border-accent/30 hover:shadow-[0px_4px_12px_0px_rgba(0,0,0,0.1)]"
>
	<div class="flex items-start justify-between gap-4">
		<h3 class="text-base font-medium text-black group-hover:text-accent transition-colors">
			{benchmark.name}
		</h3>
		<span class="shrink-0 rounded-full bg-surface-alt px-2.5 py-0.5 text-xs font-medium text-muted">
			{benchmark.sourceType}
		</span>
	</div>

	<p class="text-sm leading-relaxed text-text-secondary line-clamp-2">
		{benchmark.description}
	</p>

	<div class="flex flex-wrap gap-1.5">
		{#each benchmark.toolTypes as tt}
			<TagBadge label={getToolTypeName(tt)} variant="accent" />
		{/each}
		{#each benchmark.tags.slice(0, 4) as tag}
			<TagBadge label={tag} />
		{/each}
	</div>
</a>
