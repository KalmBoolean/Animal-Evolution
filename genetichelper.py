from animal import Animal
import random as rd
import torch as tc

def Crossover(a1: Animal, a2: Animal):
    with tc.no_grad():
        # param crossover
        achild = Animal( 0, 0, 0, a1.isPredator)

        params = ["powLevel", "Hunger", "Fertility"]
        achild.Satiation = 100

        for param in params:
            a = rd.uniform(0.0, 1.0)
            val = a * getattr(a1, param) + (1 - a) * getattr(a2, param)
            val += rd.gauss(0, 0.1)
            setattr(achild, param, val)

        # weight crossover (fully in-place)
        brain1 = a1.brain
        brain2 = a2.brain

        for i in range(len(brain1.layers)):
            w1 = brain1.layers[i].actLayer.weight
            w2 = brain2.layers[i].actLayer.weight
            out = achild.brain.layers[i].actLayer.weight

            a = rd.uniform(0.0, 1.0)

            # out = a*w1 + (1-a)*w2   (done in-place)
            out.copy_(w1)
            out.mul_(a)
            out.add_(w2, alpha=(1 - a))

            out.add_(tc.randn_like(out), alpha=0.1)

        return achild
