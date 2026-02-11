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
}

export interface ToolType {
	key: string;
	name: string;
	description: string;
	keyNeeds: string[];
}

export interface AreaGroup {
	area: string;
	frameworks: Framework[];
}
