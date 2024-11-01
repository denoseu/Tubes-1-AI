import numpy as np
import random

# Fungsi untuk menghitung magic number dari sebuah kubus dengan sisi n
def calculate_magic_number(n):
    return (n * (n**3 + 1)) // 2

# Fungsi objective function yang telah diberikan
def calculate_objective_function(cube, magic_num):
    n = cube.shape[0]
    
    # Initialize the score
    score = 0

    # Check all rows, columns, and pillars
    for i in range(n):
        for j in range(n):
            # Rows in 2D slices
            row_sum = np.sum(cube[i, j, :])
            if row_sum == magic_num:
                score += 1
            # Columns in 2D slices
            col_sum = np.sum(cube[i, :, j])
            if col_sum == magic_num:
                score += 1
            # Pillars
            pillar_sum = np.sum(cube[:, i, j])
            if pillar_sum == magic_num:
                score += 1
    
    # Check 2D diagonals in XY, XZ, and YZ planes
    for i in range(n):
        # Main diagonal in XY slice
        main_diag = [cube[i, j, j] for j in range(n)]
        if np.sum(main_diag) == magic_num:
            score += 1
        # Anti-diagonal in XY slice
        anti_diag = [cube[i, j, n-j-1] for j in range(n)]
        if np.sum(anti_diag) == magic_num:
            score += 1

    # XZ-plane diagonals
    for j in range(n):
        # Main diagonal in XZ slice
        main_diag = [cube[i, j, i] for i in range(n)]
        if np.sum(main_diag) == magic_num:
            score += 1
        # Anti-diagonal in XZ slice
        anti_diag = [cube[i, j, n-i-1] for i in range(n)]
        if np.sum(anti_diag) == magic_num:
            score += 1

    # YZ-plane diagonals
    for j in range(n):
        # Main diagonal in YZ slice
        main_diag = [cube[k, k, j] for k in range(n)]
        if np.sum(main_diag) == magic_num:
            score += 1
        # Anti-diagonal in YZ slice
        anti_diag = [cube[k, n-k-1, j] for k in range(n)]
        if np.sum(anti_diag) == magic_num:
            score += 1

    # Check 3D diagonals in space
    # Main space diagonal
    main_space_diag = [cube[i, i, i] for i in range(n)]
    if np.sum(main_space_diag) == magic_num:
        score += 1
    # Anti space diagonal
    anti_space_diag = [cube[i, i, n-i-1] for i in range(n)]
    if np.sum(anti_space_diag) == magic_num:
        score += 1
    # Other space diagonals
    other_space_diag_1 = [cube[i, n-i-1, i] for i in range(n)]
    if np.sum(other_space_diag_1) == magic_num:
        score += 1
    other_space_diag_2 = [cube[n-i-1, i, i] for i in range(n)]
    if np.sum(other_space_diag_2) == magic_num:
        score += 1
    
    return score

# Fungsi untuk menukar dua elemen pada kubus
def swap_elements(cube, pos1, pos2):
    temp = cube[pos1]
    cube[pos1] = cube[pos2]
    cube[pos2] = temp

# Fungsi utama untuk menjalankan algoritma Stochastic Hill-Climbing
def stochastic_hill_climbing(n, max_iterations=1000):
    magic_number = calculate_magic_number(n)
    
    # Generate a random initial cube
    # cube = np.arange(1, n**3 + 1)
    # np.random.shuffle(cube)
    # cube = cube.reshape((n, n, n))

    cube = np.array([
    [[12, 82, 34, 87, 100], [25, 16, 80, 104, 90], [42, 111, 85, 2, 75], [121, 108, 7, 20, 59], [67, 18, 119, 106, 5]],
    [[91, 77, 71, 6, 70], [52, 64, 117, 69, 13], [30, 118, 21, 123, 23], [26, 39, 92, 44, 114], [116, 17, 14, 73, 95]],
    [[47, 61, 45, 76, 86], [107, 43, 38, 33, 94], [89, 68, 63, 58, 37], [32, 93, 88, 83, 19], [56, 120, 55, 49, 35]],
    [[31, 53, 112, 109, 10], [115, 98, 4, 1, 97], [103, 3, 105, 8, 96], [113, 57, 9, 62, 74], [40, 50, 81, 65, 79]],
    [[66, 72, 27, 102, 48], [29, 28, 122, 125, 11], [51, 15, 41, 124, 84], [36, 110, 46, 22, 101], [78, 54, 99, 24, 60]]
    ])
    
    current_score = calculate_objective_function(cube, magic_number)
    print(f"Initial score: {current_score}")
    
    for iteration in range(max_iterations):
        # Pilih dua posisi acak untuk ditukar
        pos1 = np.unravel_index(random.randint(0, n**3 - 1), (n, n, n))
        pos2 = np.unravel_index(random.randint(0, n**3 - 1), (n, n, n))
        
        # Tukar elemen pada posisi yang dipilih
        swap_elements(cube, pos1, pos2)
        neighbor_score = calculate_objective_function(cube, magic_number)
        
        # Jika tetangga lebih baik, pertahankan perubahan
        if neighbor_score > current_score:
            current_score = neighbor_score
            print(f"Iteration {iteration + 1}: Swapped {pos1} with {pos2}, new score: {current_score}")
        else:
            # Kembalikan kondisi sebelum swap jika tidak ada peningkatan
            swap_elements(cube, pos1, pos2)
        
    return cube, current_score

# Jalankan algoritma Stochastic Hill-Climbing
n = 5

import time
start_time = time.time()
final_cube, final_score = stochastic_hill_climbing(n, max_iterations=1000)
end_time = time.time()

print(f"Final score: {final_score}")

execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")
