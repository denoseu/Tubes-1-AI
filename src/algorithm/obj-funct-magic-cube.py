import numpy as np

# Function to calculate the magic number for a given cube size
def magic_number(n):
    return (n * (n**3 + 1)) // 2

# Function to calculate the objective function score for the cube
def calculate_objective_function(cube):
    n = cube.shape[0]
    magic_num = magic_number(n)
    
    # Initialize the score
    score = 0

    # Check all rows, columns, and pillars
    print("\nChecking 2D Rows, Columns, and Pillars:\n")
    for i in range(n):
        for j in range(n):
            # Rows in 2D slices
            row_sum = np.sum(cube[i, j, :])
            print(f"2D Row (Slice {i+1}, Row {j+1}): {cube[i, j, :]} = {row_sum}")
            if row_sum == magic_num:
                score += 1
            # Columns in 2D slices
            col_sum = np.sum(cube[i, :, j])
            print(f"2D Column (Slice {i+1}, Column {j+1}): {cube[i, :, j]} = {col_sum}")
            if col_sum == magic_num:
                score += 1
            # Pillars
            pillar_sum = np.sum(cube[:, i, j])
            print(f"Pillar (Across Slices, Row {i+1}, Column {j+1}): {cube[:, i, j]} = {pillar_sum}")
            if pillar_sum == magic_num:
                score += 1
    
    # Check 2D diagonals in XY, XZ, and YZ planes
    print("\nChecking 2D Diagonals in XY, XZ, and YZ planes:\n")

    # XY-plane diagonals (already implemented)
    for i in range(n):
        # Main diagonal in XY slice
        main_diag = [cube[i, j, j] for j in range(n)]
        main_diag_sum = np.sum(main_diag)
        print(f"2D Main Diagonal (XY Slice {i+1}): {main_diag} = {main_diag_sum}")
        if main_diag_sum == magic_num:
            score += 1
        # Anti-diagonal in XY slice
        anti_diag = [cube[i, j, n-j-1] for j in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        print(f"2D Anti-Diagonal (XY Slice {i+1}): {anti_diag} = {anti_diag_sum}")
        if anti_diag_sum == magic_num:
            score += 1

    # XZ-plane diagonals
    for j in range(n):
        # Main diagonal in XZ slice
        main_diag = [cube[i, j, i] for i in range(n)]
        main_diag_sum = np.sum(main_diag)
        print(f"2D Main Diagonal (XZ Slice {j+1}): {main_diag} = {main_diag_sum}")
        if main_diag_sum == magic_num:
            score += 1
        # Anti-diagonal in XZ slice
        anti_diag = [cube[i, j, n-i-1] for i in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        print(f"2D Anti-Diagonal (XZ Slice {j+1}): {anti_diag} = {anti_diag_sum}")
        if anti_diag_sum == magic_num:
            score += 1

    # YZ-plane diagonals
    for j in range(n):
    # Main diagonal in YZ slice (fix the third index and vary the first and second)
        main_diag = [cube[k, k, j] for k in range(n)]
        main_diag_sum = np.sum(main_diag)
        print(f"2D Main Diagonal (YZ Slice {j+1}): {main_diag} = {main_diag_sum}")
        if main_diag_sum == magic_num:
            score += 1

        # Anti-diagonal in YZ slice (fix the third index and vary first/second with reverse traversal)
        anti_diag = [cube[k, n-k-1, j] for k in range(n)]
        anti_diag_sum = np.sum(anti_diag)
        print(f"2D Anti-Diagonal (YZ Slice {j+1}): {anti_diag} = {anti_diag_sum}")
        if anti_diag_sum == magic_num:
            score += 1

    # Check 3D diagonals in space
    print("\nChecking 3D Space Diagonals:\n")
    # Main space diagonal (from [0, 0, 0] to [n-1, n-1, n-1])
    main_space_diag = [cube[i, i, i] for i in range(n)]
    main_space_diag_sum = np.sum(main_space_diag)
    print(f"3D Main Space Diagonal: {main_space_diag} = {main_space_diag_sum}")
    if main_space_diag_sum == magic_num:
        score += 1

    # Anti space diagonal (from [0, 0, n-1] to [n-1, n-1, 0])
    anti_space_diag = [cube[i, i, n-i-1] for i in range(n)]
    anti_space_diag_sum = np.sum(anti_space_diag)
    print(f"3D Anti Space Diagonal: {anti_space_diag} = {anti_space_diag_sum}")
    if anti_space_diag_sum == magic_num:
        score += 1

    # Other space diagonals
    other_space_diag_1 = [cube[i, n-i-1, i] for i in range(n)]
    other_space_diag_1_sum = np.sum(other_space_diag_1)
    print(f"3D Diagonal 1: {other_space_diag_1} = {other_space_diag_1_sum}")
    if other_space_diag_1_sum == magic_num:
        score += 1

    other_space_diag_2 = [cube[n-i-1, i, i] for i in range(n)]
    other_space_diag_2_sum = np.sum(other_space_diag_2)
    print(f"3D Diagonal 2: {other_space_diag_2} = {other_space_diag_2_sum}")
    if other_space_diag_2_sum == magic_num:
        score += 1
    
    return score

# Example of initializing the cube (replace this with actual values)
# Assuming we have a 5x5x5 cube for example (fill in with actual data)
cube = np.array([
    [[25, 16, 80, 104, 90], [115, 98, 4, 1, 97], [42, 111, 85, 2, 75], [66, 72, 27, 102, 48], [67, 18, 119, 106, 5]],
    [[91, 77, 71, 6, 70], [52, 64, 117, 69, 13], [30, 118, 21, 123, 23], [26, 39, 92, 44, 114], [116, 17, 14, 73, 95]],
    [[47, 61, 45, 76, 86], [107, 43, 38, 33, 94], [89, 68, 63, 58, 37], [32, 93, 88, 83, 19], [40, 50, 81, 65, 79]],
    [[31, 53, 112, 109, 10], [12, 82, 34, 87, 100], [103, 3, 105, 8, 96], [113, 57, 9, 62, 74], [56, 120, 55, 49, 35]],
    [[121, 108, 7, 20, 59], [29, 28, 122, 125, 11], [51, 15, 41, 124, 84], [78, 54, 99, 24, 60], [36, 110, 46, 22, 101]]
])

# Calculate the objective function score
score = calculate_objective_function(cube)
print(f"Objective function score: {score}")
