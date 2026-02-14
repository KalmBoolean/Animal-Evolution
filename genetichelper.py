from animal import Animal
import random as rd
import torch as tc
def Crossover(a1: Animal, a2: Animal):
    #param crossover:
    achild = Animal("child" + a1.Name + a2.Name,0,0,0,a1.isPredator)

    params = [
    "powLevel", "Hunger","Fertility"
    ]
    achild.Satiation = 100
    for param in params:
        a = rd.uniform(0.0, 1.0)
        a1param = getattr(a1,param)
        a2param = getattr(a2,param)
        val = a * a1param + (1 - a) * a2param
        val += rd.gauss(0,0.1)
        setattr(achild, param, val)
    
    #weight crossover:
    brain1 = a1.brain
    brain2 = a2.brain

    for i in range(len(brain1.layers)):
       a = rd.uniform(0.0, 1.0)
       adaptedWeight = a * brain1.layers[i].actLayer.weight + (1 - a) * brain2.layers[i].actLayer.weight
       x = tc.randn_like(adaptedWeight) * 0.1
       adaptedWeight += x
       with tc.no_grad():
        achild.brain.layers[i].actLayer.weight.copy_(adaptedWeight)
    return achild
    
    


