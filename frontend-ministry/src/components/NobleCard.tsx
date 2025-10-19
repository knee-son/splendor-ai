import diamondGem from '../assets/images/diamond_gem.png';
import emeraldGem from '../assets/images/emerald_gem.png';
import rubyGem from '../assets/images/ruby_gem.png';
import sapphireGem from '../assets/images/sapphire_gem.png';
import onyxGem from '../assets/images/onyx_gem.png';

import onyxProspect from '../assets/images/onyx_prospector.png';

type GemType = 'diamond' | 'emerald' | 'ruby' | 'sapphire' | 'onyx';
type Cost = Record<GemType, number>;

interface Noble {
  name: string;
  cost: Cost;
  prestige: number;
  tier: number;
}
interface NobleProps {
  nobleInfo: Noble;
}

const gemImages: Record<GemType, string> = {
  diamond: diamondGem,
  sapphire: sapphireGem,
  emerald: emeraldGem,
  ruby: rubyGem,
  onyx: onyxGem,
}

export default function EngineCard({ nobleInfo }: NobleProps) {
  return (
  <div
    className="w-72 h-72 border-2 border-gray-800 rounded-lg shadow-md relative text-2xl font-semibold"
    style={{
      backgroundImage: `url(${
        onyxProspect
      })`,
      backgroundSize: 'cover',
      backgroundPosition: 'top center',
    }}
  >
    <div className="absolute w-full flex justify-end items-start p-2 bg-gray-200/60 rounded-t-md">
      <div className="text-4xl">
        {nobleInfo?.prestige ? nobleInfo.prestige : ''}
      </div>
    </div>

    {/* gem costs panel */}
    <div className="absolute bottom-2 left-2 text-lg rounded-md">
      <div className="flex flex-col">{
        Object.entries(nobleInfo?.cost || {})
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
