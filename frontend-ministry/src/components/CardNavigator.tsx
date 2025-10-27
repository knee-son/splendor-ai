import { useEffect } from "react";

interface Props {
  onPrev: () => void;
  onNext: () => void;
  addVertical?: boolean;
}

export function CardNavigator({ onPrev, onNext, addVertical }: Props) {
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "ArrowLeft") onPrev();
      if (e.key === "ArrowRight") onNext();
      if (e.key === "ArrowUp" && addVertical) onPrev();
      if (e.key === "ArrowDown" && addVertical) onNext();
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [onPrev, onNext]);

  return null;
}
