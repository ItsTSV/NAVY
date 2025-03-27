from collections import deque
import random


# Replay Memory
class ReplayMemory:
    """Memory in which the agent stores info about previous episodes"""
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """Adds relevant info about episode to the memory"""
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """Randomly samples info about previous episodes"""
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
