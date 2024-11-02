import numpy as np
import random
import matplotlib.pyplot as plt

# Fungsi untuk menghitung magic number dari sebuah kubus dengan sisi n
def calculate_magic_number(n):
    return (n * (n**3 + 1)) // 2

# Fungsi untuk menghitung objective function
def calculate_objective_function(cube, magic_num):
    n = cube.shape[0]
    score = 0

    for i in range(n):
        for j in range(n):
            # baris
            row_sum = np.sum(cube[i, j, :])
            if row_sum == magic_num:
                score += 1
            # kolom
            col_sum = np.sum(cube[i, :, j])
            if col_sum == magic_num:
                score += 1
            # tiang
            pillar_sum = np.sum(cube[:, i, j])
            if pillar_sum == magic_num:
                score += 1
    
    # bidang XY
    for i in range(n):
        # main diagonal
        main_diag = [cube[i, j, j] for j in range(n)]
        main_diag_sum = np.sum(main_diag)
        if main_diag_sum == magic_num:
            score += 1
        # anti diagonal
        anti_diag = [cube[i, j, n-j-1] for j in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        if anti_diag_sum == magic_num:
            score += 1

    # bidang XZ
    for j in range(n):
        # main diagonal
        main_diag = [cube[i, j, i] for i in range(n)]
        main_diag_sum = np.sum(main_diag)
        if main_diag_sum == magic_num:
            score += 1
        # anti diagonal
        anti_diag = [cube[i, j, n-i-1] for i in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        if anti_diag_sum == magic_num:
            score += 1

    # bidang YZ
    for j in range(n):
        # main diagonal
        main_diag = [cube[k, k, j] for k in range(n)]
        main_diag_sum = np.sum(main_diag)
        if main_diag_sum == magic_num:
            score += 1
        # anti diagonal
        anti_diag = [cube[k, n-k-1, j] for k in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        if anti_diag_sum == magic_num:
            score += 1

    # main space diagonal (from [0, 0, 0] to [n-1, n-1, n-1])
    main_space_diag = [cube[i, i, i] for i in range(n)]
    main_space_diag_sum = np.sum(main_space_diag)
    if main_space_diag_sum == magic_num:
        score += 1

    # anti space diagonal (from [0, 0, n-1] to [n-1, n-1, 0])
    anti_space_diag = [cube[i, i, n-i-1] for i in range(n)]
    anti_space_diag_sum = np.sum(anti_space_diag)
    if anti_space_diag_sum == magic_num:
        score += 1

    # diagonal ruang lainnya
    other_space_diag_1 = [cube[i, n-i-1, i] for i in range(n)]
    other_space_diag_1_sum = np.sum(other_space_diag_1)
    if other_space_diag_1_sum == magic_num:
        score += 1

    other_space_diag_2 = [cube[n-i-1, i, i] for i in range(n)]
    other_space_diag_2_sum = np.sum(other_space_diag_2)
    if other_space_diag_2_sum == magic_num:
        score += 1
    
    return score

# Fungsi untuk menukar dua elemen pada kubus
def swap_elements(cube, pos1, pos2):
    temp = cube[pos1]
    cube[pos1] = cube[pos2]
    cube[pos2] = temp

def get_successors(cube):
    n = cube.shape[0]
    successors = []
    
    for i in range(n**3):
        for j in range(i + 1, n**3):
            pos1 = np.unravel_index(i, (n, n, n))
            pos2 = np.unravel_index(j, (n, n, n))
            # simpan kondisi kubus sebelum di swap
            new_cube = cube.copy()
            swap_elements(new_cube, pos1, pos2)
            successors.append((new_cube, (pos1, pos2)))  # Menyimpan kubus dan posisi yang ditukar
            
    return successors

# Fungsi utama untuk menjalankan algoritma Steepest Ascent Hill-Climbing dan mencatat nilai objective function
def steepest_ascent_hill_climbing(cube):
    n = cube.shape[0]
    magic_number = calculate_magic_number(n)
    
    current_score = calculate_objective_function(cube, magic_number)
    print(f"Initial score: {current_score}")
    
    # List untuk menyimpan nilai objective function di setiap iterasi
    scores = [current_score]
    iter_count = 0

    while True:
        successors = get_successors(cube)
        best_neighbor_score = current_score
        best_successor = None
        
        for successor, positions in successors:
            neighbor_score = calculate_objective_function(successor, magic_number)

            if neighbor_score > best_neighbor_score:
                best_neighbor_score = neighbor_score
                best_successor = successor
                best_positions = positions

        if best_successor is not None:
            cube = best_successor
            current_score = best_neighbor_score
            print(f"Iteration {iter_count}: Moved to better neighbor, new score: {current_score}")
            print(f"Swapped: {best_positions[0]} with {best_positions[1]}")
            scores.append(current_score)  # Menyimpan nilai score setelah tiap iterasi
        else:
            print(f"No better neighbor found at iteration {iter_count}, terminating.")
            break

        iter_count += 1

    return cube, scores

# Initial state dari kubus (5x5x5) dengan angka 1 hingga 125 secara acak
n = 5
initial_cube = np.array([
    [[12, 82, 34, 87, 100], [25, 16, 80, 104, 90], [42, 111, 85, 2, 75], [121, 108, 7, 20, 59], [67, 18, 119, 106, 5]],
    [[91, 77, 71, 6, 70], [52, 64, 117, 69, 13], [30, 118, 21, 123, 23], [26, 39, 92, 44, 114], [116, 17, 14, 73, 95]],
    [[47, 61, 45, 76, 86], [107, 43, 38, 33, 94], [89, 68, 63, 58, 37], [32, 93, 88, 83, 19], [56, 120, 55, 49, 35]],
    [[31, 53, 112, 109, 10], [115, 98, 4, 1, 97], [103, 3, 105, 8, 96], [113, 57, 9, 62, 74], [40, 50, 81, 65, 79]],
    [[66, 72, 27, 102, 48], [29, 28, 122, 125, 11], [51, 15, 41, 124, 84], [36, 110, 46, 22, 101], [78, 54, 99, 24, 60]]
])

# Jalankan algoritma Steepest Ascent Hill-Climbing
import time
start_time = time.time()
final_cube, scores = steepest_ascent_hill_climbing(initial_cube)
end_time = time.time()

# waktu ekskusi dalam detik
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

# Plot nilai objective function terhadap iterasi
plt.plot(scores)
plt.xlabel('Iteration')
plt.ylabel('Objective Function Value')
plt.title('Objective Function Value vs. Iteration')
plt.grid()
plt.show()