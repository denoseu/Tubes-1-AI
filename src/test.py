import numpy as np
from genetic import GeneticAlgorithm  # Adjust this import based on your file structure
from cube import MagicCube  # Assuming MagicCube is implemented and imported correctly

# Define parameters
population_size = 10        # Set the size of the population
generations = 10         # Set the number of generations to evolve
mutation_rate = 0.1         # Set the mutation rate
n = 5                       # Size of the magic cube (for example, a 5x5x5 cube)

# Create an instance of the GeneticAlgorithm class
genetic_algorithm = GeneticAlgorithm()

# Initialize a MagicCube (initial cube setup, if needed)
initial_magic_cube = MagicCube(n)

# Run the genetic algorithm
genetic_algorithm.execute(initial_magic_cube, population_size, generations, n)
