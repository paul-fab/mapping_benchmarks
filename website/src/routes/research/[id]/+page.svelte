<script lang="ts">
	import { marked } from 'marked';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// Parse the markdown into sections (split on h2 headings)
	interface Section {
		id: string;
		title: string;
		html: string;
	}

	function parseIntoSections(md: string): { title: string; sections: Section[] } {
		// Extract the h1 title
		const h1Match = md.match(/^#\s+(.+)$/m);
		const title = h1Match ? h1Match[1] : data.framework.name;

		// Split on h2 headings
		const h2Pattern = /^## (.+)$/gm;
		const parts: Section[] = [];
		let lastIndex = 0;
		let lastTitle = '';
		let match: RegExpExecArray | null;

		// Remove the h1 line from content
		const content = md.replace(/^#\s+.+\n*/m, '');

		const matches: { index: number; title: string }[] = [];
		while ((match = h2Pattern.exec(content)) !== null) {
			matches.push({ index: match.index, title: match[1] });
		}

		for (let i = 0; i < matches.length; i++) {
			const start = matches[i].index;
			const end = i + 1 < matches.length ? matches[i + 1].index : content.length;
			const sectionMd = content.slice(start, end);
			const sectionTitle = matches[i].title;
			const id = sectionTitle
				.toLowerCase()
				.replace(/[^a-z0-9]+/g, '-')
				.replace(/^-|-$/g, '');

			// Remove the h2 heading from the section body
			const body = sectionMd.replace(/^## .+\n*/m, '');

			parts.push({
				id,
				title: sectionTitle,
				html: marked(body) as string
			});
		}

		return { title, sections: parts };
	}

	const parsed = $derived(parseIntoSections(data.markdown));

	// Track which sections are expanded (Executive Summary always open)
	let expandedSections = $state<Set<string>>(new Set(['executive-summary']));

	function toggleSection(id: string) {
		const next = new Set(expandedSections);
		if (next.has(id)) {
			next.delete(id);
		} else {
			next.add(id);
		}
		expandedSections = next;
	}

	function expandAll() {
		expandedSections = new Set(parsed.sections.map((s) => s.id));
	}

	function collapseAll() {
		expandedSections = new Set(['executive-summary']);
	}

	// Section icons
	function getSectionIcon(id: string): string {
		if (id === 'executive-summary') return '📋';
		if (id === 'key-themes') return '🔍';
		if (id.includes('measured') || id.includes('gaps') || id.includes('critical')) return '📊';
		if (id === 'notable-benchmarks' || id.includes('datasets')) return '📐';
		if (id === 'methodological-trends') return '🔬';
		if (id === 'recommendations') return '💡';
		if (id === 'key-papers') return '📄';
		if (id.includes('cognitive')) return '🧠';
		return '📝';
	}
</script>

<div class="mx-auto flex max-w-[1440px] flex-col gap-8 px-4 py-8 sm:px-8 sm:py-12">
	<!-- Breadcrumb -->
	<nav class="flex flex-wrap items-center gap-2 text-sm text-muted">
		<a href="/" class="transition-colors hover:text-black">Framework</a>
		<span>/</span>
		<a href="/framework/{data.framework.id}" class="transition-colors hover:text-black">
			{data.framework.name}
		</a>
		<span>/</span>
		<span class="text-black">Research</span>
	</nav>

	<!-- Header -->
	<div class="flex flex-col gap-4">
		<div class="flex flex-wrap items-center gap-3">
			<span
				class="inline-block min-w-[2.5rem] rounded-md bg-accent/10 px-2 py-1 text-center text-sm font-semibold text-accent"
			>
				{data.framework.id}
			</span>
			<span class="rounded-full bg-green-50 px-3 py-1 text-xs font-medium text-green-700">
				Research Report
			</span>
		</div>
		<h1 class="text-2xl font-medium text-black sm:text-3xl">{parsed.title}</h1>
		<p class="text-text-secondary">{data.framework.description}</p>
	</div>

	<!-- Process explanation -->
	<div class="rounded-[14px] border border-black/10 bg-surface/50 px-5 py-4">
		<p class="text-sm leading-relaxed text-text-secondary">
			<span class="font-medium text-black">How this was produced:</span> We identified high-relevance
			papers (scored ≥7/10) classified under this category, extracted key sections (abstract,
			introduction, results, discussion, conclusions) from each, then used Claude to synthesise findings
			into a structured analysis. The report below reflects what the research covers — and what it
			doesn't.
		</p>
	</div>

	<!-- Navigation links -->
	<div class="flex flex-wrap items-center gap-3">
		<a
			href="/framework/{data.framework.id}"
			class="inline-flex items-center gap-2 rounded-full border border-black/10 px-4 py-2 text-sm font-medium text-muted transition-colors hover:border-accent/30 hover:text-accent"
		>
			<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
				<path d="M19 12H5m7-7l-7 7 7 7" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			View benchmarks
		</a>
		<button
			onclick={expandAll}
			class="rounded-full border border-black/10 px-4 py-2 text-sm font-medium text-muted transition-colors hover:border-accent/30 hover:text-accent"
		>
			Expand all
		</button>
		<button
			onclick={collapseAll}
			class="rounded-full border border-black/10 px-4 py-2 text-sm font-medium text-muted transition-colors hover:border-accent/30 hover:text-accent"
		>
			Collapse all
		</button>
	</div>

	<!-- Table of contents -->
	<div class="flex flex-wrap gap-2">
		{#each parsed.sections as section}
			<button
				onclick={() => {
					if (!expandedSections.has(section.id)) {
						toggleSection(section.id);
					}
					// Scroll to section after a tick
					setTimeout(() => {
						document.getElementById(section.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
					}, 50);
				}}
				class="rounded-full px-3 py-1.5 text-xs font-medium transition-colors
					{expandedSections.has(section.id)
						? 'bg-accent/10 text-accent'
						: 'bg-surface text-muted hover:bg-accent/5 hover:text-accent'}"
			>
				{getSectionIcon(section.id)}
				{section.title}
			</button>
		{/each}
	</div>

	<!-- Sections -->
	<div class="flex flex-col gap-4">
		{#each parsed.sections as section (section.id)}
			{@const isExpanded = expandedSections.has(section.id)}
			<div
				id={section.id}
				class="scroll-mt-24 rounded-[14px] border transition-colors
					{isExpanded ? 'border-black/15 bg-white shadow-[0px_2px_8px_0px_rgba(0,0,0,0.06)]' : 'border-black/10 bg-white hover:border-black/20'}"
			>
				<button
					onclick={() => toggleSection(section.id)}
					class="flex w-full items-center gap-3 px-5 py-4 text-left sm:px-6"
					aria-expanded={isExpanded}
					aria-controls="{section.id}-content"
				>
					<span class="text-lg">{getSectionIcon(section.id)}</span>
					<h2 class="flex-1 text-base font-semibold text-black sm:text-lg">{section.title}</h2>
					<svg
						class="h-5 w-5 shrink-0 text-muted transition-transform duration-200
							{isExpanded ? 'rotate-180' : ''}"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" />
					</svg>
				</button>

				{#if isExpanded}
					<div
						id="{section.id}-content"
						class="prose border-t border-black/5 px-5 pb-6 pt-4 sm:px-6"
					>
						{@html section.html}
					</div>
				{/if}
			</div>
		{/each}
	</div>
</div>

<style>
	/* Prose styling for rendered markdown */
	:global(.prose) {
		color: #333;
		line-height: 1.8;
		font-size: 0.95rem;
	}

	:global(.prose h3) {
		font-size: 1.1rem;
		font-weight: 600;
		margin-top: 1.5rem;
		margin-bottom: 0.5rem;
		color: #1a1a1a;
	}

	:global(.prose h4) {
		font-size: 1rem;
		font-weight: 600;
		margin-top: 1.25rem;
		margin-bottom: 0.5rem;
		color: #1a1a1a;
	}

	:global(.prose p) {
		margin-top: 0.625rem;
		margin-bottom: 0.625rem;
	}

	:global(.prose strong) {
		font-weight: 600;
		color: #1a1a1a;
	}

	:global(.prose em) {
		font-style: italic;
	}

	:global(.prose ul) {
		list-style: disc;
		padding-left: 1.5rem;
		margin-top: 0.5rem;
		margin-bottom: 0.5rem;
	}

	:global(.prose ol) {
		list-style: decimal;
		padding-left: 1.5rem;
		margin-top: 0.5rem;
		margin-bottom: 0.5rem;
	}

	:global(.prose li) {
		margin-top: 0.2rem;
		margin-bottom: 0.2rem;
	}

	:global(.prose li p) {
		margin-top: 0.2rem;
		margin-bottom: 0.2rem;
	}

	:global(.prose a) {
		color: var(--color-accent, #2563eb);
		text-decoration: underline;
		text-underline-offset: 2px;
		transition: color 0.15s;
	}

	:global(.prose a:hover) {
		color: #1d4ed8;
	}

	:global(.prose blockquote) {
		border-left: 3px solid rgba(0, 0, 0, 0.12);
		padding-left: 1rem;
		margin-left: 0;
		margin-top: 0.75rem;
		margin-bottom: 0.75rem;
		color: #555;
		font-style: italic;
	}

	:global(.prose table) {
		width: 100%;
		border-collapse: collapse;
		margin-top: 0.75rem;
		margin-bottom: 0.75rem;
		font-size: 0.875rem;
	}

	:global(.prose th) {
		text-align: left;
		padding: 0.5rem 0.75rem;
		border-bottom: 2px solid rgba(0, 0, 0, 0.12);
		font-weight: 600;
		color: #1a1a1a;
	}

	:global(.prose td) {
		padding: 0.5rem 0.75rem;
		border-bottom: 1px solid rgba(0, 0, 0, 0.05);
	}

	:global(.prose hr) {
		border: none;
		border-top: 1px solid rgba(0, 0, 0, 0.08);
		margin-top: 1.5rem;
		margin-bottom: 1.5rem;
	}

	:global(.prose code) {
		background: rgba(0, 0, 0, 0.04);
		padding: 0.1rem 0.25rem;
		border-radius: 3px;
		font-size: 0.85em;
	}

	:global(.prose pre) {
		background: rgba(0, 0, 0, 0.03);
		padding: 0.75rem;
		border-radius: 8px;
		overflow-x: auto;
		margin-top: 0.75rem;
		margin-bottom: 0.75rem;
	}

	:global(.prose pre code) {
		background: none;
		padding: 0;
	}
</style>
