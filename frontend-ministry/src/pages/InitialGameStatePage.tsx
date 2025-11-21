/**
 * InitialGameStatePage
 *
 * A v1 of what the UI for the Splendor game looks like.
 *
 * @page
 */

import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";

import SplendorBoard from "@/components/SplendorBoard";

import type { State } from "@/types/splendor";

export default function InitialGameStatePage() {
  const navigate = useNavigate();

  const init_url = import.meta.env.VITE_INIT_URL;

  const [gameState, setGameState] = useState<State | null>(null);
  const [isFetching, setIsFetching] = useState<boolean>(true);

  async function fetchInitialState() {
    setIsFetching(true);

    const data = await fetch(init_url).then((res) => res.json());

    setGameState(data.state);

    setIsFetching(false);
  }

  useEffect(() => {
    fetchInitialState();
  }, []);

  return (
    <div className="flex h-screen bg-gray-100  flex-col justify-center items-center p-6">
      <button
        onClick={() => navigate("/")}
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

      <SplendorBoard gameState={gameState} isFetching={isFetching} />
    </div>
  );
}
