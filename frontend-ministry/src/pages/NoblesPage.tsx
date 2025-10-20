import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import NobleCard from '@/components/NobleCard';
import CardFooter from '@/components/CardFooter';

export default function CardsPage() {
  const navigate = useNavigate();

  const [nobles, setNobles] = useState<any[]>([]);
  const [cardIndex, setCardIndex] = useState<number>(1);

  useEffect(() => {
    const nobles_path = import.meta.env.VITE_NOBLES;

    fetch(nobles_path)
      .then(res => res.json())
      .then(data => setNobles(data));
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
    <h1 className="absolute top-14 text-5xl font-bold">Splendor Nobles 👑</h1>
    <NobleCard nobleInfo={nobles[cardIndex - 1]} />
    <CardFooter cardNumber={cardIndex} setCardNumber={setCardIndex} />
  </div>
  );
}
