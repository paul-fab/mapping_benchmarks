<script lang="ts">
	let {
		checked = $bindable(false),
		label,
		ariaLabel = label
	}: {
		checked: boolean;
		label: string;
		ariaLabel?: string;
	} = $props();
</script>

<div class="flex shrink-0 cursor-pointer items-center gap-2 select-none">
	<span class="text-xs text-muted">{label}</span>
	<button
		role="switch"
		aria-checked={checked}
		aria-label={ariaLabel}
		onclick={() => (checked = !checked)}
		class="relative inline-flex h-5 w-9 shrink-0 items-center rounded-full transition-colors
			{checked ? 'bg-accent' : 'bg-black/15'}"
	>
		<span
			class="inline-block h-3.5 w-3.5 rounded-full bg-white shadow-sm transition-transform
				{checked ? 'translate-x-[18px]' : 'translate-x-[3px]'}"
		></span>
	</button>
</div>
