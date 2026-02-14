import torch as tc
import torch.nn as nn

class BrainLayer(nn.Module):
    def __init__(self, numin,numout):
        super().__init__()
        self.actLayer = nn.Linear(numin,numout)
        self.e = tc.zeros_like(self.actLayer.weight)
        nn.init.normal_(self.actLayer.weight, 0, 0.1)
        self.actfn = nn.LeakyReLU(0.01)
    def forward(self,x, out: bool):
        if out:
            y = tc.tanh(self.actLayer(x))
        else:
            y = self.actfn(self.actLayer(x))
        self.lx = x.detach()
        self.ly = y.detach()
        return y
    def UpdateE(self, dec): 
        self.e = dec * self.e + tc.outer(self.ly, self.lx) 
    
    def HebbLearn(self, lr, deltaF): 
        with tc.no_grad(): 
            self.actLayer.weight += lr * deltaF * self.e

class Brain(nn.Module):
    def __init__(self):
        super().__init__()
        self.lays = []
    def AddLayer(self,l : BrainLayer):
        self.lays.append(l)
    def BuildBrain(self):
        self.layers = nn.ModuleList(self.lays)

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            out = (i == len(self.layers) - 1)
            x = layer(x, out)
        return x

    def UpdateE(self, dec):
        for layer in self.layers:
            layer.UpdateE(dec)

    def HebbPulse(self, lr, deltaF):   
        for layer in self.layers:
            layer.HebbLearn(lr,deltaF)

def PeanutBrainBuild():
    brain = Brain()
    brain.AddLayer(BrainLayer(7,16))
    brain.AddLayer(BrainLayer(16,8))
    brain.AddLayer(BrainLayer(8,2))
    brain.BuildBrain()
    return brain





