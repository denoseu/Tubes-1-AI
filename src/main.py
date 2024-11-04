from cube import MagicCube
from algomanager import AlgorithmManager
from simulated_annealing import SimulatedAnnealingStrategy

n = 5
magic_cube = MagicCube(n)
algorithm_manager = AlgorithmManager()
simulatedAnnealing = SimulatedAnnealingStrategy()

start = True

while start:
    print("Pilih Algoritma:")
    print("1. Steepest Ascent")
    print("2. Simulated Annealing")
    print("3. Genetic Algorithm")
    print("4. Exit")
    choice = int(input())


    if (choice == 1):
        algorithm_manager.setStrategy(simulatedAnnealing)
        final_cube, final_scsore, iterations = algorithm_manager.solve(magic_cube)
    
    
    while True:
        replay_experiment = input("Apakah Anda ingin melakukan eksperimen ulang (y or n): ").strip().lower()
        if replay_experiment in ["y", "n"]:
            start = False
            break
        else:
            print("Input tidak valid. Masukkan 'y' atau 'n'.")

    


