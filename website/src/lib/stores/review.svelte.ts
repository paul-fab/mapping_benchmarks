/**
 * Human review store — persists dismissed benchmark slugs in localStorage.
 *
 * Usage:
 *   import { reviewStore } from '$lib/stores/review.svelte';
 *   reviewStore.dismiss('mmlu');
 *   reviewStore.restore('mmlu');
 *   reviewStore.isDismissed('mmlu');  // true/false
 *   reviewStore.dismissed;            // Set<string>
 */

const STORAGE_KEY = 'edubench-dismissed';

function createReviewStore() {
	let dismissed = $state<Set<string>>(loadFromStorage());

	function loadFromStorage(): Set<string> {
		if (typeof localStorage === 'undefined') return new Set();
		try {
			const raw = localStorage.getItem(STORAGE_KEY);
			if (raw) {
				const arr = JSON.parse(raw);
				if (Array.isArray(arr)) return new Set(arr);
			}
		} catch {
			// ignore corrupt data
		}
		return new Set();
	}

	function save() {
		if (typeof localStorage === 'undefined') return;
		localStorage.setItem(STORAGE_KEY, JSON.stringify([...dismissed]));
	}

	return {
		get dismissed() {
			return dismissed;
		},
		get count() {
			return dismissed.size;
		},
		isDismissed(slug: string): boolean {
			return dismissed.has(slug);
		},
		dismiss(slug: string) {
			dismissed = new Set([...dismissed, slug]);
			save();
		},
		restore(slug: string) {
			const next = new Set(dismissed);
			next.delete(slug);
			dismissed = next;
			save();
		},
		toggle(slug: string) {
			if (dismissed.has(slug)) {
				this.restore(slug);
			} else {
				this.dismiss(slug);
			}
		},
		clearAll() {
			dismissed = new Set();
			save();
		},
		/** Export as JSON string (for saving review decisions externally) */
		exportJSON(): string {
			return JSON.stringify([...dismissed], null, 2);
		}
	};
}

export const reviewStore = createReviewStore();
