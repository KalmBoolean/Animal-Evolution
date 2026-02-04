from animal import Animal
import random as rd

def Crossover(a1: Animal, a2: Animal):
    #param crossover:
    achild = Animal("child" + a1.Name + a2.Name,0,0,0,a1.isPredator)

    params = [
    "powLevel", "Hunger", "BoundDist",
    "EnemyDist", "Fertility", "Satiation", "FoodDist"
    ]

    for param in params:
        a = rd.uniform(0.0, 1.0)
        a1param = getattr(a1,param)
        a2param = getattr(a2,param)
        val = a * a1param + (1 - a) * a2param
        setattr(achild, param, val)
    
    #weight crossover:
