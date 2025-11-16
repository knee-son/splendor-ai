interface cardProps {
  tier: number;
}

import backsideImage from "../assets/images/backside_card.png";
export default function EngineCard({ tier }: cardProps) {
  return (
    <div
      className="h-full aspect-[4/5] border-1 border-gray-800 rounded-lg shadow-md relative text-2xl font-semibold"
      style={{
        backgroundImage: `url(${backsideImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        filter: `hue-rotate(${120 * tier}deg)  brightness(${1 - 0.2 * tier})`,
      }}
    />
  );
}
