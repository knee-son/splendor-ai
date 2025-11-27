import React, { useEffect, useState } from "react";

export default function ModelTrainingPage() {
  const backend_url = import.meta.env.VITE_HTTP_URL;
  const websocket_url = import.meta.env.VITE_WEBSOCKET_URL;

  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [actions, setActions] = useState<string[]>([]);

  async function sendCommand(action: string) {
    await fetch(`${backend_url}/train?cmd=${action}`, {
      method: "POST",
    });
  }

  useEffect(() => {
    fetch(`${backend_url}/isitplaying`)
      .then((res) => res.json())
      .then((data) => setIsPlaying(data.state));

    const training_url = import.meta.env.VITE_WEBSOCKET_URL + "/train";
    const ws = new WebSocket(training_url);

    ws.onmessage = (event) => {
      console.log(event.data);
      setActions((prev) => [...prev, event.data]);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="flex h-screen w-full justify-center">
      <div className="flex items-center">
        <h2>{actions.join(", ")}</h2>
      </div>
      <footer className="absolute bottom-4 flex gap-3 p-3 bg-gray-900 rounded-lg shadow">
        <button
          className="flex px-3 py-1 bg-gray-700 text-white rounded-l hover:bg-gray-600"
          // onClick={prev}
        >
          <span className="material-symbols-outlined">skip_previous</span>
        </button>

        <button
          className={`flex px-4 py-1 ${
            isPlaying ? "bg-sky-800" : "bg-sky-600"
          } text-white ${isPlaying ? "hover:bg-sky-600" : "hover:bg-sky-400"}`}
          onClick={() => {
            sendCommand(isPlaying ? "pause" : "play");
            setIsPlaying((p) => !p);
          }}
        >
          <span className="material-symbols-outlined">
            {isPlaying ? "pause" : "play_arrow"}
          </span>
        </button>

        <button
          className="flex px-3 py-1 bg-gray-700 text-white rounded-r hover:bg-gray-600"
          // onClick={next}
        >
          <span className="material-symbols-outlined">skip_next</span>
        </button>
      </footer>
    </div>
  );
}
