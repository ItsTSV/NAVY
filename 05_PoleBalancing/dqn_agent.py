import random
import torch
from torch import optim
import torch.nn.functional as F
from deep_q_network import DQN
from replay_memory import ReplayMemory


class DQNAgent:
    """Q-Learning agent that will be able to learn to play basic Gymnasium games

       Attributes:
           action_size: int, number of actions the agent can perform
           state_size: int, number of states the game can be in
           policy_net: DQN, optimized Deep Q-Network
           target_net: DQN, stable Deep Q-Network
           optimizer: torch.optim, using Adam because it just works
           memory: ReplayMemory, the agent will store previous episode info here
           env: gymnasium.environment, the game itself
           """
    def __init__(self, action_size, state_size, env, memory_size=100000):
        # Environment info
        self.action_size = action_size
        self.state_size = state_size

        # Networks
        # Initialize networks
        self.policy_net = DQN(state_size, action_size)
        self.target_net = DQN(state_size, action_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.0001)

        # Memory
        self.memory = ReplayMemory(memory_size)

        # Environment
        self.env = env

    # epsilon-greedy action selection
    def epsilon_greedy_action(self, state, epsilon):
        """Based on epsilon. selects either random or best action"""
        if random.random() > epsilon:
            with torch.no_grad():
                return self.policy_net(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor(
                [[random.randrange(self.action_size)]], dtype=torch.long
            )

    # Training function
    def advance(self, batch_size=64, gamma=0.99):
        """"Performs one optimization step

            First, a batch is sampled from the memory. The data from is prepared to be fed into the NN.
            When that is done, the network will predict Q-values of current and next states.
            Then, according to equation, a loss between expected and current state values is computed.
        """
        if len(self.memory) < batch_size:
            return
        transitions = self.memory.sample(batch_size)
        batch = list(zip(*transitions))

        # Reshape states and next_states to ensure they are 2D tensors
        state_batch = torch.cat([s.reshape(1, -1) for s in batch[0]])
        action_batch = torch.cat(batch[1])
        reward_batch = torch.cat(batch[2])
        next_state_batch = torch.cat([s.reshape(1, -1) for s in batch[3]])
        done_batch = torch.cat(batch[4])

        # Compute Q(s_t, a)
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states
        next_state_values = self.target_net(next_state_batch).max(1)[0].detach()
        expected_state_action_values = (next_state_values * gamma) * (
            1 - done_batch
        ) + reward_batch

        # Compute loss
        loss = F.mse_loss(
            state_action_values, expected_state_action_values.unsqueeze(1)
        )

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()

        # Gradient clipping to stabilize training
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), max_norm=1.0)
        self.optimizer.step()

    def train(self, episode_count=200, epsilon_end=0.01, epsilon_decay=0.99, update_coeff=10):
        """Trains the agent for selected number of episodes"""
        # Training loop
        epsilon = 1
        for episode in range(episode_count):
            state, _ = self.env.reset()
            state = torch.tensor([state], dtype=torch.float32)
            total_reward = 0

            for _ in range(200):
                action = self.epsilon_greedy_action(state, epsilon)
                next_state, reward, done, _, _ = self.env.step(action.item())
                total_reward += reward

                next_state = torch.tensor([next_state], dtype=torch.float32)
                reward = torch.tensor([reward], dtype=torch.float32)
                done = torch.tensor([done], dtype=torch.float32)

                self.memory.push(state, action, reward, next_state, done)
                state = next_state

                self.advance()

                if done:
                    break

            # Decay epsilon
            if epsilon > epsilon_end:
                epsilon *= epsilon_decay

            # Update target network
            if episode % update_coeff == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())

            print(
                f"Episode {episode}, Total Reward: {total_reward}, epsilon: {epsilon:.2f}"
            )

        print("Training complete.")
        self.env.close()

    def save_model(self):
        """Saves the model weights, so they can be used later"""
        torch.save(self.policy_net.state_dict(), "trained_cartpole.pth")
