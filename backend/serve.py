from flask import Flask, jsonify
from flask_cors import CORS

import json

from scripts.path_manager import METADATA_DIR

cards_dir = METADATA_DIR / "cards.json"
nobles_dir = METADATA_DIR / "nobles.json"

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route("/cards")
def get_cards():
    with open(cards_dir) as f:
        return jsonify(json.load(f))

@app.route("/nobles")
def get_nobles():
    with open(nobles_dir) as f:
        return jsonify(json.load(f))

app.run(debug=True)
