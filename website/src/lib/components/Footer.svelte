<script lang="ts">
	import fabLogo from '$lib/assets/fab-ai-logo.svg';
</script>

<footer class="mt-auto border-t border-black/10 bg-white">
	<div class="mx-auto max-w-[1440px] px-4 py-8 sm:px-8 sm:py-12">
		<div class="flex flex-col gap-8 md:flex-row md:items-start md:justify-between">
			<div class="flex flex-col gap-4">
				<a href="https://fab-ai.org" target="_blank" rel="noopener noreferrer" class="flex items-center gap-4">
					<img src={fabLogo} alt="Fab AI" class="h-6" />
					<span class="h-5 w-px bg-black/15"></span>
					<div class="flex items-center gap-2">
						<span class="text-xl font-semibold text-black">EduBench</span>
						<span class="rounded-full bg-accent/10 px-3 py-0.5 text-sm font-medium text-accent">Mapper</span>
					</div>
				</a>
				<p class="max-w-md text-base leading-relaxed text-black/60">
					Mapping AI benchmarks to an education framework for LMICs.
					Identifying what we can measure and where the gaps are.
				</p>
			</div>

			<div class="flex flex-col gap-3 text-sm text-muted">
				<a href="https://fab-ai.org" target="_blank" rel="noopener noreferrer" class="transition-colors hover:text-black">fab-ai.org</a>
			</div>
		</div>
	</div>
</footer>
