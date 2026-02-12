export interface Framework {
	id: string;
	area: string;
	name: string;
	description: string;
}

export interface Benchmark {
	name: string;
	slug: string;
	sourceUrl: string;
	sourceType: 'dataset' | 'paper';
	description: string;
	frameworkIds: string[];
	toolTypes: string[];
	tags: string[];
	year?: number;
	/** AI-generated one-line summary from Semantic Scholar. */
	tldr?: string;
	/** Total citation count from Semantic Scholar. */
	citationCount?: number;
	/** URL to the open-access PDF (from Semantic Scholar). */
	pdfUrl?: string;
	/** LLM-assessed relevance score for K-12 education (1-10). */
	relevanceScore?: number;
}

export interface ToolType {
	key: string;
	name: string;
	description: string;
	keyNeeds: string[];
}

export interface Concern {
	key: string;
	name: string;
	description: string;
}

export interface AreaGroup {
	area: string;
	frameworks: Framework[];
}
