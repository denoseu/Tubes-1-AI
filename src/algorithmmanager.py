from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import random
import math
import time
import os
from cube import MagicCube
from animation import AnimationManager
from plot import PlotManager

class AlgorithmManager:

    def solve(self, magic_cube, algorithm="steepest_ascent_parallel", **kwargs):
        if algorithm == "steepest_ascent":
            return self.steepest_ascent_parallel(magic_cube)
        elif algorithm == "hill_climbing_with_sideways":
            return self.hill_climbing_with_sideways(magic_cube, 30)
        elif algorithm == "random_restart_hill_climbing":
            return self.random_restart_hill_climbing(magic_cube, **kwargs)
        elif algorithm == "simulated_annealing":
            initial_temp = kwargs.get("initial_temp", 1000)
            cooling_rate = kwargs.get("cooling_rate", 0.9999) 
            return self.simulated_annealing(magic_cube, initial_temp, cooling_rate)
        elif algorithm == "stochastic_hill_climbing":
            return self.stochastic_hill_climbing(magic_cube, **kwargs)
        elif algorithm == "genetic":
            population_size = kwargs.get("population_size", 200)
            generations = kwargs.get("generations", 100)
            mutation_rate = kwargs.get("mutation_rate", 0.3)
            return self.genetic_algorithm(magic_cube, population_size, generations, mutation_rate)
        else:
            raise ValueError("Invalid algorithm specified")
    
    def simulated_annealing(self, cube, initial_temp, cooling_rate):
        current_score = cube.getCurrentScore()
        temperature = initial_temp
        iterations = []

        scores = [current_score]
        acceptance_probs = [] 

        iteration = 0
        while temperature > 1e-3:
            iteration += 1
            # Choose two random positions for swapping
            pos1 = tuple(np.unravel_index(np.random.randint(0, cube.n**3), (cube.n, cube.n, cube.n)))
            pos2 = tuple(np.unravel_index(np.random.randint(0, cube.n**3), (cube.n, cube.n, cube.n)))

            # Swap elements and calculate new score
            cube.swap_elements(pos1, pos2)
            new_score = cube.getCurrentScore()
            delta_score = new_score - current_score

            if delta_score > 0:
                accepted = True
            else:
                acceptance_probability = math.exp(delta_score / temperature)
                acceptance_probs.append(acceptance_probability)
                accepted = np.random.rand() < acceptance_probability
            
            # If accepted, update the current score; otherwise, revert the swap
            if accepted:
                current_score = new_score
            else:
                cube.swap_elements(pos1, pos2)  # Revert swap if not accepted

            temperature *= cooling_rate

            scores.append(current_score)

            iterations.append((cube.cube.copy(),current_score))
           
            ## KALAU BUTUH DATA BUAT VISUALISASI TARUH SINI
            # print(f"Iter {iteration} | Temp: {temperature:.5f} | Pos1: {pos1} <-> Pos2: {pos2} | Current Score: {current_score} | Delta: {delta_score}")

        print(f"Final Score: {current_score}")
        print(f"Final Cube:\n{cube.cube}")

        plot_manager = PlotManager(scores, acceptance_probs)
        plot_manager.plot_simulated_annealing()
        
        return cube.cube, current_score,iterations
    
    def steepest_ascent_parallel(self, cube, plot=True):
        current_score = cube.getCurrentScore()
        improved = True
        iterations = []
        scores = []

        print(cube.cube)

        while improved:
            improved = False
            best_score = current_score
            best_positions = None

            with ThreadPoolExecutor(8) as executor:
                futures = []
                for i in range(1, cube.n**3):
                    for j in range(i + 1, cube.n**3):
                        pos1 = cube.get_position(i)
                        pos2 = cube.get_position(j)

                        # Submit swap evaluations to the thread pool
                        futures.append(executor.submit(cube.evaluate_swap, pos1, pos2))

                for future in as_completed(futures):
                    swap_score, pos1, pos2 = future.result()
                    if swap_score > best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)

            if best_positions:
                pos1, pos2 = best_positions
                cube.swap_elements(pos1, pos2)
                current_score = best_score
                improved = True
                scores.append(current_score) 
                
            iterations.append((cube.cube.copy(), current_score))

        if plot:
            plot_manager = PlotManager(scores)
            plot_manager.plot_objective_function()
        
        return cube.cube, current_score, iterations

    
    def hill_climbing_with_sideways(self, cube, max_sideways):
        current_score = cube.getCurrentScore()
        improved = True
        sideways_moves = 0 
        scores = [current_score] 
        iterations = []

        while improved:
            improved = False
            best_score = current_score
            best_positions = None
            found_better = False  # udah ketemu solusi lebih bagus

            with ThreadPoolExecutor(os.cpu_count()) as executor:
                futures = []
                for i in range(1, cube.n**3):
                    for j in range(i + 1, cube.n**3):
                        pos1 = cube.get_position(i)
                        pos2 = cube.get_position(j)
                        futures.append(executor.submit(cube.evaluate_swap, pos1, pos2))

                for future in as_completed(futures):
                    swap_score, pos1, pos2 = future.result()
                    if swap_score > best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)
                        found_better = True
                        sideways_moves = 0  # reset sideway count kalau next nya better
                    elif swap_score == best_score and not found_better:
                        best_positions = (pos1, pos2)
            
            if best_positions:
                pos1, pos2 = best_positions
                cube.swap_elements(pos1, pos2)
                current_score = best_score
                scores.append(current_score)
                
                if found_better:
                    improved = True
                elif sideways_moves < max_sideways:
                    sideways_moves += 1
                    improved = True
                else:
                    improved = False  # stop kalau sudah smpai max_sideways
            iterations.append((cube.cube.copy(), current_score))

        plot_manager = PlotManager(scores)
        plot_manager.plot_objective_function()

        return cube, current_score, iterations
     
    def random_restart_hill_climbing(self, magic_cube, max_restarts=2):
        best_score = float("-inf")
        best_cube = None
        all_scores = []

        for _ in range(max_restarts):
            magic_cube.initialize_cube(magic_cube.n)
            magic_cube.initialize_sums()

            _, current_score, iterations = self.steepest_ascent_parallel(magic_cube, plot=False)
            
            restart_scores = [score for _, score in iterations]
            all_scores.append(restart_scores)
            
            if current_score > best_score:
                best_score = current_score
                best_cube = magic_cube.cube.copy()

        plot_manager = PlotManager()
        plot_manager.plot_multiple_objective_functions(all_scores) # Plot all scores for each restart

        return best_cube, best_score

    def steepest_ascent(self, magic_cube, max_steps=100):
        current_score = magic_cube.getCurrentScore()
        steps = 0
        improved = True

        while improved and steps < max_steps:
            improved = False
            best_score = current_score
            best_positions = None
            steps += 1

            for i in range(1, magic_cube.n**3):
                for j in range(i + 1, magic_cube.n**3):
                    pos1 = magic_cube.get_position(i)
                    pos2 = magic_cube.get_position(j)

                    magic_cube.swap_elements(pos1, pos2)
                    swap_score = magic_cube.getCurrentScore()

                    if swap_score > best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)

                    # Revert swap
                    magic_cube.swap_elements(pos1, pos2)

            if best_positions:
                pos1, pos2 = best_positions
                magic_cube.swap_elements(pos1, pos2)
                current_score = best_score
                improved = True

        return current_score

    def stochastic_hill_climbing(cube, magic_cube, max_steps=100):
        current_score = magic_cube.getCurrentScore()
        steps = 0
        scores = [current_score]

        iterations = []
        while steps < max_steps:
            steps += 1
            # Choose two random positions to swap
            pos1 = tuple(np.unravel_index(np.random.randint(0, magic_cube.n**3), (magic_cube.n, magic_cube.n, magic_cube.n)))
            pos2 = tuple(np.unravel_index(np.random.randint(0, magic_cube.n**3), (magic_cube.n, magic_cube.n, magic_cube.n)))

            magic_cube.swap_elements(pos1, pos2)
            new_score = magic_cube.getCurrentScore()

            # If the swap improves the score, accept it; otherwise, revert it
            if new_score > current_score:
                current_score = new_score
            else:
                magic_cube.swap_elements(pos1, pos2)  # Revert swap
            
            iterations.append((magic_cube.cube.copy(),current_score))

            print(f"Step {steps} | Pos1: {pos1} <-> Pos2: {pos2} | Current Score: {current_score}")

            scores.append(current_score)

        plot_manager = PlotManager(scores)
        plot_manager.plot_objective_function()

        return magic_cube.cube, current_score, iterations

    def genetic_algorithm(self, magic_cube, population_size, generations, mutation_rate):
        # Initialize population
        population = [MagicCube(magic_cube.n) for _ in range(population_size)]
        best_individual = None
        best_fitness = float('-inf')
        iterations = []
        scores = []
        avg_fitness = []

        for generation in range(generations):
            # Calculate fitness scores for the population
            fitness_scores = [cube.getCurrentScore() for cube in population]
            
            # Find best individual in current generation
            current_best_fitness = max(fitness_scores)
            current_best_individual = population[np.argmax(fitness_scores)]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual.cube.copy()
                iterations.append((best_individual.copy(), best_fitness))
            
            scores.append(best_fitness)
            avg_fitness.append(np.mean(fitness_scores))
            print(f"Generation {generation + 1}, Best fitness: {best_fitness}")
            
            # Create new population through selection and reproduction
            new_population = []
            for _ in range(population_size // 2):
                parent1 = self._roulette_wheel_selection(population, fitness_scores)
                parent2 = self._roulette_wheel_selection(population, fitness_scores)
                
                child1, child2 = self._crossover(parent1, parent2)
                
                # Perform mutation
                self._mutate(child1, mutation_rate)
                self._mutate(child2, mutation_rate)
                
                new_population.extend([child1, child2])
            
            population = new_population

        plot_manager = PlotManager(scores)
        # plot_manager.plot_objective_function()
        plot_manager.plot_genetic_algorithm(scores, avg_fitness)
        
        return best_individual, best_fitness, iterations

    def _roulette_wheel_selection(self, population, fitness_scores):
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            return random.choice(population)
        
        probabilities = [score / total_fitness for score in fitness_scores]
        selected_idx = np.random.choice(len(population), p=probabilities)
        
        # Create a new MagicCube instance with the selected cube configuration
        selected_cube = MagicCube(population[0].n)
        selected_cube.cube = population[selected_idx].cube.copy()
        selected_cube.initialize_sums()
        return selected_cube

    def _crossover(self, parent1, parent2):
        n = parent1.n
        crossover_point = random.randint(1, n-1)
        
        # Create new MagicCube instances for children
        child1 = MagicCube(n)
        child2 = MagicCube(n)
        
        # Perform crossover
        child1.cube = np.zeros_like(parent1.cube)
        child2.cube = np.zeros_like(parent2.cube)
        
        child1.cube[:crossover_point, :, :] = parent1.cube[:crossover_point, :, :]
        child1.cube[crossover_point:, :, :] = parent2.cube[crossover_point:, :, :]
        
        child2.cube[:crossover_point, :, :] = parent2.cube[:crossover_point, :, :]
        child2.cube[crossover_point:, :, :] = parent1.cube[crossover_point:, :, :]
        
        # Initialize sums for the new cubes
        child1.initialize_sums()
        child2.initialize_sums()
        
        return child1, child2

    def _mutate(self, cube, mutation_rate):
        if random.random() < mutation_rate:
            pos1 = tuple(np.random.randint(cube.n, size=3))
            pos2 = tuple(np.random.randint(cube.n, size=3))
            cube.swap_elements(pos1, pos2)

    def evaluate_swap(self, magic_cube, pos1, pos2):
        magic_cube.swap_elements(pos1, pos2)
        score = magic_cube.getCurrentScore()
        magic_cube.swap_elements(pos1, pos2)
        return score, pos1, pos2


# Instantiate MagicCube and run parallelized steepest ascent
n = 5
magic_cube = MagicCube(n)
algorithm_manager = AlgorithmManager()
start_time = time.time()
final_cube, final_score,iterations = algorithm_manager.solve(magic_cube,"genetic")
end_time = time.time()


print('Starting Animation')
print(f'Iteration length {len(iterations)}')
animation_manager = AnimationManager(5,iterations)
animation_manager.start_animation()

# print(f"Final Cube:\n{final_cube}")
# print(f"Final Score: {final_score}")
# print(f"Elapsed time: {end_time - start_time:.2f} seconds")



