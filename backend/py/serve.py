import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path

from core.path_manager import METADATA_DIR
from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from game.splendor_env import SplendorEnv

cards_dir = METADATA_DIR / "cards.json"
nobles_dir = METADATA_DIR / "nobles.json"

game_env = SplendorEnv(render_mode="ansi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(generate_step())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("Background task cancelled cleanly")


app = FastAPI(lifespan=lifespan)

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


@app.get("/isitplaying")
async def is_it_training():
    return JSONResponse({"state": training_state["playing"]})


@app.post("/train")
async def manage_training(
    cmd: str = Query(..., description="play, pause, step_forward, step_backward")
):
    print(cmd)
    if cmd == "play":
        training_state["playing"] = True
        return {"status": "playing"}
    elif cmd == "pause":
        training_state["playing"] = False
        return {"status": "paused"}
    elif cmd == "step_forward":
        training_state["step"] += 1
        return {"status": "stepped_forward", "step": training_state["current_step"]}
    elif cmd == "step_backward":
        training_state["step"] -= 1
        return {"status": "stepped_backward", "step": training_state["current_step"]}
    else:
        return {"error": "invalid action"}


# ---------------- Manager for Multiple Clients --------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def broadcast(self, message: dict):
        print("broadcasting", message)
        assert type(message) is dict
        to_remove = []

        print(self.active_connections)

        for connection in self.active_connections:
            print("sending json", message)
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                to_remove.append(connection)

        for connection in to_remove:
            self.disconnect(connection)

        print("returning from broadcast")


manager = ConnectionManager()

training_state = {"playing": False, "step": 0}


async def generate_step():
    while True:
        if training_state["playing"]:
            if not manager.active_connections:
                training_state["playing"] = False

            training_state["step"] += 1
            data = {
                "step": str(training_state["step"]),
                "action": str(game_env.action_space.sample()),
            }

            asyncio.create_task(manager.broadcast(data))
        await asyncio.sleep(0.5)


@app.websocket("/ws/train")
async def ws_train(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(ws)
