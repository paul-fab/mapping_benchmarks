<script lang="ts">
	import fabLogo from '$lib/assets/fab-ai-logo.svg';

	let menuOpen = $state(false);

	function toggleMenu() {
		menuOpen = !menuOpen;
	}

	function closeMenu() {
		menuOpen = false;
	}
</script>

<header class="sticky top-0 z-50 w-full border-b border-black/10 bg-white">
	<div class="mx-auto flex h-14 max-w-[1440px] items-center justify-between gap-4 px-4 sm:h-[70px] sm:px-8">
		<a href="/" class="flex shrink-0 items-center gap-2 sm:gap-4" onclick={closeMenu}>
			<img src={fabLogo} alt="Fab AI" class="h-5 sm:h-6" />
			<span class="hidden h-5 w-px bg-black/15 sm:block"></span>
			<div class="flex items-center gap-1.5 sm:gap-2">
				<span class="text-base font-semibold text-black sm:text-xl">EdLab</span>
				<span class="rounded-full bg-accent/10 px-2 py-0.5 text-xs font-medium text-accent sm:px-3 sm:text-sm">Mapper</span>
			</div>
		</a>

		<!-- Desktop Navigation -->
		<nav class="hidden items-center gap-1 md:flex">
			<a
				href="/"
				class="rounded-full px-4 py-2 text-base text-black/80 transition-colors hover:bg-black/5"
			>
				Quality Components
			</a>
			<a
				href="/research"
				class="rounded-full px-4 py-2 text-base text-black/80 transition-colors hover:bg-black/5"
			>
				Landscape Summary
			</a>
			<a
				href="/#concerns"
				class="rounded-full px-4 py-2 text-base text-black/80 transition-colors hover:bg-black/5"
			>
				Concerns
			</a>
			<a
				href="/methods"
				class="rounded-full px-4 py-2 text-base text-black/80 transition-colors hover:bg-black/5"
			>
				Methods
			</a>
			<a
				href="https://www.fab-ai.org/initiatives/ai-for-education/edtech-quality/benchmarks?benchmark=CDPK&models=%5B%5D&cost=10&pageView=table"
				target="_blank"
				rel="noopener noreferrer"
				class="rounded-full px-4 py-2 text-base text-black/80 transition-colors hover:bg-black/5"
			>
				AI Benchmark Leaderboard
			</a>
		</nav>

		<!-- Mobile Menu Button -->
		<button
			onclick={toggleMenu}
			class="flex items-center justify-center rounded-full p-2 text-black/80 transition-colors hover:bg-black/5 md:hidden"
			aria-label="Toggle menu"
			aria-expanded={menuOpen}
		>
			{#if menuOpen}
				<svg
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
				</svg>
			{:else}
				<svg
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
				</svg>
			{/if}
		</button>
	</div>

	<!-- Mobile Menu Dropdown -->
	{#if menuOpen}
		<div class="border-t border-black/10 bg-white md:hidden">
			<nav class="mx-auto flex max-w-[1440px] flex-col gap-1 px-4 py-3 sm:px-8">
				<a
					href="/"
					onclick={closeMenu}
					class="rounded-full px-4 py-2.5 text-base text-black/80 transition-colors hover:bg-black/5"
				>
					Quality Components
				</a>
				<a
					href="/research"
					onclick={closeMenu}
					class="rounded-full px-4 py-2.5 text-base text-black/80 transition-colors hover:bg-black/5"
				>
					Landscape Summary
				</a>
				<a
					href="/#concerns"
					onclick={closeMenu}
					class="rounded-full px-4 py-2.5 text-base text-black/80 transition-colors hover:bg-black/5"
				>
					Concerns
				</a>
				<a
					href="/methods"
					onclick={closeMenu}
					class="rounded-full px-4 py-2.5 text-base text-black/80 transition-colors hover:bg-black/5"
				>
					Methods
				</a>
				<a
					href="https://www.fab-ai.org/initiatives/ai-for-education/edtech-quality/benchmarks?benchmark=CDPK&models=%5B%5D&cost=10&pageView=table"
					target="_blank"
					rel="noopener noreferrer"
					onclick={closeMenu}
					class="rounded-full px-4 py-2.5 text-base text-black/80 transition-colors hover:bg-black/5"
				>
					AI Benchmark Leaderboard
				</a>
			</nav>
		</div>
	{/if}
</header>
