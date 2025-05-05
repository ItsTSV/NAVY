import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.patches import Circle


class DoublePendulum:
    def __init__(self):
        self.length_1 = 1.0
        self.length_2 = 1.0
        self.mass_1 = 1.0
        self.mass_2 = 1.0
        self.gravity = 9.81

        self.time_step = 0.01
        self.simulation_time = 30.0
        self.time_array = np.arange(0, self.simulation_time + self.time_step, self.time_step)

        self.initial_state = np.array([3 * np.pi / 7, 0, 3 * np.pi / 4, 0])
        self.state_trajectory = None

        self.x1_array = None
        self.y1_array = None
        self.x2_array = None
        self.y2_array = None

        self.trail_duration = 1.0  # seconds
        self.max_trail_length = int(self.trail_duration / self.time_step)

    def simulate(self):
        self.state_trajectory = odeint(
            self._derivatives,
            self.initial_state,
            self.time_array,
            args=(self.length_1, self.length_2, self.mass_1, self.mass_2)
        )

        energy_initial = self._total_energy(self.initial_state)
        energy_drift = np.max(np.abs(self._total_energy(self.state_trajectory) - energy_initial))

        if energy_drift > 0.05:
            raise ValueError(f"Energy drift exceeded: {energy_drift}")

        self._convert_to_cartesian()

    def _derivatives(self, state, _, length_1, length_2, mass_1, mass_2):
        theta1, omega1, theta2, omega2 = state
        delta_theta = theta1 - theta2
        cos_delta = np.cos(delta_theta)
        sin_delta = np.sin(delta_theta)

        denom_1 = length_1 * (mass_1 + mass_2 * sin_delta**2)
        denom_2 = length_2 * (mass_1 + mass_2 * sin_delta**2)

        omega1_dot = (
            mass_2 * self.gravity * np.sin(theta2) * cos_delta
            - mass_2 * sin_delta * (length_1 * omega1**2 * cos_delta + length_2 * omega2**2)
            - (mass_1 + mass_2) * self.gravity * np.sin(theta1)
        ) / denom_1

        omega2_dot = (
            (mass_1 + mass_2) * (
                length_1 * omega1**2 * sin_delta
                - self.gravity * np.sin(theta2)
                + self.gravity * np.sin(theta1) * cos_delta
            )
            + mass_2 * length_2 * omega2**2 * sin_delta * cos_delta
        ) / denom_2

        return [omega1, omega1_dot, omega2, omega2_dot]

    def _total_energy(self, state_array):
        theta1 = state_array[:, 0] if state_array.ndim == 2 else state_array[0]
        omega1 = state_array[:, 1] if state_array.ndim == 2 else state_array[1]
        theta2 = state_array[:, 2] if state_array.ndim == 2 else state_array[2]
        omega2 = state_array[:, 3] if state_array.ndim == 2 else state_array[3]

        potential = (
            -(self.mass_1 + self.mass_2) * self.length_1 * self.gravity * np.cos(theta1)
            - self.mass_2 * self.length_2 * self.gravity * np.cos(theta2)
        )

        kinetic = (
            0.5 * self.mass_1 * (self.length_1 * omega1)**2
            + 0.5 * self.mass_2 * (
                (self.length_1 * omega1)**2 +
                (self.length_2 * omega2)**2 +
                2 * self.length_1 * self.length_2 * omega1 * omega2 * np.cos(theta1 - theta2)
            )
        )

        return potential + kinetic

    def _convert_to_cartesian(self):
        theta1 = self.state_trajectory[:, 0]
        theta2 = self.state_trajectory[:, 2]

        self.x1_array = self.length_1 * np.sin(theta1)
        self.y1_array = -self.length_1 * np.cos(theta1)
        self.x2_array = self.x1_array + self.length_2 * np.sin(theta2)
        self.y2_array = self.y1_array - self.length_2 * np.cos(theta2)

    def draw(self, frames_per_second=30):
        frame_step = int(1 / frames_per_second / self.time_step)
        fig, axis = plt.subplots(figsize=(8.33, 6.25), dpi=72)
        plt.ion()

        while True:
            for frame_index in range(0, len(self.time_array), frame_step):
                self._draw_frame(axis, frame_index)
                plt.pause(1 / frames_per_second)

    def _draw_frame(self, axis, index):
        axis.clear()

        axis.plot(
            [0, self.x1_array[index], self.x2_array[index]],
            [0, self.y1_array[index], self.y2_array[index]],
            lw=2,
            c='black'
        )

        axis.add_patch(Circle((0, 0), 0.025, fc='black', zorder=10))
        axis.add_patch(Circle((self.x1_array[index], self.y1_array[index]), 0.05, fc='blue', ec='blue', zorder=10))
        axis.add_patch(Circle((self.x2_array[index], self.y2_array[index]), 0.05, fc='red', ec='red', zorder=10))

        trail_segments = 20
        trail_step = self.max_trail_length // trail_segments

        for segment_index in range(trail_segments):
            start_index = index - (trail_segments - segment_index) * trail_step
            if start_index < 0:
                continue
            end_index = start_index + trail_step + 1
            alpha = (segment_index / trail_segments) ** 2
            axis.plot(
                self.x2_array[start_index:end_index],
                self.y2_array[start_index:end_index],
                c='red',
                lw=2,
                alpha=alpha
            )

        axis.set_xlim(-self.length_1 - self.length_2 - 0.1, self.length_1 + self.length_2 + 0.1)
        axis.set_ylim(-self.length_1 - self.length_2 - 0.1, self.length_1 + self.length_2 + 0.1)
        axis.set_aspect('equal')
        plt.axis('off')



if __name__ == "__main__":
    pendulum = DoublePendulum()
    pendulum.simulate()
    pendulum.draw()
