import random
import math
from PIL import Image
import numpy as np
import time

from . import detect

weights = [
    -0.530213,   # aggregate
     0.760667,   # increase tetris score after mvp
    -10.4,       # hole (replaced by blockade)
    -0.420690,   # bumpiness
    -30.474278,  # blockade
    -2.042069,   # tetris well
    -0.420420    # i piece dependencies
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

