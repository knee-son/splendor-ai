import type { CoinType } from "@/types/splendor";

import diamondGem from "../assets/images/diamond_gem.png";
import emeraldGem from "../assets/images/emerald_gem.png";
import rubyGem from "../assets/images/ruby_gem.png";
import sapphireGem from "../assets/images/sapphire_gem.png";
import onyxGem from "../assets/images/onyx_gem.png";
import goldLump from "../assets/images/gold_lump.png";

interface CoinProps {
  coin: CoinType;
}

interface CoinDetails {
  image: string;
  background: string;
  border: string;
}

const coinInfo: Record<CoinType, object> = {
  diamond: {
    image: diamondGem,
    background: "rgba(238, 236, 236, 1)",
    borderColor: "rgba(186, 182, 182, 1)",
  },
  sapphire: {
    image: sapphireGem,
    background: "rgba(36, 135, 255, 1)",
    borderColor: "rgba(0, 40, 158, 1)",
  },
  emerald: {
    image: emeraldGem,
    background: "rgba(41, 203, 23, 1)",
    borderColor: "rgba(1, 91, 15, 1)",
  },
  ruby: {
    image: rubyGem,
    background: "rgba(237, 121, 121, 1)",
    borderColor: "rgba(61, 6, 10, 1)",
  },
  onyx: {
    image: onyxGem,
    background: "rgba(255, 197, 146, 1)",
    borderColor: "rgba(35, 13, 0, 1)",
  },
  gold: {
    image: goldLump,
    backgroundColor: "rgba(255, 239, 117, 1)",
    borderColor: "rgba(170, 122, 0, 1)",
  },
};

export default function GemCoin({ coin }: CoinProps) {
  const { image, ...style } = coinInfo[coin] as CoinDetails;

  return (
    <div className="bottom-2 left-2 rounded-full border-2" style={style}>
      <img src={image} alt={coin} className="object-contain" />
    </div>
  );
}
