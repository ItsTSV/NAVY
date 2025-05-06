import numpy as np
import matplotlib.pyplot as plt


class ChaoticSystem:
    """Class for demonstrating deterministic chaos.

    Attributes:
        r_values (np.linspace): Range of r values for the bifurcation diagram.
        iterations (int): Number of iterations for the logistic map.
        last_points (int): Number of last points to plot.
        initial_x (float): Initial value of x for the logistic map.
        chaos_threshold (float): Threshold for chaos in the system.
        noise_level (float): Error added to noise in the prediction.
    """

    def __init__(
        self,
        r_range=(0, 4),
        r_resolution=1000,
        iterations=1000,
        last_points=100,
        initial_x=1e-5,
        chaos_threshold=3.5,
        noise_level=2,
    ):
        """Initializes the ChaoticSystemPredictor with the given parameters."""
        self.r_values = np.linspace(r_range[0], r_range[1], r_resolution)
        self.iterations = iterations
        self.last_points = last_points
        self.initial_x = initial_x
        self.chaos_threshold = chaos_threshold
        self.noise_level = noise_level

        # Init storage
        self.r_list = []
        self.x_list = []
        self.prediction_list = []

    def logistic_map(self, x, r):
        """Logistic map function."""
        return r * x * (1 - x)

    def add_chaotic_error(self, x, r):
        """Adds error to the prediction based on the chaos level.

        This is only a SIMULATION of the chaotic system, not a real prediction, because I wanted to
        avoid training a neural network for that.
        """
        if r < self.chaos_threshold:
            return x

        error = (
            np.random.random()
            * self.noise_level
            * (r - self.chaos_threshold)
            * np.random.choice([-1, 1])
        )
        return (x + error) % 1

    def simulate(self):
        """Runs simulation to generate bifurcation diagram data."""
        self.r_list = []
        self.x_list = []
        self.prediction_list = []

        for r in self.r_values:
            x = self.initial_x

            # Skip the first iterations to let the system settle
            for _ in range(self.iterations - self.last_points):
                x = self.logistic_map(x, r)

            # Generates the last points
            for _ in range(self.last_points):
                x = self.logistic_map(x, r)
                self.r_list.append(r)
                self.x_list.append(x)
                self.prediction_list.append(self.add_chaotic_error(x, r))

    def plot_results(self, filename="real_bifurcation_diagram.png"):
        """Plot the bifurcation diagram and the predicted values."""
        plt.figure(figsize=(12, 8))

        # Real bifurcation diagram
        plt.subplot(2, 1, 1)
        plt.plot(self.r_list, self.x_list, ",k", alpha=0.7)
        plt.title("Bifurcation diagram")
        plt.xlabel("r parameter")
        plt.ylabel("x values")
        plt.grid(True, linewidth=0.5, linestyle="dotted")

        # Predicted values
        plt.subplot(2, 1, 2)
        plt.plot(self.r_list, self.prediction_list, ",", color="red", alpha=0.7)
        plt.title("Simulated prediction")
        plt.xlabel("r parameter")
        plt.ylabel("x values")
        plt.grid(True, linewidth=0.5, linestyle="dotted")

        plt.tight_layout()
        plt.savefig(filename, dpi=100)
        plt.show()
