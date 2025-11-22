import React, { useEffect, useState } from "react";

export default function ModelTrainingPage() {
  const [actions, setActions] = useState<string[]>([]);

  useEffect(() => {
    // initialize websocket
    const socket = new WebSocket("ws://localhost:5000/train");

    socket.onopen = () => {
      console.log("WS connected");
    };

    socket.onmessage = (event) => {
      // event.data is the backend text/json message
      console.log("WS message:", event.data);

      setActions((prev) => [...prev, event.data]);
    };

    socket.onclose = () => {
      console.log("WS closed");
    };

    socket.onerror = (err) => {
      console.error("WS error:", err);
    };

    // cleanup on unmount
    return () => socket.close();
  }, []);

  return (
    <div>
      <h2>{actions.join(", ")}</h2>
    </div>
  );
}
