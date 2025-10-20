import type { Card, GemType } from '@/types/splendor';

import diamondGem from '../assets/images/diamond_gem.png';
import emeraldGem from '../assets/images/emerald_gem.png';
import rubyGem from '../assets/images/ruby_gem.png';
import sapphireGem from '../assets/images/sapphire_gem.png';
import onyxGem from '../assets/images/onyx_gem.png';

const tierToCategory: Record<number, string> = {
  1: "mine",
  2: "prospector",
  3: "cafe",
}

const gemImages: Record<GemType, string> = {
  diamond: diamondGem,
  sapphire: sapphireGem,
  emerald: emeraldGem,
  ruby: rubyGem,
  onyx: onyxGem,
}

interface CardProps {
  cardInfo: Card;
}

const images = import.meta.glob('@/assets/images/*.png', { eager: true });

export default function EngineCard({ cardInfo }: CardProps) {
  const engine = cardInfo?.engine;
  const category = tierToCategory[cardInfo?.tier];

  const imageKey = `/src/assets/images/${engine}_${category}.png`;
  const imageSrc = (images[imageKey] as { default: string })?.default;

  return (
  <div
    className="w-80 h-96 border-2 border-gray-800 rounded-lg shadow-md relative text-2xl font-semibold"
    style={{
      backgroundImage: `url(${imageSrc})`,
      backgroundSize: 'cover',
      backgroundPosition: 'top center',
    }}
  >
    <div className="absolute w-full flex justify-between items-start p-2 bg-gray-200/60 rounded-t-md">
      <div className="text-4xl">
        {cardInfo?.prestige ? cardInfo.prestige : ''}
      </div>

      <div className="w-14 h-14">
        <img
          src={gemImages[cardInfo?.engine]}
          alt={cardInfo?.engine}
          className="w-full h-full object-contain"
        />
      </div>
    </div>

    {/* gem costs section */}
    <div className="absolute bottom-2 left-2 text-lg rounded-md">
      <div className="flex flex-col">{
        Object.entries(cardInfo?.cost || {})
          .filter(([,amount]) => !!amount)
          .map(([gem, amount]) => {
            const gemKey = gem as GemType;
            return (
              <div key={gemKey} className="flex items-center gap-1">
                <img 
                  src={gemImages[gemKey]}
                  alt={gemKey}
                  className="w-7 h-7 object-contain" />
                <span>{amount}</span>
              </div>
            );
          })
        }</div>
    </div>
  </div>
  );
}
