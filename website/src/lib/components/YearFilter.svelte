<script lang="ts">
	let {
		years,
		selectedYear = $bindable<number | null>(null)
	}: {
		years: number[];
		selectedYear: number | null;
	} = $props();
</script>

<div class="flex flex-wrap items-center gap-1.5">
	<button
		onclick={() => (selectedYear = null)}
		class="rounded-full px-3 py-1 text-xs font-medium transition-colors
			{selectedYear === null
				? 'bg-black text-white'
				: 'border border-black/10 text-muted hover:border-black/30 hover:text-black'}"
	>
		All years
	</button>
	{#each years as year}
		<button
			onclick={() => (selectedYear = selectedYear === year ? null : year)}
			class="rounded-full px-3 py-1 text-xs font-medium transition-colors
				{selectedYear === year
					? 'bg-black text-white'
					: 'border border-black/10 text-muted hover:border-black/30 hover:text-black'}"
		>
			{year}
		</button>
	{/each}
</div>
