import numpy as np


class HopfieldNetwork:
    """Represents Hopfield network, its training and sync/async operations"""
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        """Train using Hebb rule (from slides)"""
        for pattern in patterns:
            pattern = pattern.flatten()
            self.weights += np.outer(pattern, pattern)
        np.fill_diagonal(self.weights, 0)

    def update(self, pattern, mode="asynchronous"):
        """Refresh neurons (bipolar mode)"""
        pattern = pattern.flatten()
        if mode == "asynchronous":
            for i in range(len(pattern)):
                activation = np.dot(self.weights[i], pattern)
                pattern[i] = np.sign(activation)
        else:
            activation = np.dot(self.weights, pattern)
            pattern = np.sign(activation)
        return pattern.reshape((5, 5))

    def recover(self, pattern, iterations=25, mode="asynchronous"):
        """Recovers"""
        for _ in range(iterations):
            pattern = self.update(pattern, mode=mode)
        return pattern
