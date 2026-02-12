<script lang="ts">
	import fabLogo from '$lib/assets/fab-ai-logo.svg';
</script>

<footer class="mt-auto border-t border-black/10 bg-white">
	<div class="mx-auto max-w-[1440px] px-4 py-8 sm:px-8 sm:py-12">
		<div class="flex flex-col gap-8 md:flex-row md:items-start md:justify-between">
			<div class="flex flex-col gap-4">
				<a href="https://www.fab-ai.org" target="_blank" rel="noopener noreferrer" class="flex items-center gap-4">
					<img src={fabLogo} alt="Fab AI" class="h-6" />
					<span class="h-5 w-px bg-black/15"></span>
					<div class="flex items-center gap-2">
						<span class="text-xl font-semibold text-black">EdLab</span>
						<span class="rounded-full bg-accent/10 px-3 py-0.5 text-sm font-medium text-accent">Mapper</span>
					</div>
				</a>
				<p class="max-w-md text-base leading-relaxed text-black/60">
					Mapping AI benchmarks and evals to quality components for education in LMICs.
					Identifying what we can measure and where the gaps are.
				</p>
			</div>

		<div class="flex flex-col gap-3 text-sm text-muted">
			<a href="/methods" class="transition-colors hover:text-black">Methods</a>
			<a href="https://www.fab-ai.org/initiatives/ai-for-education/edtech-quality/benchmarks?benchmark=CDPK&models=%5B%5D&cost=10&pageView=table" target="_blank" rel="noopener noreferrer" class="transition-colors hover:text-black">AI Benchmark Leaderboard</a>
			<a href="https://www.fab-ai.org" target="_blank" rel="noopener noreferrer" class="transition-colors hover:text-black">fab-ai.org</a>
		</div>
		</div>
	</div>
</footer>
