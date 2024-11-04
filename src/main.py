from cube import MagicCube
from algomanager import AlgorithmManager
from simulatedAnnealing import SimulatedAnnealingStrategy

n = 5
magic_cube = MagicCube(n)
algorithm_manager = AlgorithmManager()

print("Pilih Algoritma:")
print("1. Steepest Ascent")
print("2. Simulated Annealing")
print("3. Genetic Algorithm")
print("4. Exit")
choice = int(input())

while True:
    simulatedAnnealing = SimulatedAnnealingStrategy()
    if (choice == 1):
        algorithm_manager.setStrategy(simulatedAnnealing)
        algorithm_manager.solve(magic_cube)


