import numpy as np
import random

from strategy import AlgorithmStrategy
from cube import MagicCube

class GeneticAlgorithm(AlgorithmStrategy):
    def execute(self, magic_cube, population_size, generations, mutation_rate, n):
        population = [MagicCube(n) for _ in range(population_size)]
        best_individual = None
        best_fitness = float('-inf')
        iterations = []

        for generation in range(generations):
            sumofObjectiveFunctions = self._getSumOfObjectiveFunctions(population)
            fitness_scores = [(abs(cube.getCurrentScore()) / sumofObjectiveFunctions) for cube in population]
            print(f"Fitness scores: {fitness_scores}")

            # Find best individual in current generation
            current_best_fitness = max(fitness_scores)
            current_best_individual = population[np.argmax(fitness_scores)]

            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual.cube.copy()

            new_population = []
            for _ in range(population_size // 2):  # Generate population pairs
                parent1 = self._roulette_wheel_selection(population, fitness_scores)
                parent2 = self._roulette_wheel_selection(population, fitness_scores)
                
                child1, child2 = self._ordered_crossover(parent1, parent2)

                # Apply mutation to the offspring
                self._mutation(child1, mutation_rate)
                self._mutation(child2, mutation_rate)

                new_population.extend([child1, child2])

            population = new_population

    def _getSumOfObjectiveFunctions(self, population):
        scores = [cube.getCurrentScore() for cube in population]
        return abs(sum(scores))

    def _roulette_wheel_selection(self, population, fitness_scores):
        selected_idx = np.random.choice(len(population), p=fitness_scores)
        return population[selected_idx]
    
    def _ordered_crossover(self, parent1, parent2):
        n = parent1.n

        # Convert to 1D array
        parent1_flatten = parent1.cube.flatten()
        parent2_flatten = parent2.cube.flatten()

        crossover_start = random.randint(0, len(parent1_flatten) - 2)
        crossover_end = random.randint(crossover_start + 1, len(parent1_flatten) - 1)

        child1_flatten = [-1] * len(parent1_flatten)
        child2_flatten = [-1] * len(parent2_flatten)

        child1_flatten[crossover_start:crossover_end] = parent1_flatten[crossover_start:crossover_end]
        child2_flatten[crossover_start:crossover_end] = parent2_flatten[crossover_start:crossover_end]

        self._fill_remaining_values(child1_flatten, parent2_flatten, crossover_end)
        self._fill_remaining_values(child2_flatten, parent1_flatten, crossover_end)

        child1_cube = np.array(child1_flatten).reshape((n, n, n))
        child2_cube = np.array(child2_flatten).reshape((n, n, n))

        child1 = MagicCube(n)
        child2 = MagicCube(n)
        child1.cube = child1_cube
        child2.cube = child2_cube

        child1.initialize_sums()
        child2.initialize_sums()
        
        return child1, child2

    def _fill_remaining_values(self, child, source, pos):
        for gene in source:
            if gene not in child:
                if pos == len(child) - 1:
                    pos = 0  # Wrap around to the beginning if we reach the end
                
                while child[pos] != -1:  # Find the next empty position
                    pos += 1
                child[pos] = gene

    def _mutation(self, child, mutation_rate):
        
        child_flatten = child.cube.flatten()

        for i in range(len(child_flatten)):
            if random.random() < mutation_rate:
                # Choose a random index to swap with
                swap_idx = random.randint(0, len(child_flatten) - 1)
                # Swap genes
                child_flatten[i], child_flatten[swap_idx] = child_flatten[swap_idx], child_flatten[i]

        # Reshape back to cube form after mutation
        child.cube = np.array(child_flatten).reshape(child.n, child.n, child.n)
        child.initialize_sums()
