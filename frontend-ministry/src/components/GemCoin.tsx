import type { CoinType } from "@/types/splendor";

import diamondGem from "../assets/images/diamond_gem.png";
import emeraldGem from "../assets/images/emerald_gem.png";
import rubyGem from "../assets/images/ruby_gem.png";
import sapphireGem from "../assets/images/sapphire_gem.png";
import onyxGem from "../assets/images/onyx_gem.png";
import goldLump from "../assets/images/gold_lump.png";

interface CoinProps {
  coinType: CoinType;
}

const coinImages: Record<CoinType, string> = {
  diamond: diamondGem,
  sapphire: sapphireGem,
  emerald: emeraldGem,
  ruby: rubyGem,
  onyx: onyxGem,
  gold: goldLump,
};

export default function GemCoin({ coinType }: CoinProps) {
  const gemImage = coinImages[coinType];

  return (
    <div className="bottom-2 left-2 text-lg rounded-full bg-amber-400">
      <div className="flex flex-col">
        <img
          src={gemImage}
          alt={coinType}
          className="w-1/3 h-1/3 object-contain"
        />
      </div>
    </div>
  );
}
