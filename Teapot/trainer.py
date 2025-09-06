import random
import numpy as np
from copy import deepcopy
from multiprocessing import Pool, cpu_count
from game import TetrisGame
from lib import heuristic
from lib.constants import pieces

# Known good weights (seed)
SEED_WEIGHTS = [
    -1.030,   # aggregate
     0.760,   # increase tetris score after mvp
    -0.420,   # bumpiness
    -6.474,  # blockade
    -1.942,  # tetris well
    -2.420   # i piece dependencies
]

GENES = len(SEED_WEIGHTS)
POPULATION_SIZE = 30
GENERATIONS = 50
ELITE_COUNT = 2
TOURNAMENT_SIZE = 5
BASE_MUTATION_RATE = 0.3
BASE_MUTATION_SCALE = 1.5

# --- Evaluation function (unchanged) ---
def evaluate(weights):
    scores = []
    for trial in range(10):
        game = TetrisGame()
        for move in range(100):
            piece = pieces[game.next_piece()]
            best = [-float("inf"), -1, -1]
            for rotation in range(len(piece)):
                maxPos = 11 - len(piece[rotation][0])
                for pos in range(maxPos):
                    boardSnapshot = deepcopy(game.board)
                    game.drop(piece[rotation], pos)
                    score = heuristic.analyze(game.board, weights)
                    if score > best[0]:
                        best = [score, rotation, pos]
                    game.set_board(boardSnapshot)
            game.drop(piece[best[1]], best[2])
            game.clear_lines()
            if game.isGameOver():
                break
        scores.append(game.score)
    return np.median(scores)

# --- GA functions ---
def create_individual():
    # Random small variation around seed weights
    return [w + random.gauss(0, 0.5) for w in SEED_WEIGHTS]

def mutate(individual, generation, max_generations):
    # Mutation probability decays over generations
    mutation_rate = BASE_MUTATION_RATE * (1 - generation / max_generations)
    mutation_scale = BASE_MUTATION_SCALE * (1 - generation / max_generations)
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] += random.gauss(0, mutation_scale)
    return individual

def crossover(parent1, parent2):
    point = random.randint(1, GENES - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

def tournament_selection(fitness, k):
    # Randomly choose k individuals and pick the best
    selected = random.sample(fitness, k)
    return max(selected, key=lambda x: x[1])[0]

def evaluate_population(population):
    with Pool(cpu_count()) as pool:
        scores = pool.map(evaluate, population)
    return list(zip(population, scores))

# --- Main GA loop ---
def evolve():
    # Initialize population around seed weights
    population = [create_individual() for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        fitness = evaluate_population(population)
        fitness.sort(key=lambda x: x[1], reverse=True)
        print(f"Gen {generation}: Best score = {fitness[0][1]:.2f}, Weights = {fitness[0][0]}")

        # Elitism: carry top performers
        new_population = [deepcopy(fitness[i][0]) for i in range(ELITE_COUNT)]

        # Fill the rest using tournament selection, crossover, and mutation
        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(fitness, TOURNAMENT_SIZE)
            parent2 = tournament_selection(fitness, TOURNAMENT_SIZE)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, generation, GENERATIONS))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child2, generation, GENERATIONS))

        population = new_population

    # Final evaluation
    fitness = evaluate_population(population)
    best_weights = max(fitness, key=lambda x: x[1])
    print("Best final weights:", best_weights[0])
    print("Best final score:", best_weights[1])
    return best_weights[0]

if __name__ == "__main__":
    evolve()
