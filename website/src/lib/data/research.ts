/**
 * Research reports data loading.
 *
 * Reports are stored as static markdown files:
 *   - Framework categories: /static/research/{id}.md
 *   - Tool types: /static/research/tool-type/{key}.md
 *
 * Manifests list which IDs have reports:
 *   - /static/research/manifest.json         (category IDs)
 *   - /static/research/tool-type/manifest.json (tool type keys)
 */

let _catCache: Promise<Set<string>> | null = null;
let _ttCache: Promise<Set<string>> | null = null;
let _cnCache: Promise<Set<string>> | null = null;

/**
 * Load the set of framework category IDs that have research reports available.
 */
export function loadResearchIds(fetchFn: typeof fetch): Promise<Set<string>> {
	if (!_catCache) {
		_catCache = fetchFn('/research/manifest.json')
			.then((r) => {
				if (!r.ok) return new Set<string>();
				return r.json() as Promise<string[]>;
			})
			.then((ids) => new Set(ids))
			.catch(() => new Set<string>());
	}
	return _catCache;
}

/**
 * Load the set of tool-type keys that have research reports available.
 */
export function loadToolTypeResearchIds(fetchFn: typeof fetch): Promise<Set<string>> {
	if (!_ttCache) {
		_ttCache = fetchFn('/research/tool-type/manifest.json')
			.then((r) => {
				if (!r.ok) return new Set<string>();
				return r.json() as Promise<string[]>;
			})
			.then((ids) => new Set(ids))
			.catch(() => new Set<string>());
	}
	return _ttCache;
}

/**
 * Load the set of concern keys that have research reports available.
 */
export function loadConcernResearchIds(fetchFn: typeof fetch): Promise<Set<string>> {
	if (!_cnCache) {
		_cnCache = fetchFn('/research/concern/manifest.json')
			.then((r) => {
				if (!r.ok) return new Set<string>();
				return r.json() as Promise<string[]>;
			})
			.then((ids) => new Set(ids))
			.catch(() => new Set<string>());
	}
	return _cnCache;
}
