import json
from itertools import combinations

import numpy as np
from core.path_manager import METADATA_DIR
from gymnasium import Env, spaces
from gymnasium.utils import seeding

with open(METADATA_DIR / "cards.json", "r") as f:
    cards = json.load(f)
with open(METADATA_DIR / "nobles.json", "r") as f:
    nobles = json.load(f)


class SplendorEnv(Env):
    metadata = {"render_modes": ["ansi"]}

    # declaring as set seems to generate this in no particular order
    GEM_TYPES = sorted(set([card["engine"] for card in cards]))
    GEMS = len(GEM_TYPES)
    TRIPS_COMB = list(combinations(GEM_TYPES, 3))
    NUM_PLAYERS = 4
    NUM_TIERS = 3
    CARDS_PER_TIER = 4
    NOBLES = 5

    def __init__(self, render_mode=metadata["render_modes"][0]):
        super().__init__()

        CARDS = self.NUM_TIERS * self.CARDS_PER_TIER
        GEMS = len(self.GEM_TYPES)
        OPPONENTS = self.NUM_PLAYERS - 1

        MAX_CARD_PRESTIGE = max([card["prestige"] for card in cards])
        MAX_CARD_COST = max(
            [engine for card in cards for engine in card["cost"].values()]
        )
        MAX_NOBLE_COST = max(
            [engine for noble in nobles for engine in noble["cost"].values()]
        )

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
                    low=0, high=GEMS - 1, shape=(CARDS,), dtype=np.int32
                ),
                "shop_cost": spaces.Box(
                    low=0, high=MAX_CARD_COST, shape=(CARDS, GEMS), dtype=np.int32
                ),
                "shop_prestige": spaces.Box(
                    low=0, high=MAX_CARD_PRESTIGE, shape=(CARDS,), dtype=np.int32
                ),
                "nobles_cost": spaces.Box(
                    low=0,
                    high=MAX_NOBLE_COST,
                    shape=(self.NOBLES, GEMS),
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

        self.cards = cards.copy()
        self.np_random.shuffle(self.cards)

        self.nobles = nobles.copy()
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
        # assert self.observation_space.contains(observation)

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
            "nobles": self.nobles[: self.NOBLES],
            "cards": {
                "t3": {"pile": [], "revealed": []},
                "t2": {"pile": [], "revealed": []},
                "t1": {"pile": [], "revealed": []},
            },
            "bank": {**{gem: 7 for gem in self.GEM_TYPES}, "gold": 5},
        }

        return state

    # TODO: implement this
    def get_human_observable(self): ...

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

    def get_ansi(self):
        RESET = "\033[0m"
        DIAMOND = "\033[97m"
        RUBY = "\033[91m"
        SAPPHIRE = "\033[94m"
        ONYX = "\033[90m"
        EMERALD = "\033[92m"

        text = f"{DIAMOND}♦ Diamond{RESET}\n"
        f"{RUBY}♦ Ruby{RESET}\n"
        f"{SAPPHIRE}♦ Sapphire{RESET}\n"
        f"{ONYX}♦ Onyx{RESET}\n"
        f"{EMERALD}♦ Emerald{RESET}\n"

        state = self.state

        return text

    def render(self):
        print(self.get_ansi())

    def close(self):
        pass
