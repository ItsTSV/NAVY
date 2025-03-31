import tkinter as tk
import numpy as np


def _parse_axiom(rule, axiom, nesting):
    for _ in range(nesting):
        parts = rule.split(" -> ")
        assert len(parts) == 2, "Not a valid rule! Use format Symbol -> Expand!"
        axiom = axiom.replace(parts[0], parts[1])

    return axiom


class LSystemApp:
    """Graphical interface and pattern handling for Hopfield network"""

    def __init__(self, root):
        self.root = root
        self.root.title("L-System App")

        # Main layout
        self.frame_left = tk.Frame(root)
        self.frame_left.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

        # Left frame
        self.canvas = tk.Canvas(self.frame_left, width=900, height=900)
        self.canvas.pack()

        # Right frame - controls -- Start X, Start Y, Starting Degree, Nesting count, Line length, Axiom, Rule, Draw button
        self.start_x = tk.Entry(self.frame_right, width=10)
        self.start_x.insert(0, "450")
        self.start_x.grid(row=0, column=1)
        self.start_x_label = tk.Label(self.frame_right, text="Start X")
        self.start_x_label.grid(row=0, column=0)

        self.start_y = tk.Entry(self.frame_right, width=10)
        self.start_y.insert(0, "450")
        self.start_y.grid(row=1, column=1)
        self.start_y_label = tk.Label(self.frame_right, text="Start Y")
        self.start_y_label.grid(row=1, column=0)

        self.start_degree = tk.Entry(self.frame_right, width=10)
        self.start_degree.insert(0, "0")
        self.start_degree.grid(row=2, column=1)
        self.start_degree_label = tk.Label(self.frame_right, text="Start Degree")
        self.start_degree_label.grid(row=2, column=0)

        self.nesting = tk.Entry(self.frame_right, width=10)
        self.nesting.insert(0, "5")
        self.nesting.grid(row=3, column=1)
        self.nesting_label = tk.Label(self.frame_right, text="Nesting")
        self.nesting_label.grid(row=3, column=0)

        self.line_length = tk.Entry(self.frame_right, width=10)
        self.line_length.insert(0, "10")
        self.line_length.grid(row=4, column=1)
        self.line_length_label = tk.Label(self.frame_right, text="Line Length")
        self.line_length_label.grid(row=4, column=0)

        self.axiom = tk.Entry(self.frame_right, width=10)
        self.axiom.insert(0, "F")
        self.axiom.grid(row=5, column=1)
        self.axiom_label = tk.Label(self.frame_right, text="Axiom")
        self.axiom_label.grid(row=5, column=0)

        self.rule = tk.Entry(self.frame_right, width=10)
        self.rule.insert(0, "F-F+F+F-F")
        self.rule.grid(row=6, column=1)
        self.rule_label = tk.Label(self.frame_right, text="Rule")
        self.rule_label.grid(row=6, column=0)

        self.draw_button = tk.Button(self.frame_right, text="Draw", command=self.draw)
        self.draw_button.grid(row=7, column=0, columnspan=2)

    def draw(self):
        start_x = int(self.start_x.get())
        start_y = int(self.start_y.get())
        start_degree = int(self.start_degree.get())
        nesting_count = int(self.nesting.get())
        length = int(self.line_length.get())
        axiom = self.axiom.get()
        rule = self.rule.get()

        # Adjust axiom
        axiom = _parse_axiom(rule, axiom, nesting_count)

        # Run, draw
