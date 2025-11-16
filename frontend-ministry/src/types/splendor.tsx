export type GemType = "diamond" | "emerald" | "ruby" | "sapphire" | "onyx";
export type TierKey = "t1" | "t2" | "t3";

export type Cost = Record<GemType, number>;
export type Coins = Record<GemType | "gold", number>;

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

interface Tier {
  pile: Array<Card>;
  revealed: Array<Card>;
}

interface Player {
  cards: Array<Card>;
  coins: Coins;
}

export interface State {
  bank: Coins;
  cards: Record<TierKey, Tier>;
  current_player: number;
  last_chance: boolean;
  nobles: Array<Noble>;
  players: Array<Player>;
}
