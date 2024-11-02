import numpy as np
import random
import matplotlib.pyplot as plt

# Fungsi untuk menginisialisasi satu kubus acak
def initialize_random_cube(n):
    cube = np.arange(1, n**3 + 1)
    np.random.shuffle(cube)
    return cube.reshape((n, n, n))

# Fungsi untuk menghitung magic number dari sebuah kubus dengan sisi n
def calculate_magic_number(n):
    return (n * (n**3 + 1)) // 2

# Function to calculate the objective function score for the cube
def calculate_objective_function(cube, magic_num):
    n = cube.shape[0]
    # magic_num = calculate_magic_number(n)
    
    # Initialize the score
    score = 0

    # Check all rows, columns, and pillars
    # print("\nChecking 2D Rows, Columns, and Pillars:\n")
    for i in range(n):
        for j in range(n):
            # Rows in 2D slices
            row_sum = np.sum(cube[i, j, :])
            # print(f"2D Row (Slice {i+1}, Row {j+1}): {cube[i, j, :]} = {row_sum}")
            if row_sum == magic_num:
                score += 1
            # Columns in 2D slices
            col_sum = np.sum(cube[i, :, j])
            # print(f"2D Column (Slice {i+1}, Column {j+1}): {cube[i, :, j]} = {col_sum}")
            if col_sum == magic_num:
                score += 1
            # Pillars
            pillar_sum = np.sum(cube[:, i, j])
            # print(f"Pillar (Across Slices, Row {i+1}, Column {j+1}): {cube[:, i, j]} = {pillar_sum}")
            if pillar_sum == magic_num:
                score += 1
    
    # Check 2D diagonals in XY, XZ, and YZ planes
    # print("\nChecking 2D Diagonals in XY, XZ, and YZ planes:\n")

    # XY-plane diagonals (already implemented)
    for i in range(n):
        # Main diagonal in XY slice
        main_diag = [cube[i, j, j] for j in range(n)]
        main_diag_sum = np.sum(main_diag)
        # print(f"2D Main Diagonal (XY Slice {i+1}): {main_diag} = {main_diag_sum}")
        if main_diag_sum == magic_num:
            score += 1
        # Anti-diagonal in XY slice
        anti_diag = [cube[i, j, n-j-1] for j in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        # print(f"2D Anti-Diagonal (XY Slice {i+1}): {anti_diag} = {anti_diag_sum}")
        if anti_diag_sum == magic_num:
            score += 1

    # XZ-plane diagonals
    for j in range(n):
        # Main diagonal in XZ slice
        main_diag = [cube[i, j, i] for i in range(n)]
        main_diag_sum = np.sum(main_diag)
        # print(f"2D Main Diagonal (XZ Slice {j+1}): {main_diag} = {main_diag_sum}")
        if main_diag_sum == magic_num:
            score += 1
        # Anti-diagonal in XZ slice
        anti_diag = [cube[i, j, n-i-1] for i in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        # print(f"2D Anti-Diagonal (XZ Slice {j+1}): {anti_diag} = {anti_diag_sum}")
        if anti_diag_sum == magic_num:
            score += 1

    # YZ-plane diagonals
    for j in range(n):
    # Main diagonal in YZ slice (fix the third index and vary the first and second)
        main_diag = [cube[k, k, j] for k in range(n)]
        main_diag_sum = np.sum(main_diag)
        # print(f"2D Main Diagonal (YZ Slice {j+1}): {main_diag} = {main_diag_sum}")
        if main_diag_sum == magic_num:
            score += 1

        # Anti-diagonal in YZ slice (fix the third index and vary first/second with reverse traversal)
        anti_diag = [cube[k, n-k-1, j] for k in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        # print(f"2D Anti-Diagonal (YZ Slice {j+1}): {anti_diag} = {anti_diag_sum}")
        if anti_diag_sum == magic_num:
            score += 1

    # Check 3D diagonals in space
    # print("\nChecking 3D Space Diagonals:\n")
    # Main space diagonal (from [0, 0, 0] to [n-1, n-1, n-1])
    main_space_diag = [cube[i, i, i] for i in range(n)]
    main_space_diag_sum = np.sum(main_space_diag)
    # print(f"3D Main Space Diagonal: {main_space_diag} = {main_space_diag_sum}")
    if main_space_diag_sum == magic_num:
        score += 1

    # Anti space diagonal (from [0, 0, n-1] to [n-1, n-1, 0])
    anti_space_diag = [cube[i, i, n-i-1] for i in range(n)]
    anti_space_diag_sum = np.sum(anti_space_diag)
    # print(f"3D Anti Space Diagonal: {anti_space_diag} = {anti_space_diag_sum}")
    if anti_space_diag_sum == magic_num:
        score += 1

    # Other space diagonals
    other_space_diag_1 = [cube[i, n-i-1, i] for i in range(n)]
    other_space_diag_1_sum = np.sum(other_space_diag_1)
    # print(f"3D Diagonal 1: {other_space_diag_1} = {other_space_diag_1_sum}")
    if other_space_diag_1_sum == magic_num:
        score += 1

    other_space_diag_2 = [cube[n-i-1, i, i] for i in range(n)]
    other_space_diag_2_sum = np.sum(other_space_diag_2)
    # print(f"3D Diagonal 2: {other_space_diag_2} = {other_space_diag_2_sum}")
    if other_space_diag_2_sum == magic_num:
        score += 1
    
    return score

# Fungsi untuk menukar dua elemen pada kubus
def swap_elements(cube, pos1, pos2):
    temp = cube[pos1]
    cube[pos1] = cube[pos2]
    cube[pos2] = temp

# Fungsi untuk menghitung fitness (menggunakan objective function)
def fitness(cube, magic_number):
    return calculate_objective_function(cube, magic_number)

# Fungsi untuk melakukan seleksi menggunakan roulette wheel selection
def roulette_wheel_selection(population, fitness_scores):
    total_fitness = np.sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected_idx = np.random.choice(len(population), p=probabilities)
    return population[selected_idx]

# Fungsi crossover untuk menggabungkan dua parent dan menghasilkan offspring
def crossover(parent1, parent2):
    n = parent1.shape[0]
    crossover_point = random.randint(1, n-1) 
    child1 = np.zeros_like(parent1)
    child2 = np.zeros_like(parent2)
    
    child1[:crossover_point, :, :] = parent1[:crossover_point, :, :]
    child1[crossover_point:, :, :] = parent2[crossover_point:, :, :]
    
    child2[:crossover_point, :, :] = parent2[:crossover_point, :, :]
    child2[crossover_point:, :, :] = parent1[crossover_point:, :, :]
    
    return child1, child2

# Fungsi mutasi: menukar dua elemen secara acak dalam offspring
def mutate(cube, mutation_rate):
    if random.random() < mutation_rate:
        n = cube.shape[0]
        pos1 = tuple(np.random.randint(n, size=3))
        pos2 = tuple(np.random.randint(n, size=3))
        
        swap_elements(cube, pos1, pos2)

# Fungsi untuk menjalankan algoritma genetika
def genetic_algorithm(n, population_size, generations, mutation_rate):
    magic_number = calculate_magic_number(n)
    
    # Initialize population
    population = [initialize_random_cube(n) for _ in range(population_size)]
    
    # Fitness statistics (objective function value)
    max_fitness = []
    avg_fitness = []
    
    best_individual = None
    best_fitness = -1
    
    for generation in range(generations):
        # Evaluate population and calculate fitness for each individual
        fitness_scores = [fitness(cube, magic_number) for cube in population]
        
        # Track the best individual
        current_best_fitness = max(fitness_scores)
        current_best_individual = population[np.argmax(fitness_scores)]
        
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_individual = current_best_individual

        # Store fitness statistics for this generation
        max_fitness.append(current_best_fitness)
        avg_fitness.append(np.mean(fitness_scores))
        
        print(f"Generation {generation + 1}, Best fitness: {best_fitness}")

        # Selection and reproduction to create the new population
        new_population = []
        for _ in range(population_size // 2):
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)
            
            # Crossover to create offspring
            child1, child2 = crossover(parent1, parent2)

            # Mutation on offspring
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            
            # Add offspring to the new population
            new_population.append(child1)
            new_population.append(child2)
        
        # Replace old population with the new one
        population = new_population
    
    print(f"Best solution found with fitness: {best_fitness}")
    return best_individual, best_fitness, max_fitness, avg_fitness

# Parameters
n = 5  # Cube size
population_size = 50
generations = 1000
mutation_rate = 0.05

# Run the genetic algorithm and gather fitness history data
best_individual, best_fitness, max_fitness, avg_fitness = genetic_algorithm(
    n, population_size, generations, mutation_rate
)

# Plotting maximum and average fitness over generations
plt.figure(figsize=(10, 6))
plt.plot(range(1, generations + 1), max_fitness, label="Max Fitness", color="blue")
plt.plot(range(1, generations + 1), avg_fitness, label="Average Fitness", color="green")
plt.xlabel("Generation")
plt.ylabel("Fitness (Objective Function)")
plt.title("Maximum and Average Fitness over Generations")
plt.legend()
plt.grid()
plt.show()
