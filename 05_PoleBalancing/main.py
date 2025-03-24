import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from collections import deque
import random

# Hyperparameters
BATCH_SIZE = 64
GAMMA = 0.99
EPS_START = 1.0
EPS_END = 0.01
EPS_DECAY = 0.995
TARGET_UPDATE = 10
MEMORY_SIZE = 100000
LEARNING_RATE = 0.0001
NUM_EPISODES = 200


# Neural Network for Q-function approximation
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


# Replay Memory
class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


# Environment setup
env = gym.make("CartPole-v1")
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# Initialize networks
policy_net = DQN(state_size, action_size)
target_net = DQN(state_size, action_size)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LEARNING_RATE)
memory = ReplayMemory(MEMORY_SIZE)


# Epsilon-greedy action selection
def epsilon_greedy_action(state, eps):
    if random.random() > eps:
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[random.randrange(action_size)]], dtype=torch.long)


# Training function
def advance():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = list(zip(*transitions))

    # Reshape states and next_states to ensure they are 2D tensors
    state_batch = torch.cat([s.reshape(1, -1) for s in batch[0]])
    action_batch = torch.cat(batch[1])
    reward_batch = torch.cat(batch[2])
    next_state_batch = torch.cat([s.reshape(1, -1) for s in batch[3]])
    done_batch = torch.cat(batch[4])

    # Compute Q(s_t, a)
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states
    next_state_values = target_net(next_state_batch).max(1)[0].detach()
    expected_state_action_values = (next_state_values * GAMMA) * (1 - done_batch) + reward_batch

    # Compute loss
    loss = F.mse_loss(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()

    # Gradient clipping to stabilize training
    torch.nn.utils.clip_grad_norm_(policy_net.parameters(), max_norm=1.0)
    optimizer.step()


# Training loop
eps = EPS_START
for episode in range(NUM_EPISODES):
    state, _ = env.reset()
    state = torch.tensor([state], dtype=torch.float32)
    total_reward = 0

    for t in range(200):
        action = epsilon_greedy_action(state, eps)
        next_state, reward, done, _, _ = env.step(action.item())
        total_reward += reward

        next_state = torch.tensor([next_state], dtype=torch.float32)
        reward = torch.tensor([reward], dtype=torch.float32)
        done = torch.tensor([done], dtype=torch.float32)

        memory.push(state, action, reward, next_state, done)
        state = next_state

        advance()

        if done:
            break

    # Decay epsilon
    if eps > EPS_END:
        eps *= EPS_DECAY

    # Update target network
    if episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

    print(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {eps:.2f}")

print("Training complete.")
env.close()

# Preview model
env = gym.make("CartPole-v1", render_mode="human")
state, _ = env.reset()
state = torch.tensor([state], dtype=torch.float32)
while True:
    env.render()
    action = policy_net(state).max(1)[1].view(1, 1)
    next_state, _, done, _, _ = env.step(action.item())
    state = torch.tensor([next_state], dtype=torch.float32)
    if done:
        break

# Save model
torch.save(policy_net.state_dict(), "cartpole.pth")