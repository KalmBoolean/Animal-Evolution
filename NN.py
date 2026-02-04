import math

class Node:
    def __init__(self, bias=0.0, dec=0.9):
        self.bias = bias
        self.dec = dec
        self.output = 0.0
        self.e = None 

    def Out(self, inputs, weights):
        if self.e is None:
            self.e = [0.0] * len(weights)

        self.output = sum(i * w for i, w in zip(inputs, weights)) + self.bias
        y = math.tanh(self.output)

        deri = 1.0 - y * y #calc how much final output changes with self.output(cuz sometimes if self.output is too high, tanh wouldnt change much, so its eligibility would have to be low)

        for k in range(len(weights)):
            self.e[k] = self.dec * self.e[k] + inputs[k] * deri

        return y


#very basic, no hidden layer
class NeuralNet:
    def __init__(self, numInput, numOutput):
        self.numInput = numInput
        self.numOutput = numOutput

        self.weights = [
            [0.0 for _ in range(numInput)]
            for _ in range(numOutput)
        ]
        self.outputLayer = [Node() for _ in range(numOutput)]

    def Out(self, inputs):
        outputs = []
        for j in range(self.numOutput):
            out = self.outputLayer[j].Out(
                inputs,
                self.weights[j]
            )
            outputs.append(out)
        return outputs
    
    def HebbLearn(self, a: float, inputs):
        nodesArray = self.outputLayer
        for i in range(len(nodesArray)):
            for j in range(len(nodesArray[i].e)):
                self.weights[i][j] += a * nodesArray[i].e * inputs[j] * math.tanh(nodesArray[i].output)
            nodesArray[i].bias += a * math.tanh(nodesArray[i].output) 


