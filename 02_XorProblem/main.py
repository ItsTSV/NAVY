import numpy as np
from xor_neural_network import XorNeuralNetwork

if __name__ == "__main__":
    # Prepare inputs and labels
    inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    labels = np.array([[0], [1], [1], [0]])

    # Create the network (parameters are default)
    network = XorNeuralNetwork()
    network.print_info()

    # Train for 50k epochs
    print("\nTraining the network...\n")
    network.train(inputs, labels, 50000)
    network.print_info()

    # Predict the labels
    print("\nEvaluating the network...\n")
    predictions = network.predict(inputs)
    print("Predictions -- Correct labels:")
    for i in range(len(predictions)):
        print(f"{predictions[i]} -- {labels[i]}")
