import pygame
import random as rd
from pygame.math import Vector2
from animal import *
from genetichelper import *
from food import *
import time
import gc

width, height = 1280, 720
startNum = 20
foodspawnRate = 1200 
pulseRate = 7000 
foodRad = 6
animalRad = 10
maxFood = 10
animalList = []
foodList = []
rate = 0.5 #sat decrease rate
genCount = 0
totalGuyCount = 50
rewardRate = 4500
genTimer = 10000

def InitialSpawn(n):
    for _ in range(n):
        a = Animal()
        a.RandomiseProperties()

        a.rect.x = rd.randint(animalRad, width - animalRad)
        a.rect.y = rd.randint(animalRad, height - animalRad)
        a.speed = rd.uniform(1.2,2)

        animalList.append(a)


def SpawnFood():
    if len(foodList) >= maxFood:
        return
    x = rd.randint(10, width - 10)
    y = rd.randint(10, height - 10)

    foodList.append(Food(x,y))


def dist(a1 , a2):
    return Vector2(a1.rect.x,a1.rect.y).distance_to((a2.rect.x,a2.rect.y))


def UpdateBoundaryDist(animal):

    left = animal.rect.x
    right = width - animal.rect.x
    top = animal.rect.y
    bottom = height - animal.rect.y
    animal.BoundDist = min(left, right, top, bottom)


def UpdateDistances(animal):
    closestE = float("inf")
    closestF = float("inf")
    for other in animalList:
        if other.isAlive and other.isPredator and other != animal:
            d = dist(animal, other)
            if d < closestE:
                closestE = d
    for food in foodList:
        d = dist(animal, food)
        if d < closestF:
            closestF = d

    animal.EnemyDist = closestE if closestE != float("inf") else 999
    animal.FoodDist = closestF if closestF != float("inf") else 999

def MoveAnimal(animal):
    x,y = animal.Reason()

    animal.rect.x += x * animal.speed
    animal.rect.y += y * animal.speed

    # Hard boundary clamp
    animal.rect.x = max(animalRad, min(width - animalRad, animal.rect.x))
    animal.rect.y = max(animalRad, min(height - animalRad, animal.rect.y))

def UpdateDelta(animal):
    animal.calcDelta()

def LearnPulse():
    for animal in animalList:
        df = animal.calcDelta()
        if(df > 0):
            animal.brain.HebbPulse(0.25,df)


def DecreaseSatiation(animal: Animal):
    animal.Satiation -= rate * animal.Hunger/60
    if(animal.Satiation <= 0):
        print("animal ded due to low satiation, fitness: ",animal.Die())

def EatEmUp():
    rects = [a.rect for a in animalList]

    for i, animal in enumerate(animalList):
        hit = animal.rect.collidelistall(rects[i+1:])
        if hit:
            ani = [animalList[ind] for ind in hit]
            if any(a.isPredator == True for a in ani):
                ChanceGame(ani,animal)
            

def ChanceGame(other, animal):
    if not animal.isAlive:
        return
    for predator in other:
        if not predator.isPredator:
            continue
        chance = animal.powLevel/(animal.powLevel + predator.powLevel)
        roll = rd.uniform(0,1)
        if chance < roll:
            print("boohoo animal eaten with fitness: ", animal.Die())
            predator.Satiation = min(100,predator.Satiation + 40)
            predator.Fitness += 1
            break

def RizzGame(other, animal):
    if not animal.isAlive:
        return
    for mate in other:
        if not mate.isAlive:
            continue
        if mate.isPredator != animal.isPredator:
            continue
        chance = rd.uniform(0,animal.Fertility + mate.Fertility) / animal.Fertility + mate.Fertility
        roll = rd.uniform(0,1)
        if chance < roll:
            print("Animal Rejected")
            break
        else:
            animal.Satiation = max(0, animal.Satiation - 25)
            mate.Satiation = max(0, mate.Satiation - 25)
            WelcomeKid(animal,mate)
            break

def WelcomeKid(animal, mate):
    if len(animalList) >= totalGuyCount:
        print("animal limit exceeded")
        return
    print("Welcome, kid")
    animal.Fitness += 0.5
    mate.Fitness += 0.5
    child = Crossover(animal,mate)
    child.speed = rd.uniform(1.2,2)
    child.rect.x = (animal.rect.x + mate.rect.x)/2
    child.rect.y = (animal.rect.y + mate.rect.y)/2
    animalList.append(child)


def ConsumeDatFood(animal:Animal):
    if animal.isPredator:
        return
    for food in foodList:
        if animal.rect.colliderect(food.rect):
            food.Consume(animal)

def DecreaseFitness(animal: Animal):
    animal.Fitness -= 0.1/ 60

def RewardForSurvival():
    for animal in animalList:
        if animal.isAlive:
            animal.Fitness += 0.2

def BreedEmUp():
    rects = [a.rect for a in animalList]
    for i, animal in enumerate(animalList):
        hit = animal.rect.collidelistall(rects[i+1:])
        if hit:
            ani = [animalList[ind] for ind in hit]
            if any(a.isPredator == animal.isPredator for a in ani):
                RizzGame(ani,animal)
def NextGen():
    global genCount
    genCount += 1
    
    prey = [a for a in animalList if not a.isPredator]
    predators = [a for a in animalList if a.isPredator]
    
    prey.sort(key=lambda a: a.Fitness, reverse=True)
    predators.sort(key=lambda a: a.Fitness, reverse=True)

    bprey,sprey = prey[0],prey[1]
    bpred, spred = predators[0], predators[1]
    animalList.clear()
    numSplit = startNum//2
    for _ in range(numSplit):
        childprey = Crossover(bprey,sprey)
        childprey.speed = rd.uniform(0.5,2.5)
        childpred  = Crossover(bpred,spred)
        childpred.speed = rd.uniform(0.5,2.5)
        for layer in childpred.brain.layers:
            layer.e.zero_()
        for layer in childprey.brain.layers:
            layer.e.zero_()
        childprey.rect.x = rd.randint(animalRad, width - animalRad)
        childprey.rect.y = rd.randint(animalRad, height - animalRad)
        childpred.rect.x = rd.randint(animalRad, width - animalRad)
        childpred.rect.y = rd.randint(animalRad, height - animalRad)

        animalList.append(childprey)
        animalList.append(childpred)

    bprey.rect.x = rd.randint(animalRad, width - animalRad)
    bprey.rect.y = rd.randint(animalRad, height - animalRad)
    bpred.rect.x = rd.randint(animalRad, width - animalRad)
    bpred.rect.y = rd.randint(animalRad, height - animalRad)
    bprey.isAlive = True
    bpred.isAlive = True
    animalList.append(bprey)
    animalList.append(bpred)
    gc.collect()


pygame.init()

font = pygame.font.SysFont(None, 28)

lPulse = pygame.time.get_ticks()
lEatBreed = pygame.time.get_ticks()
lReward = pygame.time.get_ticks()
lNextGen = pygame.time.get_ticks()


screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

InitialSpawn(startNum)

foodSpawn = pygame.USEREVENT + 1
pulse = pygame.USEREVENT + 2
reward = pygame.USEREVENT + 3
eatorbreed = pygame.USEREVENT + 4
nextgen = pygame.USEREVENT + 5

pygame.time.set_timer(foodSpawn, foodspawnRate)
pygame.time.set_timer(pulse, pulseRate)
pygame.time.set_timer(reward, rewardRate)
pygame.time.set_timer(eatorbreed, 2000)
pygame.time.set_timer(nextgen, genTimer)

run = True
while run:
    foodList = [f for f in foodList if f.isConsumed == False]
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == foodSpawn:
            SpawnFood()
        if event.type == pulse:
            LearnPulse()
            lPulse = pygame.time.get_ticks()
        if event.type == reward:
            RewardForSurvival()
            lReward = pygame.time.get_ticks()
        if event.type == eatorbreed:
            EatEmUp()
            BreedEmUp()
            lEatBreed = pygame.time.get_ticks()
        if event.type == nextgen:
            NextGen()
            lNextGen = pygame.time.get_ticks()

    now = pygame.time.get_ticks()
    pulseVal = max(0, (pulseRate - (now - lPulse)) // 1000)
    eatVal = max(0, (2000 - (now - lEatBreed)) // 1000)
    rewardVal = max(0, (rewardRate - (now - lReward)) // 1000)
    genVal = max(0, (genTimer - (now - lNextGen)) // 1000)


    gen_text = font.render(f"Generation: {genCount}", True, (220,220,220))
    pulse_text = font.render(f"Next Learn Pulse: {pulseVal}s", True, (220,220,220))
    eat_text = font.render(f"Next Eat/Breed: {eatVal}s", True, (220,220,220))
    reward_text = font.render(f"Next Reward: {rewardVal}s", True, (220,220,220))
    nextgen_text = font.render(f"Next Generation: {genVal}s", True, (220,220,220))

    screen.fill((30, 30, 30))
    screen.blit(gen_text, (10, 10))
    screen.blit(pulse_text, (10, 40))
    screen.blit(eat_text, (10, 70))
    screen.blit(reward_text, (10, 100))
    screen.blit(nextgen_text, (10, 130))


    

    # Update animals
    for animal in animalList:
        if not animal.isAlive:
            continue
        MoveAnimal(animal)
        UpdateBoundaryDist(animal)
        UpdateDistances(animal)
        DecreaseSatiation(animal)
        ConsumeDatFood(animal)
        DecreaseFitness(animal)
        #keep at end, yea?
        UpdateDelta(animal)
        
        color = (200, 50, 50) if animal.isPredator else (50, 200, 50)

        pygame.draw.circle(
            screen,
            color,
            (int(animal.rect.x), int(animal.rect.y)),
            animalRad
        )

    # Draw food
    for food in foodList:
        pygame.draw.circle(
            screen,
            (240, 220, 50),
            (food.rect.x,food.rect.y),
            foodRad
        )

    pygame.display.flip()

pygame.quit()
