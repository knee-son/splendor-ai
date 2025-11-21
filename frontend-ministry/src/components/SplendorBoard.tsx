import type { State, TierKey, CoinType } from "@/types/splendor";
import { useEffect, useState, useRef } from "react";

import NobleCard from "@/components/NobleCard";
import EngineCard from "@/components/EngineCard";
import EngineUnderside from "@/components/EngineUnderside";
import GemCoin from "@/components/GemCoin";

interface GameProps {
  gameState: State | null;
  isFetching: boolean;
}

export default function SplendorBoard({ gameState, isFetching }: GameProps) {
  const MAX_BANK_COINS = 5 + 7 * 5;

  const nobleRefs = useRef<(HTMLDivElement | null)[]>([]);
  const cardRefs = useRef<(HTMLDivElement | null)[][]>([]);
  const undersideRefs = useRef<(HTMLDivElement | null)[]>([]);

  function moveCardToCard(start: HTMLElement, end: HTMLElement) {
    const cardRect = start.getBoundingClientRect();
    const underRect = end.getBoundingClientRect();

    const dx = underRect.left - cardRect.left;
    const dy = underRect.top - cardRect.top;

    start.style.transition = "transform 0.4s cubic-bezier(.2, .8, .2, 1)";
    start.style.transform = `translate(${dx}px, ${dy}px) scale(0.7)`;

    end.style.transition = "transform 0.4s cubic-bezier(.2, .8, .2, 1)";
    end.style.transform = "scale(1.05) rotate(5deg)";
    end.style.filter = "saturate(.5)";
  }

  useEffect(() => {
    if (isFetching) {
      nobleRefs.current.slice(1).forEach((el) => {
        moveCardToCard(el!, nobleRefs.current[0]!);
      });
      cardRefs.current.forEach((row, i) => {
        row.forEach((el) => moveCardToCard(el!, undersideRefs.current[i]!));
      });
    } else {
      nobleRefs.current.forEach((el) => {
        if (el) {
          el.style.transform = "none";
          el.style.filter = "none";
        }
      });
      undersideRefs.current!.forEach((el) => {
        if (el) {
          el.style.transform = "none";
          el.style.filter = "none";
        }
      });
      cardRefs.current.forEach((row) => {
        row.forEach((el) => {
          if (el) {
            el.style.transform = "none";
          }
        });
      });
    }
  }, [isFetching]);

  return (
    <div className="w-4/5 aspect-[16/9] flex flex-row">
      {/* cards & nobles */}
      <div className="h-full flex flex-wrap bg-[#d1d5db] p-8 rounded-2xl">
        <div className="h-full">
          {/* TODO: convert this to a ternary if we have a loading state for cards & nobles */}
          <div className="flex h-1/6 justify-center gap-4">
            {gameState &&
              gameState.nobles.map((noble, i) => (
                <div
                  ref={(el) => {
                    nobleRefs.current[i] = el;
                  }}
                  style={{ zIndex: `${4 - i}` }}
                >
                  <NobleCard key={i} nobleInfo={noble} />
                </div>
              ))}
          </div>

          <div className="flex flex-col h-full gap-y-2 mt-8">
            {["t3", "t2", "t1"].map((tier, i) => (
              <div className="flex h-1/4 justify-center gap-x-2">
                {gameState?.cards[tier as TierKey].revealed[0] && (
                  <div
                    ref={(el) => {
                      undersideRefs.current[i] = el;
                    }}
                    style={{ zIndex: 999 }}
                  >
                    <EngineUnderside tier={2 - i} />
                  </div>
                )}
                {gameState &&
                  gameState.cards[tier as TierKey].revealed.map((card, j) => (
                    <div
                      ref={(el) => {
                        if (!cardRefs.current[i]) cardRefs.current[i] = [];
                        cardRefs.current[i][j] = el;
                      }}
                      className="relative transform-gpu"
                      style={{ zIndex: `${4 - j}` }}
                    >
                      <EngineCard key={j} cardInfo={card} />
                    </div>
                  ))}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* bank */}
      <div className="w-1/3 mx-auto flex flex-col bg-slate-800  rounded-2xl">
        <div className="w-full h-1/3 grid grid-cols-2 grid-rows-3 gap-2 p-2">
          {gameState &&
            Object.entries(gameState.bank).map(([name, amt]) => (
              <div className="relative bg-slate-900 rounded-l">
                {Array.from({ length: amt }, (_, i) => (
                  <div
                    key={i}
                    className="absolute h-[80%] top-[10%] aspect-square"
                    style={{
                      left: `${i * 7 + 3}%`,
                      zIndex: MAX_BANK_COINS - i,
                    }}
                  >
                    <GemCoin coin={name as CoinType} />
                  </div>
                ))}
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
