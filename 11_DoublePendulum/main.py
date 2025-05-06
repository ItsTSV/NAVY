import numpy as np
from double_pendulum import DoublePendulum

if __name__ == "__main__":
    pendulum = DoublePendulum(length1=1.0, length2=1.0, mass1=1.0, mass2=1.0)
    initial_state = [np.pi / 2, 0, np.pi, 0]
    pendulum.solve(initial_state)
    pendulum.animate()
