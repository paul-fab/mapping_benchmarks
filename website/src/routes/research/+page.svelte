<script lang="ts">
	import { getAreaGroups, FRAMEWORK } from '$lib/data/framework';
	import { TOOL_TYPES } from '$lib/data/tool-types';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const areaGroups = getAreaGroups();

	// Build a flat list of frameworks that have reports
	const frameworkReports = $derived(
		Object.values(FRAMEWORK)
			.filter((fw) => data.researchIds.has(fw.id))
			.sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }))
	);

	const toolTypeReports = $derived(
		Object.values(TOOL_TYPES)
			.filter((tt) => data.ttResearchIds.has(tt.key))
	);
</script>

<div class="mx-auto flex max-w-[1440px] flex-col gap-8 px-4 py-8 sm:gap-10 sm:px-8 sm:py-12">
	<!-- Header -->
	<div class="flex flex-col gap-4">
		<h1 class="text-2xl font-medium text-black sm:text-4xl">Research Reports</h1>
		<p class="max-w-[700px] text-lg leading-relaxed text-text-secondary">
			State-of-the-art analyses and evidence summaries synthesised from high-relevance papers,
			organised by framework category and tool type.
		</p>
	</div>

	<!-- Process explanation -->
	<div class="rounded-[14px] border border-black/10 bg-surface/50 px-5 py-4">
		<p class="text-sm leading-relaxed text-text-secondary">
			<span class="font-medium text-black">How these were produced:</span> We identified papers
			scoring ≥7/10 for relevance to K-12 AI education, extracted key sections (abstract,
			introduction, results, discussion, conclusions), then used Claude to synthesise findings
			into structured analyses. Each report reflects what the research covers — and what it doesn't.
		</p>
	</div>

	<!-- Framework Category Reports -->
	{#if frameworkReports.length > 0}
		<section class="flex flex-col gap-5">
			<div class="flex items-center gap-3">
				<h2 class="text-xl font-medium text-black">Framework Categories</h2>
				<span class="rounded-full bg-surface px-3 py-1 text-sm font-medium text-muted">
					{frameworkReports.length}
				</span>
			</div>

			<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
				{#each frameworkReports as fw}
					<a
						href="/research/{fw.id}"
						class="group flex flex-col gap-2 rounded-[14px] border border-black/10 bg-white p-5 transition-all hover:border-accent/30 hover:shadow-[0px_2px_8px_0px_rgba(0,0,0,0.08)]"
					>
						<div class="flex items-center gap-2">
							<span class="inline-block min-w-[2rem] rounded-md bg-accent/10 px-2 py-0.5 text-center text-xs font-semibold text-accent">
								{fw.id}
							</span>
							<span class="text-xs text-muted">{fw.area}</span>
						</div>
						<h3 class="text-base font-medium text-black transition-colors group-hover:text-accent">
							{fw.name}
						</h3>
						<p class="line-clamp-2 text-sm text-text-secondary">{fw.description}</p>
					</a>
				{/each}
			</div>
		</section>
	{/if}

	<!-- Tool Type Evidence Summaries -->
	{#if toolTypeReports.length > 0}
		<section class="flex flex-col gap-5">
			<div class="flex items-center gap-3">
				<h2 class="text-xl font-medium text-black">Tool Type Evidence Summaries</h2>
				<span class="rounded-full bg-surface px-3 py-1 text-sm font-medium text-muted">
					{toolTypeReports.length}
				</span>
			</div>

			<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
				{#each toolTypeReports as tt}
					<a
						href="/research/tool-type/{tt.key}"
						class="group flex flex-col gap-2 rounded-[14px] border border-black/10 bg-white p-5 transition-all hover:border-purple-300 hover:shadow-[0px_2px_8px_0px_rgba(0,0,0,0.08)]"
					>
						<div class="flex items-center gap-2">
							<span class="inline-block rounded-md bg-purple-50 px-2 py-0.5 text-xs font-semibold text-purple-700">
								Tool Type
							</span>
						</div>
						<h3 class="text-base font-medium text-black transition-colors group-hover:text-purple-700">
							{tt.name}
						</h3>
						<p class="line-clamp-2 text-sm text-text-secondary">{tt.description}</p>
					</a>
				{/each}
			</div>
		</section>
	{/if}

	<!-- Empty state -->
	{#if frameworkReports.length === 0 && toolTypeReports.length === 0}
		<div class="flex flex-col items-center gap-4 py-12 text-center">
			<span class="text-4xl">📝</span>
			<p class="text-lg text-muted">No research reports available yet.</p>
			<p class="text-sm text-text-secondary">Reports will appear here once they have been generated and synced.</p>
		</div>
	{/if}
</div>
