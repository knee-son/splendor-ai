import json
import random
from collections import deque

from core.path_manager import METADATA_DIR
from flask import Flask, jsonify, request
from flask_cors import CORS

cards_dir = METADATA_DIR / "cards.json"
nobles_dir = METADATA_DIR / "nobles.json"

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


# --------------- Util Functions --------------------
def generate_ascii(engine_shop, nobles):
    WHITESPACE = "-"
    ASCII_LEN = 32

    shop_strings = [
        f'[{len(tier["pile"]):02}]-{WHITESPACE.join([f"{(hash(str(card)) & 0xFF):02X}" for card in tier["field"]])}'
        for tier in engine_shop
    ]
    nobles_string = WHITESPACE.join([n["name"][:2].upper() for n in nobles])

    ascii = "\n".join(
        [
            line.center(ASCII_LEN, WHITESPACE)
            for line in [
                "",
                nobles_string,
                "",
                *shop_strings,
                "",
                "P1:-[]-0D-0E-0R-0S-0O-0G",
                "P2:-[]-0D-0E-0R-0S-0O-0G",
                "P3:-[]-0D-0E-0R-0S-0O-0G",
                "P4:-[]-0D-0E-0R-0S-0O-0G",
                "",
                "Bank:-7D-7E-7R-7S-7O-5G",
                "",
            ]
        ]
    )

    return ascii


def replenish_card(pile: deque, field: deque):
    card = pile.popleft()
    field.appendleft(card)


def purchase_card(player, tier, idx): ...


# --------------- API Endpoints --------------------


@app.route("/cards")
def get_cards():
    with open(cards_dir, "r") as f:
        return jsonify(json.load(f))


@app.route("/nobles")
def get_nobles():
    with open(nobles_dir, "r") as f:
        return jsonify(json.load(f))


@app.route("/initial-state")
def get_initial_state():
    payload = {}

    with open(cards_dir, "r") as f:
        cards = json.load(f)

    with open(nobles_dir, "r") as f:
        nobles = json.load(f)

    random.shuffle(cards)
    random.shuffle(nobles)

    game_nobles = nobles[:5]

    CARDS_PER_ROW = 4

    engine_shop = [
        {
            "pile": deque([card for card in cards if card["tier"] == 1]),
            "field": deque([]),
        },
        {
            "pile": deque([card for card in cards if card["tier"] == 2]),
            "field": deque([]),
        },
        {
            "pile": deque([card for card in cards if card["tier"] == 3]),
            "field": deque([]),
        },
    ]

    for tier in engine_shop:
        while len(tier["field"]) < CARDS_PER_ROW:
            replenish_card(tier["pile"], tier["field"])

    get_ascii = "get-ascii" in request.args
    if get_ascii:
        payload["ascii"] = generate_ascii(engine_shop, game_nobles)

    return jsonify(payload)


app.run(debug=True)
