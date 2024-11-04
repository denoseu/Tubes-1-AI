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

    while True:
        print("\nPilih Algoritma:")
        print("1. Steepest Ascent Hill Climbing")
        print("2. Sideways Move Hill Climbing")
        print("3. Random Restart Hill Climbing")
        print("4. Stochastic Hill Climbing")
        print("5. Simulated Annealing")
        print("6. Genetic Algorithm")
        print("7. Exit")

        try:
            choice = int(input("Masukkan pilihan (1-7): "))
            if 1 <= choice <= 7:
                break
            else:
                print("Input tidak valid. Masukkan nomor dari 1 sampai 7.")
        except ValueError:
            print("Input tidak valid. Masukkan nomor dari 1 sampai 7.")

    # Prepare algorithm and kwargs based on choice
    kwargs = {}  # Default kwargs as empty
    if choice == 1:
        algorithm_manager.setStrategy(steepestAscent)
    elif choice == 2:
        algorithm_manager.setStrategy(sideways)
    elif choice == 3:
        algorithm_manager.setStrategy(random_restart)
    elif choice == 4:
        algorithm_manager.setStrategy(stochastic)
    elif choice == 5:
        algorithm_manager.setStrategy(simulatedAnnealing)
    elif choice == 6:
        algorithm_manager.setStrategy(genetic)
        population_size = int(input("Masukkan jumlah populasi awal: "))
        generations = int(input("Masukkan banyak iterasi: "))
        kwargs = {"population_size": population_size, "n": n, "generations": generations}
    elif choice == 7:
        print("Exiting program.")
        break

    

    # Run the selected algorithm
    start_time = time.time()
    final_cube, final_score, iterations = algorithm_manager.solve(magic_cube, **kwargs)
    end_time = time.time()

    # Display cube state
    display_manager = CubeDisplayManager(initial_cube, final_cube)
    display_manager.start()

    # Video player animation
    animation_manager = AnimationManager(n, iterations)
    animation_manager.start_animation()

    # Ask if the user wants to replay
    while True:
        replay_experiment = input("Apakah Anda ingin melakukan eksperimen ulang (y atau n): ").strip().lower()
        if replay_experiment == "y":
            break  # Restart the algorithm selection
        elif replay_experiment == "n":
            print("Eksperimen selesai.")
            exit()
        else:
            print("Input tidak valid. Masukkan 'y' atau 'n'.")
