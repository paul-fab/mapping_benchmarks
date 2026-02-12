// Re-export public API for convenient `$lib` imports
export type { Benchmark, Framework, ToolType, AreaGroup } from './types';
export {
	loadBenchmarks,
	getAvailableYears,
	applyYearCutoff,
	filterBenchmarks
} from './data/benchmarks';
export { FRAMEWORK, getAreaGroups } from './data/framework';
export { TOOL_TYPES, getToolTypeName } from './data/tool-types';
export { reviewStore } from './stores/review.svelte';
export { settingsStore, OLD_PAPER_CUTOFF } from './stores/settings.svelte';
