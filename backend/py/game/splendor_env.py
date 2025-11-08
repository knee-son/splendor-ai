import json
import re
from itertools import combinations

import numpy as np
from core.path_manager import METADATA_DIR
from gymnasium import Env, spaces
from gymnasium.utils import seeding

with open(METADATA_DIR / "cards.json", "r") as f:
    CARDS = json.load(f)
with open(METADATA_DIR / "nobles.json", "r") as f:
    NOBLES = json.load(f)


class SplendorEnv(Env):
    metadata = {"render_modes": ["ansi"]}

    # declaring as set seems to generate this in no particular order
    GEM_TYPES = sorted(set([card["engine"] for card in CARDS]))
    GEMS = len(GEM_TYPES)
    TRIPS_COMB = list(combinations(GEM_TYPES, 3))
    NUM_PLAYERS = 4
    NUM_TIERS = 3
    CARDS_PER_TIER = 4
    NUM_NOBLES = 5

    MAX_CARD_COST = max([engine for card in CARDS for engine in card["cost"].values()])
    MAX_NOBLE_COST = max(
        [engine for noble in NOBLES for engine in noble["cost"].values()]
    )

    def __init__(self, render_mode=metadata["render_modes"][0]):
        super().__init__()

        NUM_CARDS = self.NUM_TIERS * self.CARDS_PER_TIER
        GEMS = len(self.GEM_TYPES)
        OPPONENTS = self.NUM_PLAYERS - 1

        MAX_CARD_PRESTIGE = max([card["prestige"] for card in CARDS])

        # "why not use spaces.Discrete instead of Box?"
        # because NNs don't expect integers as input,
        # so they typically enforce one-hot encoding anyway.
        # my source is i chatgpt'd it the fuck up
        self.observation_space = spaces.Dict(
            {
                "player_throughput": spaces.Box(
                    low=0, high=10, shape=(GEMS,), dtype=np.int32
                ),
                "player_gem_coins": spaces.Box(
                    low=0, high=7, shape=(GEMS,), dtype=np.int32
                ),
                "player_gold_coins": spaces.Box(
                    low=0, high=5, shape=(1,), dtype=np.int32
                ),
                "player_reserves": spaces.Box(
                    low=0, high=3, shape=(1,), dtype=np.int32
                ),
                "player_prestige": spaces.Box(
                    low=0, high=25, shape=(1,), dtype=np.int32
                ),
                "opponents_throughput": spaces.Box(
                    low=0, high=10, shape=(OPPONENTS, GEMS), dtype=np.int32
                ),
                "opponents_gem_coins": spaces.Box(
                    low=0, high=7, shape=(OPPONENTS, GEMS), dtype=np.int32
                ),
                "opponents_gold_coins": spaces.Box(
                    low=0, high=5, shape=(OPPONENTS,), dtype=np.int32
                ),
                "opponents_reserves": spaces.Box(
                    low=0, high=3, shape=(OPPONENTS,), dtype=np.int32
                ),
                "opponents_prestige": spaces.Box(
                    low=0, high=25, shape=(OPPONENTS,), dtype=np.int32
                ),
                "shop_throughput": spaces.Box(
                    low=0, high=GEMS - 1, shape=(NUM_CARDS,), dtype=np.int32
                ),
                "shop_cost": spaces.Box(
                    low=0,
                    high=self.MAX_CARD_COST,
                    shape=(NUM_CARDS, GEMS),
                    dtype=np.int32,
                ),
                "shop_prestige": spaces.Box(
                    low=0, high=MAX_CARD_PRESTIGE, shape=(NUM_CARDS,), dtype=np.int32
                ),
                "nobles_cost": spaces.Box(
                    low=0,
                    high=self.MAX_NOBLE_COST,
                    shape=(self.NUM_NOBLES, GEMS),
                    dtype=np.int32,
                ),
                "bank_gems": spaces.Box(low=0, high=7, shape=(GEMS,), dtype=np.int32),
                "bank_gold": spaces.Box(low=0, high=5, shape=(1,), dtype=np.int32),
            }
        )

        # all actions are discrete
        self.action_space = spaces.Discrete(
            1  # get_gold
            + len(self.GEM_TYPES)  # get gem pair
            + len(self.TRIPS_COMB)  # get three gems
            # actions for getting cards. 3 rows, 4 columns times
            # buy card | reserve | reserve with gold
            + self.NUM_TIERS * self.CARDS_PER_TIER * 3
            + 1  # pass a turn :)
        )

        self.render_mode = render_mode

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.np_random, _ = seeding.np_random(seed)

        self.cards = CARDS.copy()
        self.np_random.shuffle(self.cards)

        self.nobles = NOBLES.copy()
        self.np_random.shuffle(self.nobles)

        self.state = self._get_initial_state()

        # populate cards for each row, then move top cards
        for i in range(self.NUM_TIERS):
            key = f"t{i+1}"
            self.state["cards"][key]["pile"] = [
                card for card in self.cards if card["tier"] == i + 1
            ]
            for _ in range(self.CARDS_PER_TIER):
                self._mill_card(key)

        observation = self._get_observation()

        # make sure observation_space shape aligns with our observations
        assert self.observation_space.contains(observation)

        return observation

    def step(self, action):
        reward = 0
        done = False

        if (
            self.observation["prestige"] >= 15 or self.last_chance != 0
        ) and self.last_chance < self.NUM_PLAYERS:
            self.last_chance += 1
        else:
            done = True

        self.state["current_player"] = (
            self.state["current_player"] + 1
        ) % self.NUM_PLAYERS

        observation = self._get_observation()

        return observation, reward, done

    def _mill_card(self, key):
        top_card = self.state["cards"][key]["pile"].pop()
        self.state["cards"][key]["revealed"].append(top_card)

    def _get_initial_state(self):
        state = {
            "current_player": 0,
            # sets to True if one player manages to get 15 prestige
            "last_chance": False,
            "players": [
                {
                    "coins": {**{gem: 0 for gem in self.GEM_TYPES}, "gold": 0},
                    "income": {gem: 0 for gem in self.GEM_TYPES},
                    "cards": [],
                    "reserves": [],
                    "nobles": [],
                    "prestige": 0,
                }
                for _ in range(self.NUM_PLAYERS)
            ],
            "nobles": self.nobles[: self.NUM_NOBLES],
            "cards": {
                "t3": {"pile": [], "revealed": []},
                "t2": {"pile": [], "revealed": []},
                "t1": {"pile": [], "revealed": []},
            },
            "bank": {**{gem: 7 for gem in self.GEM_TYPES}, "gold": 5},
        }

        return state

    def _get_observation(self):
        state = self.state
        GEM_TYPES = self.GEM_TYPES

        player_num = state["current_player"]

        player = state["players"][player_num]
        opponents = state["players"].copy()
        opponents.remove(player)

        bank = state["bank"]

        shop = [card for tier in state["cards"].values() for card in tier["revealed"]]

        observation = {
            "player_throughput": np.array(
                [player["income"][g] for g in GEM_TYPES], dtype=np.int32
            ),
            "player_gem_coins": np.array(
                [player["coins"][g] for g in GEM_TYPES], dtype=np.int32
            ),
            "player_gold_coins": np.array([player["coins"]["gold"]], dtype=np.int32),
            "player_reserves": np.array([len(player["reserves"])], dtype=np.int32),
            "player_prestige": np.array([player["prestige"]], dtype=np.int32),
            "opponents_throughput": np.array(
                [[p["income"][g] for g in GEM_TYPES] for p in opponents],
                dtype=np.int32,
            ),
            "opponents_gem_coins": np.array(
                [[p["coins"][g] for g in GEM_TYPES] for p in opponents],
                dtype=np.int32,
            ),
            "opponents_gold_coins": np.array(
                [p["coins"]["gold"] for p in opponents], dtype=np.int32
            ),
            "opponents_reserves": np.array(
                [len(p["reserves"]) for p in opponents], dtype=np.int32
            ),
            "opponents_prestige": np.array(
                [p["prestige"] for p in opponents], dtype=np.int32
            ),
            "shop_throughput": np.array(
                [GEM_TYPES.index(card["engine"]) for card in shop], dtype=np.int32
            ),
            "shop_cost": np.array(
                [[card["cost"][gem] for gem in GEM_TYPES] for card in shop],
                dtype=np.int32,
            ),
            "shop_prestige": np.array(
                [card["prestige"] for card in shop], dtype=np.int32
            ),
            "nobles_cost": np.array(
                [
                    [noble["cost"][gem] for gem in self.GEM_TYPES]
                    for noble in self.state["nobles"]
                ],
                dtype=np.int32,
            ),
            "bank_gems": np.array([bank[g] for g in GEM_TYPES], dtype=np.int32),
            "bank_gold": np.array([bank["gold"]], dtype=np.int32),
        }

        return observation

    # TODO: implement this
    # get_human_observation would vary in result given whose perspective it is
    # i.e. player 1, player 2, etc... would have different vision if this is
    # a game with some players' cards faced for themselves only. hence,
    # implement it like this: get_human_observation(self, player: int)
    def get_human_observation(self):
        observation = self.state.copy()

        for key in observation["cards"]:
            tier = observation["cards"][key]
            tier = [card["id"] for card in tier["revealed"]]
            observation["cards"][key] = tier

        observation["nobles"] = [noble["name"] for noble in observation["nobles"]]

        for i in range(len(observation["players"])):
            for card in observation["players"][i]["cards"]:
                observation["players"][i]["cards"] = card["id"]
            for noble in observation["players"][i]["nobles"]:
                observation["players"][i]["nobles"] = noble["name"]

        return observation

    # would be just a formatted ansi without the ansi formatting
    def get_human_ascii(self):
        COLS = 64

        state = self.state

        nobles = "".join(f"|{n['name'].upper():^10}|" for n in state["nobles"])

        w = self.MAX_CARD_COST // 2
        cards = [
            f"[{len(t['pile'])}]  "
            + " ".join(
                f"|{c['id']:<{w}}{('♦'+str(c['prestige'])) if c['prestige'] else '':>{w}}|"
                for c in t["revealed"]
            )
            for t in state["cards"].values()
        ]

        print(self._get_ansi())

        return "\n".join(
            line.center(COLS)
            for line in [
                nobles,
                "",
                *cards,
            ]
        )

    def _get_ansi(self):
        colors = {
            "reset": "\033[0m",
            "diamond": "\033[97m",
            "ruby": "\033[91m",
            "sapphire": "\033[94m",
            "onyx": "\033[90m",
            "emerald": "\033[92m",
        }

        COLS = 64

        state = self.state

        nobles = " ".join(f"|{n['name'].upper():<9}|" for n in state["nobles"])

        costs = [noble["cost"] for noble in state["nobles"]]
        flat_costs = [[{k: v} for k, v in cost.items() if v] for cost in costs]
        max_len = max(len(row) for row in flat_costs)
        padded = [row + [None] * (max_len - len(row)) for row in flat_costs]
        rotated = list(zip(*padded))
        noble_costs = [
            " ".join(
                [
                    (
                        f"|"
                        + colors[list(c)[0]]
                        + f"{list(c.values())[0]} "
                        + f"{'♦'*list(c.values())[0]:<7}"
                        + colors["reset"]
                        + "|"
                        if c
                        else "|" + " " * 9 + "|"
                    )
                    for c in row
                ]
            )
            for row in rotated
        ]

        w = self.MAX_CARD_COST // 2
        cards = [
            f" [{len(t['pile']):>2} left]  "
            + "  ".join(
                f"| {colors[c['engine']]}{c['id']:<{w}}{('◆'+str(c['prestige'])) if c['prestige'] else '':>{w}}{colors['reset']} |"
                for c in t["revealed"]
            )
            for t in state["cards"].values()
        ]

        bank = "Bank:"

        players = [
            "".join(
                [
                    f"{'Player '+str(i+1)+' ('+str(p['prestige'])+')':<16}"
                    for i, p in enumerate(state["players"])
                ]
            )
        ]
        players.append("".join([f"{'cards':<16}"] * self.NUM_PLAYERS))
        players.append("".join([f"{'nobles':<16}"] * self.NUM_PLAYERS))
        players.append("".join([f"{'reserves':<16}"] * self.NUM_PLAYERS))
        players.append("".join([f"{'coins':<16}"] * self.NUM_PLAYERS))

        return "\n".join(
            [
                f"It's currently player {state['current_player']+1}'s turn.",
                "",
                *players,
                "",
                "Nobles:",
                nobles,
                *noble_costs,
                "",
                bank,
                "",
                "Shop:",
                *cards,
            ]
        )

    def render(self):
        print(self._get_ansi())

    def close(self):
        pass
