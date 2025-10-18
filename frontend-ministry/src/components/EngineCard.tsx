import diamondMine from '../assets/images/diamond_mine.png';
import emeraldMine from '../assets/images/emerald_mine.png';
import rubyMine from '../assets/images/ruby_mine.png';
import sapphireMine from '../assets/images/sapphire_mine.png';
import onyxMine from '../assets/images/onyx_mine.png';

import diamondGem from '../assets/images/diamond_gem.png';
import emeraldGem from '../assets/images/emerald_gem.png';
import rubyGem from '../assets/images/ruby_gem.png';
import sapphireGem from '../assets/images/sapphire_gem.png';
import onyxGem from '../assets/images/onyx_gem.png';

import diamondProspect from '../assets/images/diamond_prospector.png';
import emeraldProspect from '../assets/images/emerald_prospector.png';
import rubyProspect from '../assets/images/ruby_prospector.png';
import sapphireProspect from '../assets/images/sapphire_prospector.png';
import onyxProspect from '../assets/images/onyx_prospector.png';

type GemType = 'diamond' | 'emerald' | 'ruby' | 'sapphire' | 'onyx';
type Cost = Record<GemType, number>;

interface CardInfo {
  cost: Cost;
   // doing this instead of string prevents lint because ts get angy
  engine: GemType;
  prestige: number;
  tier: number;
}
interface CardProps {
  cardInfo: CardInfo;
}

const engineImages: Record<GemType, string> = {
  diamond: diamondMine,
  sapphire: sapphireMine,
  emerald: emeraldMine,
  ruby: rubyMine,
  onyx: onyxMine,
}

const gemImages: Record<GemType, string> = {
  diamond: diamondGem,
  sapphire: sapphireGem,
  emerald: emeraldGem,
  ruby: rubyGem,
  onyx: onyxGem,
}

const prosImages: Record<GemType, string> = {
  diamond: diamondProspect,
  sapphire: sapphireProspect,
  emerald: emeraldProspect,
  ruby: rubyProspect,
  onyx: onyxProspect,
}

export default function EngineCard({ cardInfo }: CardProps) {
  return (
  <div
    className="w-80 h-96 border-2 border-gray-800 rounded-lg shadow-md relative text-2xl font-semibold"
    style={{
      backgroundImage: `url(${
        cardInfo?.tier===1 ? engineImages[cardInfo?.engine] : prosImages[cardInfo?.engine]
      })`,
      backgroundSize: 'cover',
      backgroundPosition: 'top center',
    }}
  >
    {/* Top row: prestige (left) and engine image (right) */}
    <div className="absolute w-full flex justify-between items-start p-2 bg-gray-200/60 rounded-t-md">
      {/* Prestige at top-left */}
      <div className="text-4xl">
        {cardInfo?.prestige ? cardInfo.prestige : ''}
      </div>

      {/* Engine image at top-right */}
      <div className="w-14 h-14">
        <img
          src={gemImages[cardInfo?.engine]}
          alt={cardInfo?.engine}
          className="w-full h-full object-contain"
        />
      </div>
    </div>

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
