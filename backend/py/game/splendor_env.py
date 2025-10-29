import json

import gymnasium as gym
import numpy as np
from core.path_manager import METADATA_DIR
from gymnasium import spaces

with open(METADATA_DIR / "cards.json", "r") as f:
    cards = json.load(f)
with open(METADATA_DIR / "nobles.json", "r") as f:
    nobles = json.load(f)

GEM_TYPES = set([card["engine"] for card in cards])

from itertools import combinations

trips_comb = list(combinations(GEM_TYPES, 3))


class SplendorEnv(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    NUMBER_OF_PLAYERS = 4

    def __init__(self, render_mode=None):
        super().__init__()
        self.player_state_shape = (self.NUMBER_OF_PLAYERS, len(self.GEM_TYPES) + 1)
        self.bank_shape = (len(self.GEM_TYPES),)

        obs_shape = (self.NUMBER_OF_PLAYERS + 1, len(self.GEM_TYPES) + 1)

        observation_dict = {
            "opponents": [
                {
                    "diamond_throughput": 0,  # no limit
                    "sapphire_throughput": 0,  # no limit
                    "emerald_throughput": 0,  # no limit
                    "ruby_throughput": 0,  # no limit
                    "onyx_throughput": 0,  # no limit
                    "diamond_tokens": 0,  # until 7
                    "sapphire_tokens": 0,  # until 7
                    "emerald_tokens": 0,  # until 7
                    "ruby_tokens": 0,  # until 7
                    "onyx_tokens": 0,  # until 7
                    "gold_tokens": 0,  # until 5
                    "reserves": 0,  # until 3
                    "prestige": 0,
                },
                ...,  # three opponents total
            ],
            "shop": [
                {
                    "diamond_throughput": 0,
                    "sapphire_throughput": 0,
                    "emerald_throughput": 0,
                    "ruby_throughput": 0,
                    "onyx_throughput": 0,
                    "diamond_cost": 0,
                    "sapphire_cost": 0,
                    "emerald_cost": 0,
                    "ruby_cost": 0,
                    "onyx_cost": 0,
                    "prestige": 0,
                },
                ...,  # up to 12 cards to purchase from
            ],
            "nobles": [
                {
                    "diamond_cost": 0,
                    "sapphire_cost": 0,
                    "emerald_cost": 0,
                    "ruby_cost": 0,
                    "onyx_cost": 0,
                    "prestige": 0,
                },
                ...,  # 4 nobles total
            ],
            "bank": {
                "diamond": 7,
                "sapphire": 7,
                "emerald": 7,
                "ruby": 7,
                "onyx": 7,
                "gold": 5,
            },
        }

        self.observation_space = spaces.Box(
            low=0,
            high=20,
            shape=obs_shape,
            dtype=np.int32,
        )

        self.action_space = spaces.Discrete(
            {
                1  # get_gold
                + len(GEM_TYPES)  # get gem pair
                + len(trips_comb)  # get three gems
                + len(cards) * 3  # buy card | reserve | reserve with gold
            }
        )

        self.render_mode = render_mode
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state[:] = 0
        self.current_player = 0
        self.last_chance = 0
        return self.state, {}

    def step(self, action):
        reward = 0
        done = False
        observation = np.array([self.position], dtype=np.int32)
        # info = {'something': 'something something'}

        if (
            self.observation["prestige"] >= 15 or self.last_chance != 0
        ) and self.last_chance < self.NUMBER_OF_PLAYERS:
            self.last_chance += 1
        else:
            done = True

        self.current_player = (self.current_player + 1) % self.NUMBER_OF_PLAYERS

        return observation, reward, done

    def get_ansi(self):
        state = self.state

    def render(self):
        print(self.get_ansi())

    def close(self):
        pass
