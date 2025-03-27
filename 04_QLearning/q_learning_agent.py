import numpy as np


class QLearningAgent:
    """Class that represents QLearning agent and its operations (step, epsilon based decision...)"""

    def __init__(
        self,
        env,
        max_episodes,
        epsilon_decay=0.005,
        learning_rate=0.1,
        gamma=0.95,
    ):
        """Initialize the agent, its memory and epsilon decay scheme

        Args:
         env: gymnasium environment
         epsilon_decay: how fast will the decision constant fall
         max_episodes: for how long will the agent learn
         learning_rate: how fast will the agent learn (alpha)
         gamma: discount factor for future rewards
        """
        # Setup Q-table (Neural network from Wish.com)
        self.q_table = np.zeros((env.observation_space.n, env.action_space.n))

        # Setup epsilon
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay

        # Episode control
        self.max_episodes = max_episodes

        # Setup learning constants
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.cumulative_reward = 0

        # Setup environment
        self.env = env
        self.action_count = env.action_space.n

    def epsilon_greedy_action(self, state):
        """Choose action from Q-table based on epsilon greedy policy

        Args:
         state: current state of the environment

        Returns:
         action: action to take
        """
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, self.action_count - 1)

        return np.argmax(self.q_table[state])

    def decay_epsilon(self):
        """Linear epsilon decay"""
        self.epsilon = max(self.epsilon_min, self.epsilon * (1 - self.epsilon_decay))

    def train(self):
        """Train the agent to play the game"""
        for episode in range(self.max_episodes):
            state, _ = self.env.reset()
            done = False

            # Reset cumulative reward and step count
            self.cumulative_reward = 0

            while not done:
                action = self.epsilon_greedy_action(state)
                next_state, reward, done, _, _ = self.env.step(action)

                # Update cumulative reward
                self.cumulative_reward += reward

                # Update Q-table
                self.q_table[state, action] = self.q_table[
                    state, action
                ] + self.learning_rate * (
                    reward
                    + self.gamma * np.max(self.q_table[next_state])
                    - self.q_table[state, action]
                )

                # Update state
                state = next_state

            # Update epsilon
            self.decay_epsilon()

            # Print info
            if episode % 100 == 0:
                print(
                    f"Episode {episode} finished with reward {self.cumulative_reward}; epsilon: {self.epsilon}"
                )

        print(f"Training done. Cumulative reward: {self.cumulative_reward}")
