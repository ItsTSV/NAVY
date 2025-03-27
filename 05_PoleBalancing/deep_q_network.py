from torch import nn
import torch.nn.functional as F


class DQN(nn.Module):
    """(Not so) Deep Q Network for basic Gymnasium environments"""
    def __init__(self, state_size, action_size):
        super().__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, x):
        """Network forward pass

        Args:
            "x: torch.tensor, environment state
        """
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
