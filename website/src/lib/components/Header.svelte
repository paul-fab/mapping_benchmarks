<script lang="ts">
	import fabLogo from '$lib/assets/fab-ai-logo.svg';
</script>

<header class="sticky top-0 z-50 w-full border-b border-black/10 bg-white">
	<div class="mx-auto flex h-14 max-w-[1440px] items-center justify-between px-4 sm:h-[70px] sm:px-8">
		<a href="/" class="flex items-center gap-2 sm:gap-4">
			<img src={fabLogo} alt="Fab AI" class="h-5 sm:h-6" />
			<span class="hidden h-5 w-px bg-black/15 sm:block"></span>
			<div class="flex items-center gap-1.5 sm:gap-2">
				<span class="text-base font-semibold text-black sm:text-xl">EdLab</span>
				<span class="rounded-full bg-accent/10 px-2 py-0.5 text-xs font-medium text-accent sm:px-3 sm:text-sm">Mapper</span>
			</div>
		</a>

		<nav class="flex items-center gap-0.5 sm:gap-1">
			<a
				href="/"
				class="rounded-full px-2.5 py-1.5 text-sm text-black/80 transition-colors hover:bg-black/5 sm:px-4 sm:py-2 sm:text-base"
			>
				Quality Components
			</a>
			<a
				href="/research"
				class="rounded-full px-2.5 py-1.5 text-sm text-black/80 transition-colors hover:bg-black/5 sm:px-4 sm:py-2 sm:text-base"
			>
				Landscape Summary
			</a>
			<a
				href="https://www.fab-ai.org/initiatives/ai-for-education/edtech-quality/benchmarks?benchmark=CDPK&models=%5B%5D&cost=10&pageView=table"
				target="_blank"
				rel="noopener noreferrer"
				class="rounded-full px-2.5 py-1.5 text-sm text-black/80 transition-colors hover:bg-black/5 sm:px-4 sm:py-2 sm:text-base"
			>
				AI Benchmark Leaderboard
			</a>
		</nav>
	</div>
</header>
