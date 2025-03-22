import gymnasium as gym
from q_learning_agent import QLearningAgent

# Create environment and agent, train it
env = gym.make("FrozenLake-v1", is_slippery=False)
agent = QLearningAgent(env, 1000, epsilon_decay=0.005)
agent.train()

# Test the agent
agent.epsilon = 0
env = gym.make("FrozenLake-v1", render_mode="rgb_array", is_slippery=False)
state, _ = env.reset()
done = False
while not done:
    action = agent.epsilon_greedy_action(state)
    state, _, done, _, _ = env.step(action)
    env.render()
