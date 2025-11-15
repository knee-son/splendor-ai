import json

from core.path_manager import METADATA_DIR
from flask import Flask, jsonify, request
from flask_cors import CORS
from game.splendor_env import SplendorEnv

cards_dir = METADATA_DIR / "cards.json"
nobles_dir = METADATA_DIR / "nobles.json"

game_env = SplendorEnv(render_mode="ansi")

app = Flask(__name__)
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


@app.route("/setup")
def setup_board():
    payload = {}

    game_env.reset()
    game_env.render()

    if "get-ascii" in request.args:
        payload["ascii"] = game_env.get_ascii()

    payload["state"] = game_env.state

    return jsonify(payload)


app.run(debug=True)
