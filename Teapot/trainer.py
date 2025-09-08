import random
import numpy as np
from copy import deepcopy
from multiprocessing import Pool, cpu_count
from game import TetrisGame # Make sure your fixed TetrisGame class is in game.py
from lib import heuristic
from lib.constants import pieces

# --- GA Hyperparameters (Tuned for better performance) ---
SEED_WEIGHTS = [
    -1.030,  # aggregate height
    0.760,   # lines cleared
    -0.420,  # bumpiness
    -6.474,  # blockades
    -1.942,  # tetris well
    -2.420   # i piece dependencies
]

GENES = len(SEED_WEIGHTS)
POPULATION_SIZE = 100       # Increased for more exploration
GENERATIONS = 100           # Increased for a longer run
ELITE_COUNT = 10            # Keep more of the best performers
TOURNAMENT_SIZE = 8         # Slightly higher selection pressure
MUTATION_RATE = 0.2         # Base chance for a gene to mutate
MUTATION_SCALE = 0.5        # Max scale of mutation
IMMIGRANT_COUNT = 10        # Number of new individuals per generation
GAME_MOVES = 500            # Increased for deeper evaluation
GAME_TRIALS = 5             # Fewer trials but deeper games is often better

# --- Evaluation function ---
def evaluate(weights):
    """Plays several games with the given weights and returns the median score."""
    scores = []
    for _ in range(GAME_TRIALS):
        game = TetrisGame()
        # --- NEW: Pre-generate a long list of pieces for consistency ---
        # This ensures every evaluation uses the same piece sequences within a trial,
        # reducing noise and making fitness comparison more accurate.
        piece_sequence = [game.next_piece() for _ in range(GAME_MOVES)]

        for move_num, piece_name in enumerate(piece_sequence):
            if game.isGameOver():
                break

            piece = pieces[piece_name]
            best_move = [-float("inf"), -1, -1] # [score, rotation, position]

            # Find the best possible move for the current piece
            for rotation in range(len(piece)):
                max_pos = 10 - len(piece[rotation][0])
                for pos in range(max_pos + 1):
                    # Use a temporary board for simulation to avoid deepcopy overhead in loop
                    temp_board = deepcopy(game.board)
                    game.set_board(temp_board)
                    
                    # --- NEW: More robust drop logic ---
                    # Create a temporary game instance to simulate the move fully
                    sim_game = TetrisGame()
                    sim_game.set_board(deepcopy(game.board))
                    sim_game.drop(piece[rotation], pos)
                    
                    if not sim_game.isGameOver():
                        sim_game.clear_lines()
                        score = heuristic.analyze(sim_game.board, weights)
                        if score > best_move[0]:
                            best_move = [score, rotation, pos]
            
            # If no valid move was found (unlikely but possible), break
            if best_move[1] == -1:
                break
            
            # Perform the best move on the actual game board
            game.drop(piece[best_move[1]], best_move[2])
            game.clear_lines()

        scores.append(game.score)
    return np.median(scores)

# --- GA Operators ---
def create_individual():
    """Creates a new individual by adding noise to the seed weights."""
    return [w + random.uniform(-1, 1) for w in SEED_WEIGHTS]

def blend_crossover(parent1, parent2, alpha=0.5):
    """
    --- NEW: Blend Crossover (BLX-alpha) ---
    More effective for real-valued genes. Creates children in a range around parents.
    """
    child1, child2 = [], []
    for i in range(GENES):
        d = abs(parent1[i] - parent2[i])
        min_val = min(parent1[i], parent2[i]) - alpha * d
        max_val = max(parent1[i], parent2[i]) + alpha * d
        child1.append(random.uniform(min_val, max_val))
        child2.append(random.uniform(min_val, max_val))
    return child1, child2

def mutate(individual, generation, max_generations):
    """
    --- CHANGED: Adaptive Mutation ---
    Mutation scale decreases, but the rate stays constant. This allows for
    fine-tuning in late generations while still being able to escape local optima.
    """
    # The scale of mutation decreases over time
    current_scale = MUTATION_SCALE * (1 - generation / max_generations)**2
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] += random.gauss(0, current_scale)
    return individual

def tournament_selection(fitness, k):
    """Randomly select k individuals and return the best one."""
    selected_indices = np.random.choice(len(fitness), k, replace=False)
    tournament_contestants = [fitness[i] for i in selected_indices]
    return max(tournament_contestants, key=lambda x: x[1])[0]

def evaluate_population(population):
    """Evaluates the entire population in parallel."""
    # Using cpu_count() to maximize utilization on your Ultra 9
    with Pool(processes=12) as pool:
        scores = pool.map(evaluate, population)
    return list(zip(population, scores))

# --- Main GA loop ---
def evolve():
    """The main function to run the genetic algorithm."""
    # Initialize population around seed weights
    population = [create_individual() for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        fitness = evaluate_population(population)
        fitness.sort(key=lambda x: x[1], reverse=True)

        best_individual = fitness[0]
        avg_score = np.mean([f[1] for f in fitness])
        
        # --- CHANGED: More informative printout ---
        weights_str = ", ".join([f"{w:.3f}" for w in best_individual[0]])
        print(
            f"Gen {generation+1}/{GENERATIONS} | "
            f"Best Score: {best_individual[1]:,.0f} | "
            f"Avg Score: {avg_score:,.0f} | "
            f"Best Weights: [{weights_str}]"
        )

        # Start building the next generation
        new_population = []
        
        # 1. Elitism: Keep the best individuals
        new_population.extend([deepcopy(fitness[i][0]) for i in range(ELITE_COUNT)])

        # 2. Immigration: Add fresh, random individuals to maintain diversity
        new_population.extend([create_individual() for _ in range(IMMIGRANT_COUNT)])

        # 3. Crossover & Mutation: Fill the rest of the population
        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(fitness, TOURNAMENT_SIZE)
            parent2 = tournament_selection(fitness, TOURNAMENT_SIZE)
            
            child1, child2 = blend_crossover(parent1, parent2)
            
            new_population.append(mutate(child1, generation, GENERATIONS))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child2, generation, GENERATIONS))

        population = new_population

    # --- Final evaluation of the last generation ---
    print("\n--- Final Evaluation ---")
    fitness = evaluate_population(population)
    best_weights, best_score = max(fitness, key=lambda x: x[1])
    
    weights_str = ", ".join([f"{w:.4f}" for w in best_weights])
    print(f"Best final score: {best_score:,.0f}")
    print(f"Best final weights: [{weights_str}]")
    
    return best_weights

if __name__ == "__main__":
    evolve()