import asyncio
import json
from pathlib import Path

from core.path_manager import METADATA_DIR
from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from game.splendor_env import SplendorEnv

cards_dir = METADATA_DIR / "cards.json"
nobles_dir = METADATA_DIR / "nobles.json"

game_env = SplendorEnv(render_mode="ansi")

app = FastAPI()

# CORS
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- API Endpoints --------------------


@app.get("/cards")
async def get_cards():
    with open(cards_dir, "r") as f:
        return JSONResponse(json.load(f))


@app.get("/nobles")
async def get_nobles():
    with open(nobles_dir, "r") as f:
        return JSONResponse(json.load(f))


@app.get("/setup")
async def setup_board(get_ascii: bool = Query(False, alias="get-ascii")):
    payload = {}

    game_env.reset()
    game_env.render()

    if get_ascii:
        payload["ascii"] = game_env.get_ascii()

    payload["state"] = game_env.state

    return JSONResponse(payload)


# ---------------- WebSocket Training --------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/train")
async def websocket_train(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        step = 0
        while step < 100:  # mock 100 steps
            step += 1
            loss = round(1.0 / step, 4)
            accuracy = round(step / 100, 4)
            await manager.broadcast({"step": step, "loss": loss, "accuracy": accuracy})
            await asyncio.sleep(0.1)  # 100ms delay
    except WebSocketDisconnect:
        manager.disconnect(websocket)
