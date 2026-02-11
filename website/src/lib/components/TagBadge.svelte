<script lang="ts">
	let {
		label,
		variant = 'default'
	}: {
		label: string;
		variant?: 'default' | 'accent' | 'muted';
	} = $props();

	const variantClasses: Record<string, string> = {
		default: 'bg-surface text-text-body border-black/10',
		accent: 'bg-accent/10 text-accent border-accent/20',
		muted: 'bg-surface-alt text-muted border-black/5'
	};
</script>

<span
	class="inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium {variantClasses[variant]}"
>
	{label}
</span>
