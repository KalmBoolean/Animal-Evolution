from NN import *
class Animal:
    def __init__(self,name,powLevel,Hunger,Fertility,isPredator : bool = False):
       self.Name = name
       self.powLevel = powLevel
       self.Hunger = Hunger
       self.Fertility = Fertility       
       self.EnemyDist = 0
       self.Satiation = 100
       self.FoodDist = 0
       self.BoundDist = 0
       self.isPredator = int(isPredator)
       self.Fitness = 0
       self.isAlive = True
       self.brain = PeanutBrainBuild()
    def Die(self):
        self.Fitness -= 1
        self.isAlive = False
        return self.Fitness
