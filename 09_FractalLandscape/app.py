import tkinter as tk
from math import sin, cos, radians
import numpy as np


class LandscapeApp:
    """Graphical interface for generating 2D landscapes using fractal noise"""

    def __init__(self, root):
        self.root = root
        self.root.title("Landscape App")

        # Main layout
        self.frame_left = tk.Frame(root)
        self.frame_left.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

        # Left frame
        self.canvas = tk.Canvas(self.frame_left, width=900, height=900)
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, 900, 900, fill="lightblue")

        self.start_x = tk.Entry(self.frame_right, width=10)
        self.start_x.insert(0, "0")
        self.start_x.grid(row=0, column=1)
        self.start_x_label = tk.Label(self.frame_right, text="Start X")
        self.start_x_label.grid(row=0, column=0)

        self.start_y = tk.Entry(self.frame_right, width=10)
        self.start_y.insert(0, "450")
        self.start_y.grid(row=1, column=1)
        self.start_y_label = tk.Label(self.frame_right, text="Start Y")
        self.start_y_label.grid(row=1, column=0)

        self.end_x = tk.Entry(self.frame_right, width=10)
        self.end_x.insert(0, "900")
        self.end_x.grid(row=2, column=1)
        self.end_x_label = tk.Label(self.frame_right, text="End X")
        self.end_x_label.grid(row=2, column=0)

        self.end_y = tk.Entry(self.frame_right, width=10)
        self.end_y.insert(0, "450")
        self.end_y.grid(row=3, column=1)
        self.end_y_label = tk.Label(self.frame_right, text="End Y")
        self.end_y_label.grid(row=3, column=0)

        self.iteration_count = tk.Entry(self.frame_right, width=10)
        self.iteration_count.insert(0, "5")
        self.iteration_count.grid(row=4, column=1)
        self.iteration_count_label = tk.Label(self.frame_right, text="Iterations")
        self.iteration_count_label.grid(row=4, column=0)

        self.offset = tk.Entry(self.frame_right, width=10)
        self.offset.insert(0, "25")
        self.offset.grid(row=5, column=1)
        self.offset_label = tk.Label(self.frame_right, text="Offset")
        self.offset_label.grid(row=5, column=0)

        self.draw = tk.Button(self.frame_right, text="Draw", command=self._parse_and_draw)
        self.draw.grid(row=6, column=0, columnspan=2)

        self.clear = tk.Button(self.frame_right, text="Clear", command=self._clear)
        self.clear.grid(row=7, column=0, columnspan=2)

    def _parse_and_draw(self):
        start_x = int(self.start_x.get())
        start_y = int(self.start_y.get())
        end_x = int(self.end_x.get())
        end_y = int(self.end_y.get())
        iteration_count = int(self.iteration_count.get())
        offset = int(self.offset.get())

        y = (start_y + end_y) / 2
        self._draw_fractal(start_x, start_y, end_x, end_y, iteration_count, offset)

    def _draw_fractal(self, start_x, start_y, end_x, end_y, iteration_count, offset):
        # Find line center and new y
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2
        center_y += offset if np.random.rand() > 0.5 else -offset

        # Kill recursion
        if iteration_count == 1:
            self.canvas.create_line(start_x, start_y, center_x, center_y, fill="black")
            self.canvas.create_line(center_x, center_y, end_x, end_y, fill="black")
            return

        # Call recursively
        self._draw_fractal(start_x, start_y, center_x, center_y, iteration_count - 1, offset)
        self._draw_fractal(center_x, start_y, end_x, center_y, iteration_count - 1, offset)

    def _clear(self):
        self.canvas.create_rectangle(0, 0, 900, 900, fill="lightblue")
