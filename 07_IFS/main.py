import numpy as np
import matplotlib.pyplot as plt

# 0-8 -> a-i, 9-11 -> j-l
transformations = [
    (0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00),
    (0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24, 0.00, 0.80, 0.00),
    (-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24, 0.00, 0.22, 0.00),
    (0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84, 0.00, 0.80, 0.00),
]

transformations2 = [
    (0.05, 0.00, 0.00, 0.00, 0.60, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00),
    (0.45, -0.22, 0.22, 0.22, 0.45, 0.22, -0.22, 0.00, -0.45, 0.00, 1.00, 0.00),
    (-0.45, 0.22, -0.22, 0.22, 0.45, 0.22, -0.22, 0.00, 0.45, 0.00, 1.25, 0.00),
    (0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49, 0.00, 2.00, 0.00),
]


def run_ifs(transform_list, n_points=10000):
    """Generates n-points based on IFS algorithm and given transformations

    1. Select random transformation
    2. Compute new point using the selected transformation
    3. Add the point to history, so it can be drawn later

    Returns:
        points: np.array, IFS fractal points that can be drawn
    """
    points = np.zeros((n_points, 3))
    current_point = np.array([0.0, 0.0, 0.0])

    for i in range(n_points):
        t = transform_list[np.random.randint(len(transform_list))]
        a = np.array([[t[0], t[1], t[2]], [t[3], t[4], t[5]], [t[6], t[7], t[8]]])
        b = np.array([t[9], t[10], t[11]])
        current_point = a @ current_point + b
        points[i] = current_point
    return points


# Run both models
points1 = run_ifs(transformations)
points2 = run_ifs(transformations2)

# Plotting the first model
fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(121, projection="3d")
ax1.scatter(points1[:, 0], points1[:, 1], points1[:, 2], s=0.2, color="green")
ax1.set_title("First model")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")

# Plotting the second model
ax2 = fig.add_subplot(122, projection="3d")
ax2.scatter(points2[:, 0], points2[:, 1], points2[:, 2], s=0.2, color="green")
ax2.set_title("Second model")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")

# Show
plt.tight_layout()
plt.show()
