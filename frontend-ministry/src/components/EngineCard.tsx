import diamondMine from '../assets/images/diamond_mine.png';
import emeraldMine from '../assets/images/emerald_mine.png';
import rubyMine from '../assets/images/ruby_mine.png';
import sapphireMine from '../assets/images/sapphire_mine.png';
import onyxMine from '../assets/images/onyx_mine.png';

const engineImages = {
  diamond: diamondMine,
  sapphire: sapphireMine,
  emerald: emeraldMine,
  ruby: rubyMine,
  onyx: onyxMine,
}

interface Cost {
  diamond: number;
  sapphire: number;
  emerald: number;
  ruby: number;
  onyx: number;
}

interface CardInfo {
  cost: Cost;
   // doing this instead of string prevents lint because ts get angy
  engine: 'diamond' | 'sapphire' | 'emerald' | 'ruby' | 'onyx';
  prestige: number;
  tier: number;
}

interface CardProps {
  cardInfo: CardInfo;
}

export default function EngineCard({ cardInfo }: CardProps) {
  return (
  <div
    className="w-80 h-96 border-2 border-gray-800 flex flex-col items-center justify-center text-2xl font-semibold rounded-lg shadow-md"
    style={{
      backgroundImage: `url(${engineImages[cardInfo?.engine]})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }}
  >
      {cardInfo?.engine} <br />
      {JSON.stringify(cardInfo?.cost)} <br />
      {cardInfo?.prestige} <br />
      {cardInfo?.tier} <br />
    </div>
  );
}
