import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EngineCard from '@/components/EngineCard';
import CardFooter from '@/components/CardFooter';
import CardPageScrollbar from '@/components/CardPageScrollbar';

export default function CardsPage() {
  const navigate = useNavigate();

  const [cards, setCards] = useState<any[]>([]);
  const [cardIndex, setCardIndex] = useState<number>(1);

  useEffect(() => {
    const cards_path = import.meta.env.VITE_CARDS;

    fetch(cards_path)
      .then(res => res.json())
      .then(data => setCards(data));
  }, []);

  return (
  <div className="flex h-screen bg-gray-100  flex-col justify-center items-center p-6">
    <button
      onClick={() => navigate('/')}
      className="flex items-center p-3 bg-blue-500 text-white rounded-md absolute top-5 left-5 hover:bg-blue-600"
    >
      <span className="material-symbols-outlined">arrow_back</span>
      Back to Menu
    </button>
    <h1 className="absolute top-14 text-5xl font-bold">Splendor Cards 🃏</h1>
    <EngineCard cardInfo={cards[cardIndex - 1]} />
    <CardFooter cardNumber={cardIndex} setCardNumber={setCardIndex} />
    <CardPageScrollbar cards={cards} cardNumber={cardIndex} setCardNumber={setCardIndex}/>
  </div>
  );
}
