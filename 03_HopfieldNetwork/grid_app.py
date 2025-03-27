import tkinter as tk
import numpy as np
from hopfield_network import HopfieldNetwork


class GridApp:
    """Graphical interface and pattern handling for Hopfield network"""

    def __init__(self, root):
        self.root = root
        self.root.title("Grid Pattern Editor")

        # Main layout
        self.frame_left = tk.Frame(root)
        self.frame_left.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create grid buttons
        self.grid_size = 5
        self.buttons = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = tk.Button(
                    self.frame_left,
                    width=4,
                    height=2,
                    command=lambda r=i, c=j: self.toggle_color(r, c),
                    bg="white",
                )
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        # Control buttons
        self.btn_train = tk.Button(
            self.frame_right, text="Train network", command=self.train_network
        )
        self.btn_train.pack(fill=tk.X, pady=2)

        self.btn_save = tk.Button(
            self.frame_right, text="Save pattern", command=self.save_pattern
        )
        self.btn_save.pack(fill=tk.X, pady=2)

        self.btn_repair = tk.Button(
            self.frame_right, text="Repair pattern", command=self.repair_pattern
        )
        self.btn_repair.pack(fill=tk.X, pady=2)

        self.btn_repair_async = tk.Button(
            self.frame_right,
            text="Repair pattern async",
            command=self.repair_pattern_async,
        )
        self.btn_repair_async.pack(fill=tk.X, pady=2)

        self.btn_show_saved = tk.Button(
            self.frame_right,
            text="Show saved patterns",
            command=self.show_saved_patterns,
        )
        self.btn_show_saved.pack(fill=tk.X, pady=2)

        self.btn_clear = tk.Button(
            self.frame_right, text="Clear grid", command=self.clear_grid
        )
        self.btn_clear.pack(fill=tk.X, pady=2)

        # Storage for patterns
        self.saved_patterns = []
        self.max_saved = 5
        self.current_saved = 0

        # Hopfield network
        self.hopfield_net = HopfieldNetwork(size=self.grid_size * self.grid_size)

    def toggle_color(self, row, col):
        """Left click -- mark or unmark grid cell"""
        btn = self.buttons[row][col]
        current_color = btn.cget("bg")
        new_color = "black" if current_color == "white" else "white"
        btn.config(bg=new_color)

    def extract_pattern(self):
        """Extract pattern from grid to Numpy Array (bipolar representation)"""
        pattern = np.full((self.grid_size, self.grid_size), -1, dtype=int)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.buttons[i][j].cget("bg") == "black":
                    pattern[i, j] = 1
        return pattern

    def paint_pattern(self, pattern):
        """Output pattern to grid"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = "black" if pattern[i, j] == 1 else "white"
                self.buttons[i][j].config(bg=color)

    def save_pattern(self):
        """Saves currently marked pattern to np array"""
        if len(self.saved_patterns) >= self.max_saved:
            self.saved_patterns.pop(0)
            print("Oldest pattern removed!")
        pattern = self.extract_pattern()
        self.saved_patterns.append(pattern)
        print("Pattern saved!")

    def train_network(self):
        """Trains the network using saved patterns"""
        self.hopfield_net.train(self.saved_patterns)
        print("Network trained!")

    def repair_pattern(self):
        """Synchronously repairs current pattern using Hopfield NN"""
        pattern = self.extract_pattern()
        recovered = self.hopfield_net.recover(pattern, mode="synchronous")
        self.paint_pattern(recovered)
        print("Pattern synchronously repaired!")

    def repair_pattern_async(self):
        """Asynchronously repairs current pattern using Hopfield NN"""
        pattern = self.extract_pattern()
        recovered = self.hopfield_net.recover(pattern, mode="asynchronous")
        self.paint_pattern(recovered)
        print("Pattern asynchronously repaired!")

    def show_saved_patterns(self):
        """Cycles through saved patterns, outputting them to grid"""
        if not self.saved_patterns:
            return
        pattern = self.saved_patterns[self.current_saved]
        self.current_saved = (self.current_saved + 1) % len(self.saved_patterns)
        self.paint_pattern(pattern)
        print(f"Displaying pattern {self.current_saved}")

    def clear_grid(self):
        """Unmarks all cells in current grid"""
        for row in self.buttons:
            for btn in row:
                btn.config(bg="white")
