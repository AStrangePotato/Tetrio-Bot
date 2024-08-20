import random
import math
import time
import main
from lib import detect, move

weights = [
    -0.5000,   # aggregate
     1.0000,   # cleared
    -0.5000,   # bumpiness
    -3.0000,   # blockade
    -1.0000,   # other pieces in tetris well
    -0.5000    # i piece dependencies
]


mutation_rate = 0.1
population_size = 15

def mergeWeights(A, B):
    n = len(A)
    new = [0] * n
    for i in range(n):
        new[i] = (A[i] + B[i]) / 2
        if random.uniform(0, 1) < mutation_rate:
            new[i] += random.uniform(-1, 1)
    
    return new

def evolve(population):
    new_population = []
    for i in range(3):
        new_population.append(population[i])
    
    for i in range(population_size-3):
        parentA = math.floor(random.triangular(0, population_size-1, 5))
        parentB = math.floor(random.triangular(0, population_size-1, 5))

        child = mergeWeights(population[parentA], population[parentB])
        new_population.append(child)
    
    return new_population


def train_step(population):
    outcomes = [] #(fitness, weights)
    for agent in population:
        fitness = evaluate(agent)
        outcomes.append((fitness, agent))
    
    outcomes.sort()
    next_generation = evolve(x[1] for x in outcomes)

    return next_generation

def evaluate(weights):
    time.sleep(0.3)
    move.retry()
    main.play(duration=10, weights=weights)
    print(detect.get_VS())

evaluate(weights)