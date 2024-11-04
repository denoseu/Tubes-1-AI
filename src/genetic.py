import numpy as np
import random

from strategy import AlgorithmStrategy
from cube import MagicCube

class GeneticAlgorithm(AlgorithmStrategy):
    def execute(self, cube, ):
        return super().execute(magic_cube, **kwargs)

    def fitness(cube, magic_number):
        pass

    def roulette_wheel_selection(population, fitness_scores):
        total_fitness = np.sum(fitness_scores)
        probabilities = [score / total_fitness for score in fitness_scores]
        selected_idx = np.random.choice(len(population), p=probabilities)
        return population[selected_idx]
    