import json

from core.path_manager import METADATA_DIR
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from game.splendor_env import SplendorEnv

cards_dir = METADATA_DIR / "cards.json"
nobles_dir = METADATA_DIR / "nobles.json"

game_env = SplendorEnv(render_mode="ansi")
# print(game_env.action_space.sample())

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")
CORS(app, origins=["http://localhost:5173"])


# --------------- API Endpoints --------------------


@app.route("/cards")
def get_cards():
    with open(cards_dir, "r") as f:
        return jsonify(json.load(f))


@app.route("/nobles")
def get_nobles():
    with open(nobles_dir, "r") as f:
        return jsonify(json.load(f))


# this API is for ministry only, as we are exposing the state,
# which includes the hidden cards not yet placed on board
@app.route("/setup")
def setup_board():
    payload = {}

    game_env.reset()
    game_env.render()

    if "get-ascii" in request.args:
        payload["ascii"] = game_env.get_ascii()

    payload["state"] = game_env.state

    return jsonify(payload)


@app.route("/train")
def train_model():
    # Start emitting training steps asynchronously
    socketio.start_background_task(target=mock_training)
    return "Training started!"


def mock_training():
    step = 0
    while step < 100:  # mock 100 steps
        step += 1
        # simulate some computation
        loss = round(1.0 / step, 4)
        accuracy = round(step / 100, 4)
        # send to all connected clients
        socketio.emit(
            "training_step", {"step": step, "loss": loss, "accuracy": accuracy}
        )
        socketio.sleep(0.1)  # 100ms delay


app.run(debug=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
