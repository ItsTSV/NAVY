import numpy as np


class Perceptron:
    def __init__(self, input_size, learning_rate=0.1):
        """Create perceptron with weights and bias randomly set between -1 and 1"""
        self.weights = np.random.uniform(-1, 1, input_size)
        self.bias = np.random.rand() * 2 - 1
        print(self.bias)
        self.learning_rate = learning_rate

    def activation_function(self, x):
        """Step function"""
        return 1 if x > 0 else 0

    def predict(self, input):
        """Predict the output based on input values, weights and bias"""
        return self.activation_function(np.dot(self.weights, input) + self.bias)

    def train(self, inputs, labels, epochs):
        """Train the perceptron for given number of epochs

        Every epoch, go through the whole inputs array. For each element of that array,
        make a prediction and calculate an error based on whether it's correct or not
        (predicted classes are different -> the error is not 0)

        Args:
            inputs: np.array of np.arrays, whatever we attempt to predict
            labels: np.array of ints, the correct prediction
            epochs: int, for how long we train
        """
        for _ in range(epochs):
            for i in range(len(inputs)):
                prediction = self.predict(inputs[i])
                error = labels[i] - prediction
                self.weights += self.learning_rate * error * inputs[i]
                self.bias += self.learning_rate * error
