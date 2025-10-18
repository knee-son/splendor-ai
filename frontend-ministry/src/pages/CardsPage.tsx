import { useEffect, useState } from 'react';
import EngineCard from '../components/EngineCard';
import CardFooter from '../components/CardFooter';

// import cards from '../../../metadata/cards.json';
// import nobles from '../../../metadata/nobles.json';

export default function CardsPage() {
  const [cards, setCards] = useState<any[]>([]);
  const [nobles, setNobles] = useState<any[]>([]);

  const [cardIndex, setCardIndex] = useState<number>(1);

  useEffect(() => {
    const cards_path = import.meta.env.VITE_CARDS;
    const nobles_path = import.meta.env.VITE_NOBLES;

    fetch(cards_path)
      .then(res => res.json())
      .then(data => setCards(data));

    fetch(nobles_path)
      .then(res => res.json())
      .then(data => setNobles(data));
  }, []);

  return (
    <div className="flex flex-col h-screen justify-between items-center p-6 bg-gray-100">
      <EngineCard cardInfo={cards[cardIndex]} />
      <CardFooter cardNumber={cardIndex} setCardNumber={setCardIndex} />
    </div>
  );
}
