<script lang="ts">
	import '../app.css';
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<title>EduBench Mapper</title>
	<meta name="description" content="Mapping AI benchmarks to education framework categories for LMICs" />
</svelte:head>

<div class="flex min-h-screen flex-col bg-white font-sans text-black">
	<Header />
	<main class="flex-1">
		{@render children()}
	</main>
	<Footer />
</div>
