from NN import *
import random as rd
import pygame
import torch as tc

class Animal:
    def __init__(self,name = "DefaultPeanut",powLevel = 0,Hunger = 0,Fertility = 0,isPredator : bool = False):
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
       self.lastFit = 0
       self.isAlive = True
       self.brain = PeanutBrainBuild()
       self.rect = pygame.Rect(0,0,20,20)
    def Die(self):
        self.Fitness -= 1
        self.isAlive = False
        return self.Fitness
    def RandomiseProperties(self):
        self.powLevel = rd.uniform(0.5, 2.0)                 
        self.Fertility = rd.uniform(0.1, 1.0)       
        self.Fitness = 0
        self.isAlive = True
        self.isPredator = rd.randint(0, 1)
        self.Hunger = rd.uniform(0, self.powLevel + self.Fertility) * 100
    def Reason(self):
        inputs = tc.tensor([
            self.Satiation,
            self.Hunger,
            self.Fertility,
            self.BoundDist,
            self.EnemyDist,
            self.FoodDist,
            self.powLevel
        ], dtype=tc.float32)

        out = self.brain(inputs)

        #flatten
        out = out.view(-1)

        dx = out[0].item()
        dy = out[1].item()

        return dx, dy
    def calcDelta(self):
        d = self.Fitness - self.lastFit
        self.lastFit = self.Fitness
        return d


        
