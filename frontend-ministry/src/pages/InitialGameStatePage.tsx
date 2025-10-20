import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import type { Card, Noble } from '@/types/splendor';
import NobleCard from '@/components/NobleCard';
import EngineCard from '@/components/NobleCard';

export default function InitialGameStatePage() {
  const navigate = useNavigate();

  const cards_url = import.meta.env.VITE_CARDS_URL;
  const nobles_url = import.meta.env.VITE_NOBLES_URL;
  const init_url = import.meta.env.VITE_INIT_URL;

  const [nobles, setNobles] = useState<Noble[]>([]);
  const [cards, setCards] = useState<Card[]>([]);
  const [gameState, setGameState] = useState<string>('Loading board...');

  function fetchInitialState() {
    fetch(`${init_url}?get-ascii`)
      .then(res => res.json())
      .then(data => setGameState(data.ascii));
  }

  useEffect(() => {
    fetch(cards_url)
      .then(res => res.json())
      .then(data => setCards(data));

    fetch(nobles_url)
      .then(res => res.json())
      .then(data => setNobles(data));

    fetchInitialState();
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
      onClick={fetchInitialState}
      className="flex items-center p-3 bg-gray-500 text-white rounded-md absolute top-5 right-5 hover:bg-gray-600"
    >
      <span className="material-symbols-outlined mr-3">casino</span>
      Reshuffle Board
    </button>

    <div
      className="bg-[#f5deb3] text-gray-800 font-mono w-6/12 aspect-square flex items-center justify-center p-8 rounded-lg shadow-md max-w-xl text-center border border-amber-700"
      style={{ whiteSpace: 'pre-wrap' }}
    >
      {gameState}
    </div>

  </div>
  );
}
