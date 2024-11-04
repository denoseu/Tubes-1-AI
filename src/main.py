from cube import MagicCube
from algomanager import AlgorithmManager
from simulated_annealing import SimulatedAnnealingStrategy

n = 5
magic_cube = MagicCube(n)
algorithm_manager = AlgorithmManager()
simulatedAnnealing = SimulatedAnnealingStrategy()

while True:
    print("Pilih Algoritma:")
    print("1. Steepest Ascent")
    print("2. Simulated Annealing")
    print("3. Genetic Algorithm")
    print("4. Exit")
    choice = int(input())

    if (choice == 1):
        algorithm_manager.setStrategy(simulatedAnnealing)
    if


