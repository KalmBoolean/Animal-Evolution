import pygame
class Food:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,10,10)
        self.isConsumed = False
    def Consume(self, animal):
        if  not animal.isAlive:
            print("ded animul no no foody")
            return
        animal.Satiation = min(100, animal.Satiation + 30)
        animal.Fitness += 1
        self.isConsumed = True