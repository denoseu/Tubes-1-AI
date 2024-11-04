from cube import MagicCube
from algomanager import AlgorithmManager
from simulated_annealing import SimulatedAnnealingStrategy
from steepest_asscent import SteepestAscentStrategy
from sideways import SidewaysStrategy
from random_restart import RandomRestartStrategy
from stochastic import StochasticStrategy
from simulated_annealing import SimulatedAnnealingStrategy

n = 5
magic_cube = MagicCube(n)
algorithm_manager = AlgorithmManager()
simulatedAnnealing = SimulatedAnnealingStrategy()
sideways = SidewaysStrategy()
steepestAscent = SteepestAscentStrategy()
random_restart = RandomRestartStrategy()
stochastic = StochasticStrategy()

while True:
    print("Pilih Algoritma:")
    print("1. Steepest Ascent Hill Climbing")
    print("2. Sideways Move Hill Climbing")
    print("3. Random Restart Hill Climbing")
    print("4. Stochastic Hill Climbing")
    print("5. Simulated Annealing")
    print("6. Genetic Algorithm")
    print("7. Exit")
    choice = int(input())

    if (choice == 1):
        algorithm_manager.setStrategy(steepestAscent)
    if (choice == 2):
        algorithm_manager.setStrategy(sideways)
    if (choice == 3):
        algorithm_manager.setStrategy(random_restart)
    if (choice == 4):
        algorithm_manager.setStrategy(stochastic)
    if (choice == 5):
        algorithm_manager.setStrategy(simulatedAnnealing)
        final_cube, final_scsore, iterations = algorithm_manager.solve(magic_cube)
    if (choice == 6):
        pass
    if (choice == 7):
        break

    while True:
        replay_experiment = input("Apakah Anda ingin melakukan eksperimen ulang (y or n): ").strip().lower()
        if replay_experiment in ["y", "n"]:
            start = False
            break
        else:
            print("Input tidak valid. Masukkan 'y' atau 'n'.")


