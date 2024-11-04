from cube import MagicCube
from algomanager import AlgorithmManager
from Algorithms.simulated_annealing import SimulatedAnnealingStrategy
from Algorithms.steepest_asscent import SteepestAscentStrategy
from Algorithms.sideways import SidewaysStrategy
from Algorithms.random_restart import RandomRestartStrategy
from Algorithms.stochastic import StochasticStrategy
from Algorithms.genetic import GeneticAlgorithm
from display_cube import CubeDisplayManager
from animation import AnimationManager
import time

def get_valid_input(prompt, valid_range):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_range:
                return choice
            else:
                print(f"Input tidak valid. Masukkan nomor dari {valid_range.start} sampai {valid_range.stop - 1}.")
        except ValueError:
            print("Input tidak valid. Masukkan nomor dari {valid_range.start} sampai {valid_range.stop - 1}.")

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Input tidak valid. Harap masukkan angka positif.")
        except ValueError:
            print("Input tidak valid. Harap masukkan angka positif.")

n = 5
algorithm_manager = AlgorithmManager()
simulatedAnnealing = SimulatedAnnealingStrategy()
sideways = SidewaysStrategy()
steepestAscent = SteepestAscentStrategy()
random_restart = RandomRestartStrategy()
stochastic = StochasticStrategy()
genetic = GeneticAlgorithm()

while True:
    magic_cube = MagicCube(n)
    initial_cube = magic_cube.cube.copy()

    print("\nPilih Algoritma:")
    print("1. Steepest Ascent Hill Climbing")
    print("2. Sideways Move Hill Climbing")
    print("3. Random Restart Hill Climbing")
    print("4. Stochastic Hill Climbing")
    print("5. Simulated Annealing")
    print("6. Genetic Algorithm")
    print("7. Exit")

    choice = get_valid_input("Masukkan pilihan (1-7): ", range(1, 8))

    kwargs = {}
    if choice == 1:
        algorithm_manager.setStrategy(steepestAscent)
    elif choice == 2:
        algorithm_manager.setStrategy(sideways)
        max_sideways = get_positive_integer("Masukkan jumlah gerakan samping maksimum: ")
        kwargs = {"max_sideways": max_sideways}
    elif choice == 3:
        algorithm_manager.setStrategy(random_restart)
        max_restarts = get_positive_integer("Masukkan jumlah restart: ")
        kwargs = {"max_restarts": max_restarts}
    elif choice == 4:
        algorithm_manager.setStrategy(stochastic)
    elif choice == 5:
        algorithm_manager.setStrategy(simulatedAnnealing)
    elif choice == 6:
        algorithm_manager.setStrategy(genetic)
        population_size = get_positive_integer("Masukkan jumlah populasi awal: ")
        generations = get_positive_integer("Masukkan banyak iterasi: ")
        kwargs = {"population_size": population_size, "n": n, "generations": generations}
    elif choice == 7:
        print("Exiting program.")
        break

    start_time = time.time()
    final_cube, final_score, iterations = algorithm_manager.solve(magic_cube, **kwargs)
    end_time = time.time()

    display_manager = CubeDisplayManager(initial_cube, final_cube)
    display_manager.start()

    animation_manager = AnimationManager(n, iterations)
    animation_manager.start_animation()

    while True:
        replay_experiment = input("Apakah Anda ingin melakukan eksperimen ulang (y atau n): ").strip().lower()
        if replay_experiment == "y":
            break
        elif replay_experiment == "n":
            print("Eksperimen selesai.")
            exit()
        else:
            print("Input tidak valid. Masukkan 'y' atau 'n'.")
