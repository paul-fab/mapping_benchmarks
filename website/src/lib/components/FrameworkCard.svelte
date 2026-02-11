<script lang="ts">
	import type { Framework } from '$lib/types';
	import { getBenchmarkCount } from '$lib/data/benchmarks';

	let { framework }: { framework: Framework } = $props();

	let count = $derived(getBenchmarkCount(framework.id));
	let isGap = $derived(count <= 2);
</script>

<a
	href="/framework/{framework.id}"
	class="group flex flex-col gap-3 rounded-[14px] border border-black/20 bg-white p-6 shadow-[0px_4px_6px_0px_rgba(0,0,0,0.1)] transition-all hover:border-accent/40 hover:shadow-[0px_4px_12px_0px_rgba(0,0,0,0.15)]"
>
	<div class="flex items-start justify-between">
		<span class="rounded-full bg-surface-alt px-3 py-1 text-sm font-semibold text-text-dim">
			{framework.id}
		</span>
		<span class="flex items-center gap-1 text-sm font-medium {isGap ? 'text-accent' : 'text-muted'}">
			{count}
			{#if isGap}
				<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round" />
				</svg>
			{/if}
		</span>
	</div>

	<h3 class="text-lg font-medium text-black group-hover:text-accent transition-colors">
		{framework.name}
	</h3>

	<p class="text-sm leading-relaxed text-text-secondary line-clamp-2">
		{framework.description}
	</p>

	{#if isGap}
		<span class="mt-auto inline-flex items-center rounded-full bg-accent/10 px-3 py-1 text-xs font-medium text-accent">
			Gap area
		</span>
	{/if}
</a>
