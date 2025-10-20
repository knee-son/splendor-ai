import React from "react";
import type { Card } from "@/types/splendor";

interface CardPageScrollbarProps {
  cards: Card[];
  cardNumber: number;
  setCardNumber: React.Dispatch<React.SetStateAction<number>>;
}

const CardPageScrollbar: React.FC<CardPageScrollbarProps> = ({
  cards,
  cardNumber,
  setCardNumber,
}) => {
  return (
    <div className="h-full overflow-y-auto bg-gray-200 border-l border-gray-300 absolute right-0 w-60">
      <ul className="flex flex-col items-center space-y-2 p-2">
        {cards.map((card, i) => (
          <button
            key={i}
            onClick={() => setCardNumber(i + 1)}
            className={`w-full h-14 rounded-md border-2 transition ${
              cardNumber === i + 1
                ? "border-blue-500 bg-white"
                : "border-transparent bg-gray-300 hover:bg-gray-400"
            }`}
          >
            {`${"I".repeat(card.tier)}: ${card.engine.charAt(0).toUpperCase() + card.engine.slice(1)}`}
          </button>
        ))}
      </ul>
    </div>
  );
};

export default CardPageScrollbar;
