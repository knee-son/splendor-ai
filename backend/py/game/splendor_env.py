import json

import gymnasium as gym
import numpy as np
from core.path_manager import METADATA_DIR
from gymnasium import spaces

with open(METADATA_DIR / "cards.json", "r") as f:
    cards = json.load(f)

with open(METADATA_DIR / "nobles.json", "r") as f:
    nobles = json.load(f)


class SplendorEnv(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    GEM_TYPES = ["diamond", "sapphire", "emerald", "ruby", "onyx"]

    MAX_GEM = 7
    MAX_GOLD = 5
    NUMBER_OF_PLAYERS = 4

    def __init__(self, render_mode=None):
        super().__init__()
        self.player_state_shape = (self.NUMBER_OF_PLAYERS, len(self.GEM_TYPES) + 1)
        self.bank_shape = (len(self.GEM_TYPES),)
        self.action_space = spaces.Discrete(100)

        obs_shape = (self.NUMBER_OF_PLAYERS + 1, len(self.GEM_TYPES) + 1)

        self.action_space = spaces.Discrete(
            10
        )  # placeholder (take gems, buy card, etc.)

        observation = {
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
        }

        self.observation_space = spaces.Box(
            low=0,
            high=20,
            shape=obs_shape,
            dtype=np.int32,
        )

        self.state = np.zeros((10, 10), dtype=np.int8)
        self.current_player = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state[:] = 0
        self.current_player = 0
        return self.state, {}

    def step(self, action):
        # Apply action
        reward = 0
        terminated = False
        truncated = False

        # Update turn
        self.current_player = (self.current_player + 1) % self.NUMBER_OF_PLAYERS

        return self.state

    def render(self):
        print(self.state)
