import random
import math
from game import TetrisGame
from lib import heuristic
import copy

mutation_rate = 0.2 # %
learning_rate = 0.1 # %
rollout_duration = 7 #seconds
population_size = 10 #agents

def mergeWeights(A, B):
    n = len(A)
    new = [0] * n
    for i in range(n):
        new[i] = (A[i] + B[i]) / 2
        if random.uniform(0, 1) < mutation_rate:
            new[i] += random.uniform(-1, 1) * learning_rate
    
    return new

def evolve(population):
    new_population = [population[0]]

    for i in range(population_size-1):
        parentA = math.floor(random.triangular(0, population_size-1, 3))
        parentB = math.floor(random.triangular(0, population_size-1, 3))

        child = mergeWeights(population[parentA], population[parentB])
        new_population.append(child)
    
    return new_population


def train_step(population):
    outcomes = [] #(fitness, weights)
    for agent in population:
        fitness = evaluate(agent)
        outcomes.append((fitness, agent))
    
    outcomes.sort(reverse=True)

    next_generation = evolve([x[1] for x in outcomes])

    return next_generation, outcomes[0]



def evaluate(weights):
    game = TetrisGame()

    for move in range(100): #each bot gets 100 pieces
        piece = game.next_piece()

        best = [-float("inf"), -1, -1] 

        for rotation in range(len(piece)):
            maxPos = 11 - len(piece[rotation][0])
            for pos in range(maxPos):
                boardSnapshot = copy.deepcopy(boardMaster) #new instance
                simulBoard = drop(piece[rotation], pos, boardSnapshot)
                score = heuristic.analyze(simulBoard, weights)

                if score > best[0]:
                    best = [score, rotation, pos]

                simulBoard = boardSnapshot #revert instance


    return game.score #sent lines 


def train(weights, epochs=50):
    population = evolve([weights for i in range(population_size)]) #initial pop

    for i in range(epochs):
        new_population, king = train_step(population)
        population = new_population

    return population


print(train([-0.6040088729980074, 1.2977144824191589, -0.5363367336570115, -2.8855510684311336, -0.9059300856666658, -0.2442835269184844]))