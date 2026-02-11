<script lang="ts">
	import { getAreaGroups, FRAMEWORK } from '$lib/data/framework';
	import { BENCHMARKS, getBenchmarkCount } from '$lib/data/benchmarks';
	import { TOOL_TYPES } from '$lib/data/tool-types';

	const areaGroups = getAreaGroups();
	const totalBenchmarks = BENCHMARKS.length;
	const totalCategories = Object.keys(FRAMEWORK).length;
	const totalToolTypes = Object.keys(TOOL_TYPES).length;
</script>

<div class="mx-auto flex max-w-[1440px] flex-col items-center gap-11 px-8 py-12">
	<!-- Hero -->
	<div class="flex flex-col items-center gap-4 text-center">
		<h1 class="text-5xl font-medium text-black">
			Education Benchmark Mapping
		</h1>
		<p class="max-w-[700px] text-xl leading-[30px] text-text-secondary">
			Mapping {totalBenchmarks} AI benchmarks to {totalCategories} education framework categories.
			Identifying what we can measure and where the gaps are.
		</p>
	</div>

	<!-- Stats pills -->
	<div class="flex items-center gap-2 rounded-full border border-[#8e8d8d] bg-surface p-1.5">
		<a href="#categories" class="rounded-full bg-white px-4 py-2 text-sm font-medium text-black shadow-sm transition-colors hover:bg-accent/10 hover:text-accent">
			Framework
		</a>
		<a href="#benchmarks" class="rounded-full px-4 py-2 text-sm text-muted transition-colors hover:bg-white hover:text-black hover:shadow-sm">
			Benchmarks
		</a>
		<a href="#tool-types" class="rounded-full px-4 py-2 text-sm text-muted transition-colors hover:bg-white hover:text-black hover:shadow-sm">
			Tools
		</a>
	</div>

	<!-- Framework table -->
	<div id="categories" class="w-full scroll-mt-24">
		<div class="overflow-hidden rounded-[14px] border border-black/20 shadow-[0px_4px_6px_0px_rgba(0,0,0,0.1)]">
			<table class="w-full border-collapse">
				<thead>
					<tr class="border-b border-black/10 bg-surface">
						<th class="px-6 py-3 text-left text-sm font-semibold text-muted">Area</th>
						<th class="px-4 py-3 text-left text-sm font-semibold text-muted">ID</th>
						<th class="px-6 py-3 text-left text-sm font-semibold text-muted">Category</th>
						<th class="px-4 py-3 text-right text-sm font-semibold text-muted">Benchmarks</th>
					</tr>
				</thead>
				<tbody>
					{#each areaGroups as group}
						{#each group.frameworks as fw, i}
							{@const count = getBenchmarkCount(fw.id)}
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
										{count}
										{#if count <= 2}
											<svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
												<path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round" />
											</svg>
										{/if}
									</a>
								</td>
							</tr>
						{/each}
					{/each}
				</tbody>
			</table>
		</div>
	</div>

	<!-- All benchmarks -->
	<section id="benchmarks" class="flex w-full flex-col gap-5 scroll-mt-24">
		<h2 class="text-2xl font-medium text-black">All Benchmarks</h2>
		<div class="flex flex-col gap-3">
			{#each BENCHMARKS as benchmark}
				<a
					href="/benchmark/{benchmark.slug}"
					class="group flex items-center justify-between gap-4 rounded-[14px] border border-black/10 bg-white px-5 py-4 transition-all hover:border-accent/30 hover:shadow-[0px_4px_12px_0px_rgba(0,0,0,0.1)]"
				>
					<div class="flex flex-col gap-1">
						<span class="text-sm font-medium text-black group-hover:text-accent transition-colors">{benchmark.name}</span>
						<span class="text-xs text-text-secondary line-clamp-1">{benchmark.description}</span>
					</div>
					<div class="flex shrink-0 items-center gap-2">
						{#each benchmark.frameworkIds.slice(0, 3) as fid}
							<span class="rounded-full bg-surface-alt px-2 py-0.5 text-xs font-medium text-text-dim">{fid}</span>
						{/each}
						<svg class="h-4 w-4 text-muted group-hover:text-accent transition-colors" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<path d="M9 18l6-6-6-6" stroke-linecap="round" stroke-linejoin="round" />
						</svg>
					</div>
				</a>
			{/each}
		</div>
	</section>

	<!-- Tool Types overview -->
	<section id="tool-types" class="flex w-full flex-col gap-5 scroll-mt-24">
		<h2 class="text-2xl font-medium text-black">Tool Types</h2>
		<div class="grid gap-5 sm:grid-cols-3">
			{#each Object.values(TOOL_TYPES) as toolType}
				<a
					href="/tool-type/{toolType.key}"
					class="group flex flex-col gap-3 rounded-[14px] border border-black/10 bg-white p-6 shadow-[0px_4px_6px_0px_rgba(0,0,0,0.1)] transition-all hover:border-accent/40 hover:shadow-[0px_4px_12px_0px_rgba(0,0,0,0.15)]"
				>
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
			{/each}
		</div>
	</section>
</div>
