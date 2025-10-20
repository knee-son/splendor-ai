export type GemType = 'diamond' | 'emerald' | 'ruby' | 'sapphire' | 'onyx';
export type Cost = Record<GemType, number>;

export interface Card {
  cost: Cost;
  // doing this instead of string prevents lint because ts get angy
  engine: GemType;
  prestige: number;
  tier: number;
}

export interface Noble {
  name: string;
  cost: Cost;
  prestige: number;
  tier: number;
}
