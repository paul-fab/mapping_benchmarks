/**
 * Settings store — persists user preferences in localStorage.
 *
 * Usage:
 *   import { settingsStore } from '$lib/stores/settings.svelte';
 *   settingsStore.hideOldPapers;       // boolean (default: true)
 *   settingsStore.minRelevance;        // number 0-10 (default: 0 = show all)
 *   settingsStore.toggleHideOldPapers();
 */

const STORAGE_KEY = 'edubench-settings';

/** Papers published before this year are hidden by default. */
export const OLD_PAPER_CUTOFF = 2023;

interface Settings {
	hideOldPapers: boolean;
	/** Minimum relevance score to show (0 = show all, 5 = hide low-relevance). */
	minRelevance: number;
}

const DEFAULTS: Settings = {
	hideOldPapers: true,
	minRelevance: 0
};

function createSettingsStore() {
	let settings = $state<Settings>(loadFromStorage());

	function loadFromStorage(): Settings {
		if (typeof localStorage === 'undefined') return { ...DEFAULTS };
		try {
			const raw = localStorage.getItem(STORAGE_KEY);
			if (raw) {
				const parsed = JSON.parse(raw);
				return { ...DEFAULTS, ...parsed };
			}
		} catch {
			// ignore corrupt data
		}
		return { ...DEFAULTS };
	}

	function save() {
		if (typeof localStorage === 'undefined') return;
		localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
	}

	return {
		get hideOldPapers() {
			return settings.hideOldPapers;
		},
		set hideOldPapers(value: boolean) {
			settings = { ...settings, hideOldPapers: value };
			save();
		},
		toggleHideOldPapers() {
			settings = { ...settings, hideOldPapers: !settings.hideOldPapers };
			save();
		},
		get minRelevance() {
			return settings.minRelevance;
		},
		set minRelevance(value: number) {
			settings = { ...settings, minRelevance: Math.max(0, Math.min(10, value)) };
			save();
		}
	};
}

export const settingsStore = createSettingsStore();
