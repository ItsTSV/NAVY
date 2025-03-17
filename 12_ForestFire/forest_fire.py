import numpy as np
import matplotlib.pyplot as plt


class ForestFire:
    """Class that represents forest fire simulation board and its logic

    Attributes:
        board_size (int): size of the board
        density (float): initial density of trees in the board
        regrowth_probability (float): probability of tree regrowth
        ignition_probability (float): probability of tree self igniting
        board (numpy.ndarray): 2D array representing the board
    """

    def __init__(self, board_size, density, regrowth_probability, ignition_probability):
        """Init Forest fire parameters and prepare the board"""
        self.board_size = board_size
        self.density = density
        self.regrowth_probability = regrowth_probability
        self.ignition_probability = ignition_probability

        self.board = np.zeros((board_size, board_size))
        self.tmp_board = np.zeros((board_size, board_size))
        self.initialize_board()
        plt.ion()

    def initialize_board(self):
        """Initialize the board with trees and fire"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if np.random.rand() < self.density:
                    self.board[i, j] = 1

    def update_board(self):
        """Create tmp board and update the board based on forest fire rules

        0 -- Empty, no tree here
        1 -- Living tree
        2 -- Burning tree"""
        self.tmp_board = self.board.copy()

        for i in range(self.board_size):
            for j in range(self.board_size):
                # Regrowth rule -- if the index is dirt, the tree can regrow
                if self.board[i, j] == 0:
                    if np.random.rand() < self.regrowth_probability:
                        self.tmp_board[i, j] = 1
                # Fire spread rule, self ignition rule -- if the index is tree, it might burn
                elif self.board[i, j] == 1:
                    if i > 0 and self.board[i - 1, j] == 2:
                        self.tmp_board[i, j] = 2
                    elif i < self.board_size - 1 and self.board[i + 1, j] == 2:
                        self.tmp_board[i, j] = 2
                    elif j > 0 and self.board[i, j - 1] == 2:
                        self.tmp_board[i, j] = 2
                    elif j < self.board_size - 1 and self.board[i, j + 1] == 2:
                        self.tmp_board[i, j] = 2
                    else:
                        if np.random.rand() < self.ignition_probability:
                            self.tmp_board[i, j] = 2
                # Fire extinguish rule -- if the index is burning, it will become dirt
                elif self.board[i, j] == 2:
                    self.tmp_board[i, j] = 0

        self.board = self.tmp_board.copy()

    def render_board(self):
        """Copy board, convert colors and display it in matplotlib"""
        colors = {
            0: (40, 20, 40),
            1: (0, 125, 0),
            2: (255, 125, 0),
        }

        height, width = self.board.shape
        rgb_board = np.zeros((height, width, 3), dtype=np.uint8)

        for key, color in colors.items():
            rgb_board[self.board == key] = color

        # Display the board; if it already exists, refresh
        plt.figure(0)
        plt.imshow(rgb_board)
        plt.axis("off")
        plt.show()
        plt.pause(0.25)

    def run_forest_fire(self):
        """Run the forest fire loop"""
        while True:
            self.render_board()
            self.update_board()
