import numpy as np
import matplotlib.pyplot as plt
from Perceptron import Perceptron


def get_points(count, low, high):
    """Get array of 2d points in given range"""
    return [np.array([x, y]) for x, y in zip(np.random.uniform(low, high, count), np.random.uniform(low, high, count))]


def plot_points(points, perceptron):
    """Plot points + given function line in 2D space

    Args:
        points: np.array, TEST set of points
        perceptron: Perceptron, trained perceptron which will be used to predict the points classes
    """
    # Extract x, y values
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    # Predict the classes, color the points
    colors = ['red' if perceptron.predict(p) == 1 else 'blue' for p in points]
    plt.scatter(x_values, y_values, c=colors)

    # Plot the function line
    x_range = np.linspace(-10, 10, 100)
    y_range = 3 * x_range + 2
    plt.plot(x_range, y_range, color="black", linestyle="--", label="y = 3x + 2")

    # Random plotting go
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Get train points + labels and test points ready
    points_train = get_points(200, -25, 26)
    points_train_labels = [1 if y > 3 * x + 2 else 0 for x, y in points_train]
    points_test = get_points(100, -25, 26)

    # Get perceptron ready, train it
    perceptron = Perceptron(2)
    perceptron.train(points_train, points_train_labels, 100)

    # Plot the test points and see the predictions ;)
    plot_points(points_test, perceptron)
