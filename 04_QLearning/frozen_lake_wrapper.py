import gymnasium as gym
import numpy as np


class CustomFrozenLakeWrapper(gym.Wrapper):
    """Wrapper that allows me to adjust rewards based on the environment"""

    def __init__(self, env):
        """Initializes the wrapper, store the map of the environment"""
        super().__init__(env)
        self.lake_map = np.array(env.unwrapped.desc, dtype=str)

    def step(self, action):
        """Overrides step method, adds custom reward logic"""
        obs, reward, done, truncated, info = self.env.step(action)

        if done:
            row, col = divmod(obs, self.lake_map.shape[1])
            if self.lake_map[row, col] == "G":
                reward = 1000
            elif self.lake_map[row, col] == "H":
                reward = -250
        else:
            reward = -1

        return obs, reward, done, truncated, info
