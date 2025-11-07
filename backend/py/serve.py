import json

from core.path_manager import METADATA_DIR
from flask import Flask, jsonify, request
from flask_cors import CORS
from game.splendor_env import SplendorEnv

cards_dir = METADATA_DIR / "cards.json"
nobles_dir = METADATA_DIR / "nobles.json"

game_env = None
game_env = SplendorEnv()
game_env.render()

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

    game_env = SplendorEnv()

    # TODO: implement get_ascii()
    if "get-ascii" in request.args:
        payload["ascii"] = game_env.get_human_ascii()

    if "get-ansi" in request.args:
        payload["ansi"] = game_env.get_human_ansi()

    payload["state"] = game_env.state

    return jsonify(payload)


app.run(debug=True)
