import type { Noble, GemType } from "@/types/splendor";

import diamondGem from "../assets/images/diamond_gem.png";
import emeraldGem from "../assets/images/emerald_gem.png";
import rubyGem from "../assets/images/ruby_gem.png";
import sapphireGem from "../assets/images/sapphire_gem.png";
import onyxGem from "../assets/images/onyx_gem.png";

interface NobleProps {
  nobleInfo: Noble;
}

const gemImages: Record<GemType, string> = {
  diamond: diamondGem,
  sapphire: sapphireGem,
  emerald: emeraldGem,
  ruby: rubyGem,
  onyx: onyxGem,
};

const images = import.meta.glob("@/assets/images/*.png", { eager: true });

export default function NobleCard({ nobleInfo }: NobleProps) {
  const name = nobleInfo?.name;

  const imageKey = `/src/assets/images/noble_${name}.png`;
  const imageSrc = (images[imageKey] as { default: string })?.default;

  return (
    <div
      className="h-full aspect-square border-1 border-gray-800 rounded-lg shadow-md relative text-2xl font-semibold"
      style={{
        backgroundImage: `url(${imageSrc})`,
        backgroundSize: "cover",
        backgroundPosition: "top center",
      }}
    >
      <div className="absolute h-1/5 w-full flex justify-between items-start p-2 bg-gray-400/60 rounded-t-md">
        <div
          className="flex items-center justify-center h-full font-extrabold text-white"
          style={{ WebkitTextStroke: "1px #111111" }}
        >
          {nobleInfo?.prestige ? nobleInfo.prestige : ""}
        </div>
      </div>

      {/* gem costs panel */}
      <div className="absolute bottom-2 left-2 text-lg rounded-md">
        <div className="flex flex-col">
          {Object.entries(nobleInfo?.cost || {})
            .filter(([, amount]) => !!amount)
            .map(([gem, amount]) => {
              const gemKey = gem as GemType;
              return (
                <div key={gemKey} className="flex items-center gap-0.5">
                  <img
                    src={gemImages[gemKey]}
                    alt={gemKey}
                    className="w-1/3 h-1/3 object-contain"
                  />
                  <span className="text-sm text-white">{amount}</span>
                </div>
              );
            })}
        </div>
      </div>
    </div>
  );
}
