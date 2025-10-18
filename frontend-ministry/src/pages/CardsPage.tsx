import { useEffect, useState } from 'react';
import EngineCard from '../components/EngineCard';
import CardFooter from '../components/CardFooter';

// import cards from '../../../metadata/cards.json';
// import nobles from '../../../metadata/nobles.json';

export default function CardsPage() {
  const [cards, setCards] = useState<any[]>([]);
  const [nobles, setNobles] = useState<any[]>([]);

  const [cardNumber, setCardNumber] = useState<number>(1);

  useEffect(() => {
    const cards_path = import.meta.env.VITE_CARDS;
    const nobles_path = import.meta.env.VITE_NOBLES;

    fetch(cards_path)
      .then(res => res.json())
      .then(setCards);

    fetch(nobles_path)
      .then(res => res.json())
      .then(setNobles);

    console.log(`Cards path at: ${cards_path} and nobles at: ${nobles_path}`);
    console.log(`Loaded ${cards.length} cards and ${nobles.length} nobles.`);


    console.log(cards, nobles);
  }, []);

  return (
    <div className="flex flex-col h-screen justify-between items-center p-6 bg-gray-100">
      <EngineCard cardNumber={cardNumber}/>

      <CardFooter cardNumber={cardNumber} setCardNumber={setCardNumber} />
    </div>
  );
}
