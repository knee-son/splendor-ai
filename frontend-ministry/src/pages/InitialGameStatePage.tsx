import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import NobleCard from '@/components/NobleCard';
import EngineCard from '@/components/NobleCard';

export default function InitialGameStatePage() {
  const navigate = useNavigate();

  const [nobles, setNobles] = useState<any[]>([]);
  const [cards, setCards] = useState<any[]>([]);

  useEffect(() => {
    const cards_url = import.meta.env.VITE_CARDS_URL;
    const nobles_url = import.meta.env.VITE_NOBLES_URL;

    fetch(cards_url)
      .then(res => res.json())
      .then(data => setCards(data));

    fetch(nobles_url)
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
    <button
      onClick={() => {}}
      className="flex items-center p-3 bg-gray-500 text-white rounded-md absolute top-5 right-5 hover:bg-gray-600"
    >
      <span className="material-symbols-outlined mr-3">casino</span>
      Reshuffle Board
    </button>

  </div>
  );
}
