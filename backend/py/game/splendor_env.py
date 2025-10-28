import gymnasium as gym
import numpy as np
from gymnasium import spaces


class SplendorEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None):
        super().__init__()
        self.action_space = spaces.Discrete(100)  # e.g. 100 possible moves
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(10, 10), dtype=np.int8
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
        self.current_player = 1 - self.current_player

        return self.state, reward, terminated, truncated, {}

    def render(self):
        print(self.state)
