import numpy as np
import random
import math

# Fungsi untuk menghitung magic number dari sebuah kubus dengan sisi n
def calculate_magic_number(n):
    return (n * (n**3 + 1)) // 2

# Objective function yang diberikan
def calculate_objective_function(cube, magic_num):
    n = cube.shape[0]
    score = 0

    for i in range(n):
        for j in range(n):
            row_sum = np.sum(cube[i, j, :])
            if row_sum == magic_num:
                score += 1
            col_sum = np.sum(cube[i, :, j])
            if col_sum == magic_num:
                score += 1
            pillar_sum = np.sum(cube[:, i, j])
            if pillar_sum == magic_num:
                score += 1

    for i in range(n):
        main_diag = [cube[i, j, j] for j in range(n)]
        if np.sum(main_diag) == magic_num:
            score += 1
        anti_diag = [cube[i, j, n-j-1] for j in range(n)]
        if np.sum(anti_diag) == magic_num:
            score += 1

    for j in range(n):
        main_diag = [cube[i, j, i] for i in range(n)]
        if np.sum(main_diag) == magic_num:
            score += 1
        anti_diag = [cube[i, j, n-i-1] for i in range(n)]
        if np.sum(anti_diag) == magic_num:
            score += 1

    for j in range(n):
        main_diag = [cube[k, k, j] for k in range(n)]
        if np.sum(main_diag) == magic_num:
            score += 1
        anti_diag = [cube[k, n-k-1, j] for k in range(n)]
        if np.sum(anti_diag) == magic_num:
            score += 1

    main_space_diag = [cube[i, i, i] for i in range(n)]
    if np.sum(main_space_diag) == magic_num:
        score += 1

    anti_space_diag = [cube[i, i, n-i-1] for i in range(n)]
    if np.sum(anti_space_diag) == magic_num:
        score += 1

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

# Fungsi untuk menjalankan Simulated Annealing dengan debug messages horizontal
def simulated_annealing(cube, initial_temp, cooling_rate):
    n = cube.shape[0]
    magic_number = calculate_magic_number(n)
    
    current_cube = cube.copy()
    current_score = calculate_objective_function(current_cube, magic_number)
    temperature = initial_temp

    print(f"Initial cube:\n{current_cube}\n")
    print(f"Initial score: {current_score}, Magic number: {magic_number}\n")

    iteration = 0
    while temperature > 1e-3:
        iteration += 1
        
        # Pilih dua posisi acak untuk swap
        pos1 = tuple(np.unravel_index(np.random.randint(0, n**3), (n, n, n)))
        pos2 = tuple(np.unravel_index(np.random.randint(0, n**3), (n, n, n)))

        # Buat tetangga baru dengan swap
        new_cube = current_cube.copy()
        swap_elements(new_cube, pos1, pos2)
        new_score = calculate_objective_function(new_cube, magic_number)

        # Hitung delta score
        delta_score = new_score - current_score

        # Tentukan apakah solusi diterima atau tidak
        accepted = False
        if delta_score > 0:
            accepted = True
        else:
            acceptance_probability = math.exp(delta_score / temperature)
            static_val = 0.5
            if static_val < acceptance_probability:
                accepted = True

        # Log debugging horizontal (dalam satu baris)
        print(f"Iter {iteration:4d} | Temp: {temperature:.5f} | Pos1: {pos1} <-> Pos2: {pos2} | Current Score: {current_score} | New Score: {new_score} | Delta: {delta_score} | Accepted: {accepted}")

        # Update jika diterima
        if accepted:
            current_cube = new_cube
            current_score = new_score

        # Turunkan temperatur
        temperature *= cooling_rate

    print(f"\nFinal cube:\n{current_cube}")
    print(f"Final score: {current_score}")
    
    return current_cube, current_score

# Inisialisasi state awal dari kubus (5x5x5) dengan angka 1 hingga 125 secara acak
n = 5
# initial_cube = np.arange(1, n**3 + 1)
# np.random.shuffle(initial_cube)
# initial_cube = initial_cube.reshape((n, n, n))

initial_cube = np.array([
    [[12, 82, 34, 87, 100], [25, 16, 80, 104, 90], [42, 111, 85, 2, 75], [121, 108, 7, 20, 59], [67, 18, 119, 106, 5]],
    [[91, 77, 71, 6, 70], [52, 64, 117, 69, 13], [30, 118, 21, 123, 23], [26, 39, 92, 44, 114], [116, 17, 14, 73, 95]],
    [[47, 61, 45, 76, 86], [107, 43, 38, 33, 94], [89, 68, 63, 58, 37], [32, 93, 88, 83, 19], [56, 120, 55, 49, 35]],
    [[31, 53, 112, 109, 10], [115, 98, 4, 1, 97], [103, 3, 105, 8, 96], [113, 57, 9, 62, 74], [40, 50, 81, 65, 79]],
    [[66, 72, 27, 102, 48], [29, 28, 122, 125, 11], [51, 15, 41, 124, 84], [36, 110, 46, 22, 101], [78, 54, 99, 24, 60]]
])

import time
start_time = time.time()
# Jalankan algoritma Simulated Annealing dengan debug messages horizontal
final_cube, final_score = simulated_annealing(initial_cube, initial_temp=1000, cooling_rate=0.9999)

print(f"Final score: {final_score}")
end_time = time.time()

# waktu ekskusi dalam detik
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")