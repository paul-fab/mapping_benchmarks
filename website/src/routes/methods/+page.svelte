<script lang="ts">
	import { FRAMEWORK } from '$lib/data/framework';
	import { TOOL_TYPES } from '$lib/data/tool-types';
	import { CONCERN_LIST } from '$lib/data/concerns';
</script>

<div class="mx-auto flex max-w-[900px] flex-col gap-10 px-4 py-8 sm:px-8 sm:py-12">
	<!-- Breadcrumb -->
	<nav class="flex items-center gap-2 text-sm text-muted">
		<a href="/" class="transition-colors hover:text-black">Home</a>
		<span>/</span>
		<span class="text-black">Methods</span>
	</nav>

	<!-- Header -->
	<div class="flex flex-col gap-4">
		<h1 class="text-3xl font-medium text-black sm:text-4xl">Methods</h1>
		<p class="text-lg leading-relaxed text-text-secondary">
			How we built this mapping — from paper discovery to classification to synthesis.
		</p>
	</div>

	<!-- Overview -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">Overview</h2>
		<p class="leading-relaxed text-text-secondary">
			This project maps AI/LLM benchmarks and evaluations to a quality framework for K-12 education,
			with a focus on low- and middle-income countries (LMICs). The goal is to identify what we can
			measure about AI tools for education — and where the gaps are.
		</p>
		<p class="leading-relaxed text-text-secondary">
			The pipeline has four stages: <strong class="text-black">discovery</strong>,
			<strong class="text-black">classification</strong>,
			<strong class="text-black">enrichment</strong>, and
			<strong class="text-black">synthesis</strong>. Each stage is automated but human-reviewed.
		</p>
	</section>

	<!-- Pipeline diagram -->
	<div class="rounded-[14px] border border-black/10 bg-surface/50 p-6">
		<div class="flex flex-col items-center gap-3 sm:flex-row sm:justify-between">
			<div class="flex flex-col items-center gap-1 text-center">
				<span class="text-2xl">🔍</span>
				<span class="text-sm font-semibold text-black">1. Discovery</span>
				<span class="text-xs text-muted">Semantic Scholar<br/>& HuggingFace</span>
			</div>
			<svg class="hidden h-5 w-8 text-muted sm:block" viewBox="0 0 32 20" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M2 10h24m-6-6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			<span class="text-muted sm:hidden">↓</span>
			<div class="flex flex-col items-center gap-1 text-center">
				<span class="text-2xl">🏷️</span>
				<span class="text-sm font-semibold text-black">2. Classification</span>
				<span class="text-xs text-muted">Heuristic +<br/>LLM (Claude)</span>
			</div>
			<svg class="hidden h-5 w-8 text-muted sm:block" viewBox="0 0 32 20" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M2 10h24m-6-6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			<span class="text-muted sm:hidden">↓</span>
			<div class="flex flex-col items-center gap-1 text-center">
				<span class="text-2xl">📊</span>
				<span class="text-sm font-semibold text-black">3. Enrichment</span>
				<span class="text-xs text-muted">S2 metadata,<br/>TLDRs, citations</span>
			</div>
			<svg class="hidden h-5 w-8 text-muted sm:block" viewBox="0 0 32 20" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M2 10h24m-6-6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			<span class="text-muted sm:hidden">↓</span>
			<div class="flex flex-col items-center gap-1 text-center">
				<span class="text-2xl">📝</span>
				<span class="text-sm font-semibold text-black">4. Synthesis</span>
				<span class="text-xs text-muted">LLM landscape<br/>summaries</span>
			</div>
		</div>
	</div>

	<!-- Stage 1: Discovery -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">Stage 1: Paper Discovery</h2>
		<p class="leading-relaxed text-text-secondary">
			We search for papers and datasets from two primary sources:
		</p>

		<div class="grid gap-4 sm:grid-cols-2">
			<div class="rounded-[14px] border border-black/10 bg-white p-5 shadow-[0px_2px_6px_0px_rgba(0,0,0,0.06)]">
				<div class="flex flex-col gap-2">
					<div class="flex items-center gap-2">
						<span class="text-lg">📚</span>
						<h3 class="text-base font-semibold text-black">
							<a
								href="https://www.semanticscholar.org/"
								target="_blank"
								rel="noopener noreferrer"
								class="text-accent underline underline-offset-2 transition-colors hover:text-accent/80"
							>Semantic Scholar</a>
						</h3>
					</div>
					<p class="text-sm leading-relaxed text-text-secondary">
						A free, AI-powered research tool for scientific literature maintained by the Allen Institute for AI.
						We use the Semantic Scholar API to perform bulk searches across 230M+ academic papers, fetching
						up to 1,000 results per query.
					</p>
				</div>
			</div>

			<div class="rounded-[14px] border border-black/10 bg-white p-5 shadow-[0px_2px_6px_0px_rgba(0,0,0,0.06)]">
				<div class="flex flex-col gap-2">
					<div class="flex items-center gap-2">
						<span class="text-lg">🤗</span>
						<h3 class="text-base font-semibold text-black">HuggingFace</h3>
					</div>
					<p class="text-sm leading-relaxed text-text-secondary">
						We search HuggingFace for datasets and daily papers related to education benchmarks.
						This captures evaluation datasets that may not appear in traditional academic search.
					</p>
				</div>
			</div>
		</div>

		<p class="leading-relaxed text-text-secondary">
			We run over <strong class="text-black">80 targeted search queries</strong> designed to cover every
			part of the quality framework — from broad queries like "LLM evaluation K-12 education" to
			specific ones like "automated essay scoring evaluation" or "zone of proximal development AI tutoring".
			Results are deduplicated by URL to build a comprehensive corpus.
		</p>
	</section>

	<!-- Stage 2: Classification -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">Stage 2: Two-Stage Classification</h2>
		<p class="leading-relaxed text-text-secondary">
			Every paper is classified against {Object.keys(FRAMEWORK).length} quality components, organised
			into {new Set(Object.values(FRAMEWORK).map((f) => f.area)).size} areas, and
			{Object.keys(TOOL_TYPES).length} tool types. Classification uses a two-stage pipeline:
		</p>

		<div class="flex flex-col gap-4">
			<div class="flex gap-4 rounded-[14px] border border-black/10 bg-white p-5">
				<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface font-semibold text-muted">1</div>
				<div class="flex flex-col gap-1">
					<h3 class="text-base font-semibold text-black">Heuristic Scoring</h3>
					<p class="text-sm leading-relaxed text-text-secondary">
						Word-boundary keyword matching against the paper's title, description, and tags.
						Each framework category has a curated keyword list (e.g. "pedagogical knowledge",
						"scaffolding", "automated essay scoring"). Single words use word-boundary matching;
						multi-word phrases use substring matching. This produces initial framework and tool-type
						assignments with confidence scores.
					</p>
				</div>
			</div>

			<div class="flex gap-4 rounded-[14px] border border-black/10 bg-white p-5">
				<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface font-semibold text-muted">2</div>
				<div class="flex flex-col gap-1">
					<h3 class="text-base font-semibold text-black">LLM Classification (Claude)</h3>
					<p class="text-sm leading-relaxed text-text-secondary">
						Each paper is sent to Anthropic's Claude (claude-haiku-4-5) with the full framework definitions
						and tool type descriptions. The LLM assigns framework IDs and tool types, provides a
						relevance score (1-10) indicating how relevant the paper is to K-12 AI education,
						and generates a brief rationale. LLM results are merged with heuristic results to
						produce the final classification.
					</p>
				</div>
			</div>
		</div>
	</section>

	<!-- Stage 3: Enrichment -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">Stage 3: Enrichment</h2>
		<p class="leading-relaxed text-text-secondary">
			After classification, we enrich each paper with additional metadata from
			<a
				href="https://www.semanticscholar.org/"
				target="_blank"
				rel="noopener noreferrer"
				class="text-accent underline underline-offset-2 transition-colors hover:text-accent/80"
			>Semantic Scholar</a>'s batch API:
		</p>

		<ul class="ml-5 flex list-disc flex-col gap-2 text-text-secondary">
			<li><strong class="text-black">TLDR summaries</strong> — AI-generated one-line paper summaries from Semantic Scholar</li>
			<li><strong class="text-black">Citation counts</strong> — how often the paper has been cited</li>
			<li><strong class="text-black">PDF URLs</strong> — direct links to open-access versions where available</li>
			<li><strong class="text-black">Publication venues</strong> — journal or conference names</li>
			<li><strong class="text-black">Publication year</strong> — for time-based filtering</li>
		</ul>
	</section>

	<!-- Stage 4: Synthesis -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">Stage 4: Landscape Summaries</h2>
		<p class="leading-relaxed text-text-secondary">
			For each quality component, tool type, and concern theme, we produce an AI-generated
			<strong class="text-black">landscape summary</strong> synthesising findings across all
			high-relevance papers (scored ≥7/10):
		</p>

		<ol class="ml-5 flex list-decimal flex-col gap-2 text-text-secondary">
			<li>
				<strong class="text-black">Section extraction</strong> — we extract key sections
				(abstract, introduction, results, discussion, conclusions) from each paper's full text
			</li>
			<li>
				<strong class="text-black">Batch synthesis</strong> — extracted sections are sent to Claude
				in batches, which synthesises findings into structured analyses covering: executive summary,
				key findings, what's measured, what's missing, notable studies, LMIC context, and recommendations
			</li>
			<li>
				<strong class="text-black">Multi-batch merging</strong> — when there are too many papers
				for a single LLM context window, multiple batch reports are generated and then merged into
				a single coherent summary
			</li>
		</ol>
	</section>

	<!-- Quality Components -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">The Quality Framework</h2>
		<p class="leading-relaxed text-text-secondary">
			Papers are mapped to {Object.keys(FRAMEWORK).length} quality components across
			{new Set(Object.values(FRAMEWORK).map((f) => f.area)).size} areas. These components define
			what a high-quality AI tool for K-12 education should be measured on:
		</p>

		<div class="overflow-x-auto rounded-[14px] border border-black/10">
			<table class="w-full border-collapse text-sm">
				<thead>
					<tr class="border-b border-black/10 bg-surface">
						<th class="px-4 py-2.5 text-left font-semibold text-muted">Area</th>
						<th class="px-4 py-2.5 text-left font-semibold text-muted">ID</th>
						<th class="px-4 py-2.5 text-left font-semibold text-muted">Component</th>
					</tr>
				</thead>
				<tbody>
					{#each Object.values(FRAMEWORK) as fw}
						<tr class="border-b border-black/5 last:border-b-0">
							<td class="px-4 py-2 text-text-secondary">{fw.area}</td>
							<td class="px-4 py-2">
								<span class="rounded-md bg-surface-alt px-2 py-0.5 text-xs font-semibold text-text-dim">{fw.id}</span>
							</td>
							<td class="px-4 py-2 text-black">{fw.name}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</section>

	<!-- Concerns -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">Concern Themes</h2>
		<p class="leading-relaxed text-text-secondary">
			In addition to the quality framework, we identify {CONCERN_LIST.length} cross-cutting
			<strong class="text-black">concern themes</strong> — risks and challenges that span multiple
			framework categories. Papers are matched to concerns via keyword search over their title,
			summary, and full text.
		</p>

		<div class="flex flex-col gap-3">
			{#each CONCERN_LIST as concern}
				<div class="flex gap-3 rounded-[14px] border border-black/10 bg-white p-4">
					<span class="inline-block rounded-md bg-red-50 px-2 py-0.5 text-xs font-semibold text-red-700 h-fit">
						Concern
					</span>
					<div class="flex flex-col gap-1">
						<h3 class="text-sm font-semibold text-black">{concern.name}</h3>
						<p class="text-xs leading-relaxed text-text-secondary">{concern.description}</p>
					</div>
				</div>
			{/each}
		</div>
	</section>

	<!-- Tools & Technology -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">Tools & Technology</h2>
		<div class="overflow-x-auto rounded-[14px] border border-black/10">
			<table class="w-full border-collapse text-sm">
				<thead>
					<tr class="border-b border-black/10 bg-surface">
						<th class="px-4 py-2.5 text-left font-semibold text-muted">Component</th>
						<th class="px-4 py-2.5 text-left font-semibold text-muted">Technology</th>
					</tr>
				</thead>
				<tbody>
					<tr class="border-b border-black/5">
						<td class="px-4 py-2 text-text-secondary">Paper discovery</td>
						<td class="px-4 py-2 text-black">
							<a href="https://www.semanticscholar.org/" target="_blank" rel="noopener noreferrer" class="text-accent underline underline-offset-2 hover:text-accent/80">Semantic Scholar API</a>,
							HuggingFace API
						</td>
					</tr>
					<tr class="border-b border-black/5">
						<td class="px-4 py-2 text-text-secondary">Classification & synthesis</td>
						<td class="px-4 py-2 text-black">Anthropic Claude (claude-haiku-4-5)</td>
					</tr>
					<tr class="border-b border-black/5">
						<td class="px-4 py-2 text-text-secondary">Pipeline</td>
						<td class="px-4 py-2 text-black">Python 3.11+</td>
					</tr>
					<tr class="border-b border-black/5">
						<td class="px-4 py-2 text-text-secondary">Website</td>
						<td class="px-4 py-2 text-black">SvelteKit, Tailwind CSS</td>
					</tr>
					<tr class="last:border-b-0">
						<td class="px-4 py-2 text-text-secondary">Search</td>
						<td class="px-4 py-2 text-black">MiniSearch (client-side full-text search)</td>
					</tr>
				</tbody>
			</table>
		</div>
	</section>

	<!-- Limitations -->
	<section class="flex flex-col gap-4">
		<h2 class="text-xl font-semibold text-black">Limitations</h2>
		<ul class="ml-5 flex list-disc flex-col gap-2 text-text-secondary leading-relaxed">
			<li>
				<strong class="text-black">Search coverage</strong> — while we query 80+ search terms
				across multiple sources, some relevant papers may be missed if they don't match our query set
				or aren't indexed by Semantic Scholar or HuggingFace.
			</li>
			<li>
				<strong class="text-black">Classification accuracy</strong> — LLM-based classification is
				not perfect. Some papers may be mis-classified or assigned incorrect relevance scores.
				The heuristic + LLM two-stage approach reduces errors but doesn't eliminate them.
			</li>
			<li>
				<strong class="text-black">Synthesis quality</strong> — landscape summaries are AI-generated
				and may contain inaccuracies or miss nuances present in the original papers. They should
				be treated as starting points for further investigation, not as definitive reviews.
			</li>
			<li>
				<strong class="text-black">Temporal bias</strong> — the corpus reflects what's available at
				the time of search. Newly published papers won't appear until the pipeline is re-run.
			</li>
		</ul>
	</section>

	<!-- Contact -->
	<section class="flex flex-col gap-4 rounded-[14px] border border-black/10 bg-surface/50 p-6">
		<h2 class="text-xl font-semibold text-black">About This Project</h2>
		<p class="leading-relaxed text-text-secondary">
			This project is part of the
			<a href="https://www.fab-ai.org" target="_blank" rel="noopener noreferrer"
				class="text-accent underline underline-offset-2 transition-colors hover:text-accent/80">Fab AI</a>
			initiative focused on quality assurance for AI in education, particularly in low- and middle-income countries.
		</p>
	</section>
</div>
