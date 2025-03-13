import numpy as np


class XorNeuralNetwork:
    def __init__(self, hidden_layer_size=2, learning_rate=0.1):
        """Initialize the neural network with given parameters. The weights are set to random
        values between -1 and 1. The biases are set to 0."""
        self.hidden_weights = 2 * np.random.rand(2, hidden_layer_size) - 1
        self.output_weights = 2 * np.random.rand(hidden_layer_size, 1) - 1
        self.hidden_bias = np.zeros((1, hidden_layer_size))
        self.output_bias = np.zeros((1, 1))
        self.learning_rate = learning_rate

    def sigmoid(self, x):
        """Sigmoid to transform numbers to range (0, 1)"""
        return 1 / (1 + np.exp(-x))

    def sigmoid_deriv(self, x):
        """Derived sigmoid for backpropagation"""
        return x * (1 - x)

    def train(self, inputs, labels, epochs):
        """Train the neural network for given number of epochs

        Args:
            inputs: np.array of XOR inputs
            labels: np.array of correct XOR outputs
            epochs: int, for how long we train
        """
        for _ in range(epochs):
            # Forward propagation (input -> hidden -> output)
            hidden_input = np.dot(inputs, self.hidden_weights) + self.hidden_bias
            hidden_output = self.sigmoid(hidden_input)

            final_input = np.dot(hidden_output, self.output_weights) + self.output_bias
            final_output = self.sigmoid(final_input)

            # Calculate error
            error = labels - final_output

            # Backward propagation
            d_output = error * self.sigmoid_deriv(final_output)
            d_hidden = d_output.dot(self.output_weights.T) * self.sigmoid_deriv(
                hidden_output
            )

            # Weight and bias adjustments
            self.output_weights += hidden_output.T.dot(d_output) * self.learning_rate
            self.hidden_weights += inputs.T.dot(d_hidden) * self.learning_rate
            self.output_bias += (
                np.sum(d_output, axis=0, keepdims=True) * self.learning_rate
            )
            self.hidden_bias += (
                np.sum(d_hidden, axis=0, keepdims=True) * self.learning_rate
            )

    def predict(self, inputs):
        """Predict the output based on input values (basically the forward method)

        Args:
            inputs: np.array of XOR inputs
        """
        hidden_output = self.sigmoid(
            np.dot(inputs, self.hidden_weights) + self.hidden_bias
        )
        final_output = self.sigmoid(
            np.dot(hidden_output, self.output_weights) + self.output_bias
        )
        return np.round(final_output)

    def print_info(self):
        """Print the weights and biases of the network. The printing code is a bit weird,
        because NumPy formatting is pain."""
        print("Hidden weights:")
        for weight in self.hidden_weights:
            print(f"\t{weight}")
        print(f"Hidden bias:\n\t{self.hidden_bias}")

        print("Output weights:")
        for weight in self.output_weights:
            print(f"\t{weight}")
        print(f"Output bias:\n\t{self.output_bias}")
