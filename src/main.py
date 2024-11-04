from cube import MagicCube
from algomanager import AlgorithmManager
from simulated_annealing import SimulatedAnnealingStrategy
from steepest_asscent import SteepestAscentStrategy
from sideways import SidewaysStrategy
from random_restart import RandomRestartStrategy
from stochastic import StochasticStrategy
from genetic import GeneticAlgorithm
import time

n = 5
magic_cube = MagicCube(n)
algorithm_manager = AlgorithmManager()
simulatedAnnealing = SimulatedAnnealingStrategy()
sideways = SidewaysStrategy()
steepestAscent = SteepestAscentStrategy()
random_restart = RandomRestartStrategy()
stochastic = StochasticStrategy()
genetic = GeneticAlgorithm()

while True:
    # Continuously prompt for algorithm selection until a valid option is chosen
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
    
    # Handle user choice
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
    elif choice == 7:
        print("Exiting program.")
        break

    # Run the selected algorithm
    start_time = time.time()
    final_cube, final_score, iterations = algorithm_manager.solve(magic_cube)
    end_time = time.time()
    print(f"Hasil: Cube={final_cube}, Skor={final_score}, Iterasi={len(iterations)} Waktu={end_time - start_time} detik")
    
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
