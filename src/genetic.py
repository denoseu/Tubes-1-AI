import numpy as np
import random

from strategy import AlgorithmStrategy
from cube import MagicCube

class GeneticAlgorithm(AlgorithmStrategy):
    def execute(self, magic_cube, population_size, generations,n):
        population = [MagicCube(n) for _ in range(population_size)]
        best_individual = None
        best_fitness= float('-inf')
        best_obj_function = float('-inf')
        iterations = []
        scores = []
        avg_fitness = []

        for i in range(generations):
            sumofObjectiveFunctions = self._getSumOfObjectiveFunctions(population)
            fitness_scores = self._get_fitness_array(population)
            
            # Find best individual in current generation
            current_best_fitness = max(fitness_scores)
            current_best_individual = population[np.argmax(fitness_scores)]
            iterations.append((current_best_individual.cube.copy(), current_best_individual.getCurrentScore(),current_best_fitness))

            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual.cube.copy()
                best_obj_function = current_best_individual.getCurrentScore()

            scores.append(best_fitness)
            avg_fitness.append(np.mean(fitness_scores))

            new_population = []
            for _ in range(population_size // 2):
                parent1 = self._roulette_wheel_selection(population, fitness_scores)
                parent2 = self._roulette_wheel_selection(population, fitness_scores)
                child1,child2 = self._ordered_crossover(parent1,parent2)

                self._mutate(child1)
                self._mutate(child2)

                new_population.extend([child1,child2])
            population = new_population
        
         # Final results
        print("\nFinal Results:")
        print(f"Best Individual Fitness: {best_fitness}")
        print(f"Best Obj Function {best_obj_function}")
        print("Iterations (Best Individual, Fitness):")
        for i, (ind,obj, fit) in enumerate(iterations):
            print(f"Iteration {i + 1}: OBJ = {obj} Fitness = {fit}")

        return best_individual,best_fitness,iterations


    def _getSumOfObjectiveFunctions(self,population):
        scores = [cube.getCurrentScore() for cube in population]
        return abs(sum(scores))


    def _roulette_wheel_selection(self,population, fitness_scores):
        selected_idx = np.random.choice(len(population), p=fitness_scores)
        return population[selected_idx]
    
    def _ordered_crossover(self,parent1,parent2):
        n = parent1.n

        # ubah jdi 1d array
        parent1_flatten = parent1.cube.flatten()
        parent2_flatten = parent2.cube.flatten()

        crossover_start = random.randint(0, len(parent1_flatten) - 2)
        crossover_end = random.randint(crossover_start + 1, len(parent1_flatten) - 1)

        #placeholder tracker mana yg blom diisi
        child1_flatten = [-1] * len(parent1_flatten)
        child2_flatten = [-1] * len(parent2_flatten)

        child1_flatten[crossover_start:crossover_end] = parent1_flatten[crossover_start:crossover_end]
        child2_flatten[crossover_start:crossover_end] = parent2_flatten[crossover_start:crossover_end]


        self._fill_remaining_values(child1_flatten, parent2_flatten,0)
        self._fill_remaining_values(child2_flatten, parent1_flatten,0)


        child1_cube = np.array(child1_flatten).reshape((n, n, n))
        child2_cube = np.array(child2_flatten).reshape((n, n, n))

        child1 = MagicCube(n)
        child2 = MagicCube(n)
        child1.cube = child1_cube
        child2.cube = child2_cube

        child1.initialize_sums()
        child2.initialize_sums()
        child1.update_position_map()
        child2.update_position_map()
        
        return child1,child2

    def _fill_remaining_values(self,child,source,pos):
        for gene in source:
            if gene not in child:
                while child[pos] != -1: 
                    pos += 1
                child[pos] = gene

    def _mutate(self, cube):
        if random.random() < 0.3:
            num1 = random.randint(1, 125)
            num2 = random.randint(1, 125)
            while num2 == num1:
                num2 = random.randint(1, 125)

            cube.swap_number(num1, num2)

    def _get_fitness_array(self, population):

        sum_total = sum(abs(cube.getCurrentScore()) for cube in population)

        

        real_fitness = [sum_total + cube.getCurrentScore() for cube in population]
        fitness_total = sum(real_fitness)

        return [x/fitness_total for x in real_fitness]




        