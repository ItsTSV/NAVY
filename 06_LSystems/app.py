import tkinter as tk
from math import sin, cos, radians


def _parse_axiom(rule, axiom, nesting):
    """Iteratively parses the axiom according to selected nesting"""
    for _ in range(nesting):
        parts = rule.split(" -> ")
        assert len(parts) == 2, "Not a valid rule! Use format Symbol -> Expand!"
        axiom = axiom.replace(parts[0], parts[1])

    return axiom


class LSystemApp:
    """Graphical interface and pattern handling for Hopfield network"""

    def __init__(self, root):
        """Initializes ton of components + some saved patterns"""
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
        self.canvas.create_rectangle(0, 0, 900, 900, fill="white")

        self.start_x = tk.Entry(self.frame_right, width=10)
        self.start_x.insert(0, "200")
        self.start_x.grid(row=0, column=1)
        self.start_x_label = tk.Label(self.frame_right, text="Start X")
        self.start_x_label.grid(row=0, column=0)

        self.start_y = tk.Entry(self.frame_right, width=10)
        self.start_y.insert(0, "200")
        self.start_y.grid(row=1, column=1)
        self.start_y_label = tk.Label(self.frame_right, text="Start Y")
        self.start_y_label.grid(row=1, column=0)

        self.start_degree = tk.Entry(self.frame_right, width=10)
        self.start_degree.insert(0, "90")
        self.start_degree.grid(row=2, column=1)
        self.start_degree_label = tk.Label(self.frame_right, text="Start Degree")
        self.start_degree_label.grid(row=2, column=0)

        self.nesting = tk.Entry(self.frame_right, width=10)
        self.nesting.insert(0, "4")
        self.nesting.grid(row=3, column=1)
        self.nesting_label = tk.Label(self.frame_right, text="Nesting")
        self.nesting_label.grid(row=3, column=0)

        self.line_length = tk.Entry(self.frame_right, width=10)
        self.line_length.insert(0, "10")
        self.line_length.grid(row=4, column=1)
        self.line_length_label = tk.Label(self.frame_right, text="Line Length")
        self.line_length_label.grid(row=4, column=0)

        self.axiom = tk.Entry(self.frame_right, width=10)
        self.axiom.insert(0, "F+F+F+F")
        self.axiom.grid(row=5, column=1)
        self.axiom_label = tk.Label(self.frame_right, text="Axiom")
        self.axiom_label.grid(row=5, column=0)

        self.rule = tk.Entry(self.frame_right, width=10)
        self.rule.insert(0, "F -> F+F-F")
        self.rule.grid(row=6, column=1)
        self.rule_label = tk.Label(self.frame_right, text="Rule")
        self.rule_label.grid(row=6, column=0)

        self.angle = tk.Entry(self.frame_right, width=10)
        self.angle.insert(0, "90")
        self.angle.grid(row=7, column=1)
        self.angle_label = tk.Label(self.frame_right, text="Angle")
        self.angle_label.grid(row=7, column=0)

        self.draw_button = tk.Button(self.frame_right, text="Draw", command=self._draw)
        self.draw_button.grid(row=8, column=0, columnspan=2)

        self.reset_button = tk.Button(
            self.frame_right, text="Reset", command=self._reset
        )
        self.reset_button.grid(row=9, column=0, columnspan=2)

        self.saved_button = tk.Button(
            self.frame_right, text="Cycle Saved", command=self._cycle_saved
        )
        self.saved_button.grid(row=10, column=0, columnspan=2)

        # Parts
        self.saved_index = 0
        self.saved_patterns = [
            ("F+F+F+F", "F -> F+F-F-FF+F+F-F", "90", "3", "5"),
            ("F++F++F", "F -> F+F--F+F", "60", "3", "15"),
            ("F", "F -> F[+F]F[-F]F", "25.7", "3", "18"),
            ("F", "F -> FF+[+F-F-F]-[-F+F+F]", "22.5", "3", "18"),
        ]

    def _draw(self):
        """Collects inputs from user interface, parses the axiom and runs the algorithm"""
        start_x = int(self.start_x.get())
        start_y = int(self.start_y.get())
        start_degree = int(self.start_degree.get())
        nesting_count = int(self.nesting.get())
        line_length = int(self.line_length.get())
        angle_change = float(self.angle.get())
        axiom = self.axiom.get()
        rule = self.rule.get()

        # Adjust axiom
        axiom = _parse_axiom(rule, axiom, nesting_count)
        print(axiom)

        # Current pos
        pos_x = start_x
        pos_y = start_y
        angle = start_degree

        # Checkpoints
        checkpoints = []

        # Run, draw
        for symbol in axiom:
            if symbol == " ":
                continue
            elif symbol == "[":  # Remember position rule
                checkpoints.append((pos_x, pos_y, angle))
            elif symbol == "]":  # Recall rule
                pos_x, pos_y, angle = checkpoints.pop()
                print(pos_x, pos_y, angle)
            elif symbol == "+":  # Turn rule
                angle -= angle_change
            elif symbol == "-":  # Turn rule
                angle += angle_change
            elif symbol in ["F", "b"]:  # Move, move and draw rules
                angle_rad = radians(angle)
                old_x = pos_x
                old_y = pos_y
                pos_x = old_x + (sin(angle_rad) * line_length)
                pos_y = old_y + (cos(angle_rad) * line_length)
                if symbol == "F":
                    self.canvas.create_line(old_x, old_y, pos_x, pos_y)

    def _reset(self):
        """Resets the canvas content"""
        self.canvas.create_rectangle(0, 0, 900, 900, fill="white")

    def _cycle_saved(self):
        """Not the most effective implementation -- I did it in a train w/o wifi, tho"""
        # Delete stuff
        self.axiom.delete(0, len(self.axiom.get()))
        self.rule.delete(0, len(self.rule.get()))
        self.angle.delete(0, len(self.angle.get()))
        self.nesting.delete(0, len(self.nesting.get()))
        self.line_length.delete(0, len(self.line_length.get()))

        # Add stuff
        self.axiom.insert(0, self.saved_patterns[self.saved_index][0])
        self.rule.insert(0, self.saved_patterns[self.saved_index][1])
        self.angle.insert(0, self.saved_patterns[self.saved_index][2])
        self.nesting.insert(0, self.saved_patterns[self.saved_index][3])
        self.line_length.insert(0, self.saved_patterns[self.saved_index][4])

        # Refresh
        self.saved_index = (self.saved_index + 1) % len(self.saved_patterns)
        self._reset()
        self._draw()
