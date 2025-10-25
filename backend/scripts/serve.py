from flask import Flask, request, jsonify
from flask_cors import CORS

import json

from path_manager import METADATA_DIR

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

@app.route("/initial-state")
def get_initial_state():
    payload = {}

    get_ascii = "get-ascii" in request.args
    if get_ascii:
        ascii = (
            '--------------------------------\n'
            '---------N0-N1-N2-N3-N4---------\n'
            '--------------------------------\n'
            '--------[16]-09-10-11-12--------\n'
            '--------[26]-04-05-06-07--------\n'
            '--------[36]-00-01-02-03--------\n'
            '--------------------------------\n'
            '----P1:-[]-0D-0E-0R-0S-0O-0G----\n'
            '----P2:-[]-0D-0E-0R-0S-0O-0G----\n'
            '----P3:-[]-0D-0E-0R-0S-0O-0G----\n'
            '----P4:-[]-0D-0E-0R-0S-0O-0G----\n'
            '--------------------------------'
        )
        payload['ascii'] = ascii

    return jsonify(payload)
app.run(debug=True)
