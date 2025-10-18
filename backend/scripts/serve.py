from flask import Flask, jsonify
import json, os

app = Flask(__name__)

@app.route("/metadata/cards")
def get_cards():
    with open("../metadata/cards.json") as f:
        return jsonify(json.load(f))

@app.route("/metadata/nobles")
def get_nobles():
    with open("../metadata/nobles.json") as f:
        return jsonify(json.load(f))

app.run(debug=True)
