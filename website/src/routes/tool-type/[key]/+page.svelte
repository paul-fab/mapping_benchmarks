<script lang="ts">
	import BenchmarkRow from '$lib/components/BenchmarkRow.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="mx-auto flex max-w-[1440px] flex-col gap-10 px-8 py-12">
	<!-- Breadcrumb -->
	<nav class="flex items-center gap-2 text-sm text-muted">
		<a href="/" class="transition-colors hover:text-black">Home</a>
		<span>/</span>
		<a href="/#tool-types" class="transition-colors hover:text-black">Tool Types</a>
		<span>/</span>
		<span class="text-black">{data.toolType.name}</span>
	</nav>

	<!-- Header -->
	<div class="flex flex-col gap-4">
		<h1 class="text-4xl font-medium text-black">
			{data.toolType.name}
		</h1>
		<p class="max-w-[700px] text-lg leading-relaxed text-text-secondary">
			{data.toolType.description}
		</p>
	</div>

	<!-- Key framework needs -->
	<div class="flex flex-col gap-3">
		<h2 class="text-sm font-semibold uppercase tracking-wide text-muted">Key Framework Needs</h2>
		<div class="flex flex-wrap gap-2">
			{#each data.keyNeedFrameworks as fw}
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

	<!-- Benchmark count + list -->
	<div class="flex items-center gap-3">
		<h2 class="text-xl font-medium text-black">Relevant Benchmarks</h2>
		<span class="rounded-full bg-surface px-3 py-1 text-sm font-medium text-muted">
			{data.benchmarks.length}
		</span>
	</div>

	<div class="flex flex-col gap-3">
		{#each data.benchmarks as benchmark}
			<BenchmarkRow {benchmark} />
		{/each}
	</div>
</div>
