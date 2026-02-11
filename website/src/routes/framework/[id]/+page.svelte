<script lang="ts">
	import BenchmarkRow from '$lib/components/BenchmarkRow.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="mx-auto flex max-w-[1440px] flex-col gap-10 px-8 py-12">
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
		<h1 class="text-4xl font-medium text-black">
			{data.framework.name}
		</h1>
		<p class="max-w-[700px] text-lg leading-relaxed text-text-secondary">
			{data.framework.description}
		</p>
	</div>

	<!-- Benchmark count -->
	<div class="flex items-center gap-3">
		<h2 class="text-xl font-medium text-black">Benchmarks</h2>
		<span class="rounded-full bg-surface px-3 py-1 text-sm font-medium text-muted">
			{data.benchmarks.length}
		</span>
	</div>

	<!-- Benchmark list -->
	{#if data.benchmarks.length === 0}
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
			{#each data.benchmarks as benchmark}
				<BenchmarkRow {benchmark} />
			{/each}
		</div>
	{/if}
</div>
