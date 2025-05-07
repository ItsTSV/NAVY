import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp


class DoublePendulum:
    """Class that simulates and animates a double pendulum system.

    Attributes:
        length1 (float): Length of the first pendulum.
        length2 (float): Length of the second pendulum.
        mass1 (float): Mass of the first pendulum.
        mass2 (float): Mass of the second pendulum.
        gravity (float): Gravitational acceleration.
        solution (scipy.integrate.OdeResult): Solution of the differential equations.
        theta1 (numpy.ndarray): Angles of the first pendulum over time.
        theta2 (numpy.ndarray): Angles of the second pendulum over time.

    Notes:
        omega: angular velocity
        initial_state: [theta1, omega1, theta2, omega2]
    """

    def __init__(self, length1=1.0, length2=1.0, mass1=1.0, mass2=1.0, gravity=9.81):
        """Initialize the double pendulum with physical parameters."""
        # Init physical parameters
        self.length1 = length1
        self.length2 = length2
        self.mass1 = mass1
        self.mass2 = mass2
        self.gravity = gravity

        # Init solution storage
        self.solution = None
        self.theta1 = None
        self.theta2 = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        # Init animation components
        self.fig = None
        self.ax = None
        self.line = None
        self.trace = None
        self.trace_mid = None
        self.time_text = None
        self.velocity1 = None
        self.velocity2 = None
        self.ani = None

    def derivatives(self, t, y):
        """Compute the derivatives for the double pendulum system.

        This is an utter mess; it somehow implements the stuff from slides, heavily borrowing from
        the tutorial in citations.
        """
        theta1, omega1, theta2, omega2 = y

        delta_theta = theta2 - theta1
        den1 = (
            self.mass1 + self.mass2
        ) * self.length1 - self.mass2 * self.length1 * np.cos(delta_theta) ** 2
        den2 = (self.length2 / self.length1) * den1

        derived_theta1 = omega1
        derived_omega1 = (
            self.mass2
            * self.length1
            * omega1**2
            * np.sin(delta_theta)
            * np.cos(delta_theta)
            + self.mass2 * self.gravity * np.sin(theta2) * np.cos(delta_theta)
            + self.mass2 * self.length2 * omega2**2 * np.sin(delta_theta)
            - (self.mass1 + self.mass2) * self.gravity * np.sin(theta1)
        ) / den1

        derived_theta2 = omega2
        derived_omega2 = (
            (
                -self.mass2
                * self.length2
                * omega2**2
                * np.sin(delta_theta)
                * np.cos(delta_theta)
                + (self.mass1 + self.mass2)
                * self.gravity
                * np.sin(theta1)
                * np.cos(delta_theta)
                - (self.mass1 + self.mass2)
                * self.length1
                * omega1**2
                * np.sin(delta_theta)
                - (self.mass1 + self.mass2) * self.gravity * np.sin(theta2)
            )
        ) / den2

        return [derived_theta1, derived_omega1, derived_theta2, derived_omega2]

    def solve(self, init_state, time_span=(0, 20), num_points=1000):
        """Solve the differential equations for given initial conditions."""
        t_eval = np.linspace(*time_span, num_points)
        self.solution = solve_ivp(self.derivatives, time_span, init_state, t_eval=t_eval)
        self.theta1 = self.solution.y[0]
        self.theta2 = self.solution.y[2]

        # Compute pendulum positions
        self.x1 = self.length1 * np.sin(self.theta1)
        self.y1 = -self.length1 * np.cos(self.theta1)
        self.x2 = self.x1 + self.length2 * np.sin(self.theta2)
        self.y2 = self.y1 - self.length2 * np.cos(self.theta2)

        return self.solution

    def init_animation(self):
        """Initialize the animation components."""
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlim(
            -(self.length1 + self.length2 + 0.5), self.length1 + self.length2 + 0.5
        )
        self.ax.set_ylim(
            -(self.length1 + self.length2 + 0.5), self.length1 + self.length2 + 0.5
        )
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.ax.grid(False)

        (self.line,) = self.ax.plot([], [], "o-", lw=2, color="black")
        (self.trace,) = self.ax.plot([], [], "-", lw=1, color="blue", alpha=0.2)
        (self.trace_mid,) = self.ax.plot([], [], "-", lw=1, color="red", alpha=0.2)
        self.time_text = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes)
        self.velocity1 = self.ax.text(0.02, 0.92, "", transform=self.ax.transAxes)
        self.velocity2 = self.ax.text(0.02, 0.89, "", transform=self.ax.transAxes)

    def init_func(self):
        """Initialization function for animation."""
        self.line.set_data([], [])
        self.trace.set_data([], [])
        self.trace_mid.set_data([], [])
        self.time_text.set_text("")
        self.velocity1.set_text("")
        self.velocity2.set_text("")
        return self.line, self.trace, self.trace_mid, self.time_text

    def update_func(self, frame):
        """Update function for animation."""
        x_points = [0, self.x1[frame], self.x2[frame]]
        y_points = [0, self.y1[frame], self.y2[frame]]

        self.line.set_data(x_points, y_points)
        self.trace.set_data(self.x2[: frame + 1], self.y2[: frame + 1])
        self.trace_mid.set_data(self.x1[: frame + 1], self.y1[: frame + 1])

        self.time_text.set_text(f"Time: {self.solution.t[frame]:.2f}s")
        self.velocity1.set_text(f"Velocity 1: {self.solution.y[1][frame]:.2f}")
        self.velocity2.set_text(f"Velocity 2: {self.solution.y[3][frame]:.2f}")
        return self.line, self.trace, self.trace_mid, self.time_text, self.velocity1, self.velocity2

    def animate(self, interval=20):
        """Create and run the animation."""
        if self.solution is None:
            raise ValueError("Call solve() before animate()")

        self.init_animation()
        self.ani = FuncAnimation(
            self.fig,
            self.update_func,
            frames=len(self.solution.t),
            init_func=self.init_func,
            blit=True,
            interval=interval,
        )
        plt.title("Double Pendulum")
        plt.show()
