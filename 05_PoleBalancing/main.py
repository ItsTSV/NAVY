import gymnasium as gym
import torch
from dqn_agent import DQNAgent


# Environment setup
env = gym.make("CartPole-v1")
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# DQN Agent
agent = DQNAgent(action_size, state_size, env)
agent.train()

# Preview model
env = gym.make("CartPole-v1", render_mode="human")
agent.policy_net.load_state_dict(torch.load("trained_cartpole.pth"))
total_reward = 0

state, _ = env.reset()
state = torch.tensor([state], dtype=torch.float32)
while True:
    env.render()
    action = agent.policy_net(state).max(1)[1].view(1, 1)
    next_state, reward, done, _, _ = env.step(action.item())
    total_reward += reward
    state = torch.tensor([next_state], dtype=torch.float32)
    if done:
        print(f"Total reward: {total_reward}")
        break
