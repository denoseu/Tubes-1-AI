import numpy as np

class MagicCube:
    def __init__(self, n):
        self.n = n
        self.magic_number = self.calculate_magic_number(n)
        self.cube = self.initialize_cube(n)
        self.position_map = self.create_position_map()
        # Track rows, columns, pillars, and diagonals
        self.row_sums = np.zeros((n, n))       # row sums for each layer
        self.col_sums = np.zeros((n, n))       # column sums for each layer
        self.pillar_sums = np.zeros((n, n))    # pillar sums for each layer
        self.diagonal_sums = {
            "xy_main": np.zeros(n),            # main xy diagonal for each layer
            "xy_anti": np.zeros(n),            # anti xy diagonal for each layer
            "yz_main": np.zeros(n),            # main yz diagonal for each layer
            "yz_anti": np.zeros(n),            # anti yz diagonal for each layer
            "zx_main": np.zeros(n),            # main zx diagonal for each layer
            "zx_anti": np.zeros(n)             # anti zx diagonal for each layer
        }
        self.main_diagonals = [0, 0, 0, 0]     # 3D diagonals
        self.initialize_sums()                 
        self.score = self.calculate_objective_function()

    def remake_cube(self):
        self.cube = self.initialize_cube(self.n)
        self.position_map = self.create_position_map()
        self.initialize_sums()
        self.score = self.calculate_objective_function()

    def calculate_magic_number(self, n):
        return n * (n**3 + 1) // 2

    def initialize_cube(self, n):
        # Initialize cube with random values for testing
        return np.random.permutation(n**3).reshape(n, n, n) + 1

    def create_position_map(self):
        # Map values to their positions for quick lookups
        return {self.cube[i, j, k]: (i, j, k) for i in range(self.n) for j in range(self.n) for k in range(self.n)}
    
    def update_position_map(self):
        self.position_map = self.create_position_map()

    def get_position(self, value):
        return self.position_map[value]

    def initialize_sums(self):
        
        for i in range(self.n):
            for j in range(self.n):
                # Row, column, and pillar sums
                self.row_sums[i, j] = np.sum(self.cube[i, j, :])
                self.col_sums[i, j] = np.sum(self.cube[i, :, j])
                self.pillar_sums[i, j] = np.sum(self.cube[:, i, j])

            # Diagonal sums in each layer
            self.diagonal_sums["xy_main"][i] = np.sum([self.cube[i, j, j] for j in range(self.n)])
            self.diagonal_sums["xy_anti"][i] = np.sum([self.cube[i, j, self.n - j - 1] for j in range(self.n)])
            self.diagonal_sums["yz_main"][i] = np.sum([self.cube[j, i, j] for j in range(self.n)])
            self.diagonal_sums["yz_anti"][i] = np.sum([self.cube[j, i, self.n - j - 1] for j in range(self.n)])
            self.diagonal_sums["zx_main"][i] = np.sum([self.cube[j, j, i] for j in range(self.n)])
            self.diagonal_sums["zx_anti"][i] = np.sum([self.cube[j, self.n - j - 1, i] for j in range(self.n)])

        # 3D main diagonals
        self.main_diagonals[0] = np.sum([self.cube[i, i, i] for i in range(self.n)])
        self.main_diagonals[1] = np.sum([self.cube[i, i, self.n - i - 1] for i in range(self.n)])
        self.main_diagonals[2] = np.sum([self.cube[i, self.n - i - 1, i] for i in range(self.n)])
        self.main_diagonals[3] = np.sum([self.cube[self.n - i - 1, i, i] for i in range(self.n)])

    def swap_elements(self, pos1, pos2):
        val1 = self.cube[pos1]
        val2 = self.cube[pos2]
        self.cube[pos1], self.cube[pos2] = val2, val1

        # Update position map
        self.position_map[val1], self.position_map[val2] = pos2, pos1

        # Update the row, column, and pillar sums
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2

        # Update row, column, and pillar sums
        self.row_sums[x1, y1] += val2 - val1
        self.row_sums[x2, y2] += val1 - val2
        self.col_sums[x1, z1] += val2 - val1
        self.col_sums[x2, z2] += val1 - val2
        self.pillar_sums[y1, z1] += val2 - val1
        self.pillar_sums[y2, z2] += val1 - val2

        # Update diagonal sums if affected
        if y1 == z1:
            self.diagonal_sums["xy_main"][x1] += val2 - val1
        if y2 == z2:
            self.diagonal_sums["xy_main"][x2] += val1 - val2
        if y1 == self.n - z1 - 1:
            self.diagonal_sums["xy_anti"][x1] += val2 - val1
        if y2 == self.n - z2 - 1:
            self.diagonal_sums["xy_anti"][x2] += val1 - val2
        if x1 == z1:
            self.diagonal_sums["yz_main"][y1] += val2 - val1
        if x2 == z2:
            self.diagonal_sums["yz_main"][y2] += val1 - val2
        if x1 == self.n - z1 - 1:
            self.diagonal_sums["yz_anti"][y1] += val2 - val1
        if x2 == self.n - z2 - 1:
            self.diagonal_sums["yz_anti"][y2] += val1 - val2
        if x1 == y1:
            self.diagonal_sums["zx_main"][z1] += val2 - val1
        if x2 == y2:
            self.diagonal_sums["zx_main"][z2] += val1 - val2
        if x1 == self.n - y1 - 1:
            self.diagonal_sums["zx_anti"][z1] += val2 - val1
        if x2 == self.n - y2 - 1:
            self.diagonal_sums["zx_anti"][z2] += val1 - val2
        

        # Similar updates for yz and zx diagonals, as well as 3D main diagonals
        if x1 == y1 == z1:
            self.main_diagonals[0] += val2 - val1
        if x2 == y2 == z2:
            self.main_diagonals[0] += val1 - val2
        if x1 == y1 == self.n - z1 - 1:
            self.main_diagonals[1] += val2 - val1
        if x2 == y2 == self.n - z2 - 1:
            self.main_diagonals[1] += val1 - val2
        if x1 == self.n - y1 - 1 == z1:
            self.main_diagonals[2] += val2 - val1
        if x2 == self.n - y2 - 1 == z2:
            self.main_diagonals[2] += val1 - val2
        if x1 == self.n - y1 - 1 == self.n - z1 - 1:
            self.main_diagonals[3] += val2 - val1
        if x2 == self.n - y2 - 1 == self.n - z2 - 1:
            self.main_diagonals[3] += val1 - val2

        self.score = self.calculate_objective_function()

    def calculate_objective_function(self):
        target = self.magic_number
        score = 0
        
        for i in range(self.n):
            for j in range(self.n):
                score += abs(self.row_sums[i, j] - target)
                score += abs(self.col_sums[i, j] - target)
                score += abs(self.pillar_sums[i, j] - target)

        for key in self.diagonal_sums:
            for i in range(self.n):
                score += abs(self.diagonal_sums[key][i] - target)

        for main_diag in self.main_diagonals:
            score += abs(main_diag - target)

        return -score
    
    def getCurrentScore(self):
        return self.score
    
    def evaluate_swap(self, pos1, pos2):
        # Swap elements temporarily
        self.swap_elements(pos1, pos2)
        
        # Calculate score
        score = self.getCurrentScore()
        
        # Revert swap
        self.swap_elements(pos1, pos2)
        
        return score, pos1, pos2
    
    def swap_number(self,num1,num2):
        pos1 = self.position_map[num1]
        pos2 = self.position_map[num2]
        
        self.swap_elements(pos1,pos2)
    
    def evaluate_swap_score(self, pos1, pos2):
        val1 = self.cube[pos1]
        val2 = self.cube[pos2]
        target = self.magic_number
        hypothetical_score = self.score  
        
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        
        def temp_diff(current_sum, new_val, old_val):
            return abs(current_sum - target) - abs((current_sum + new_val - old_val) - target)

        hypothetical_score += temp_diff(self.row_sums[x1, y1], val2, val1)
        hypothetical_score += temp_diff(self.row_sums[x2, y2], val1, val2)
        hypothetical_score += temp_diff(self.col_sums[x1, z1], val2, val1)
        hypothetical_score += temp_diff(self.col_sums[x2, z2], val1, val2)
        hypothetical_score += temp_diff(self.pillar_sums[y1, z1], val2, val1)
        hypothetical_score += temp_diff(self.pillar_sums[y2, z2], val1, val2)

        # Adjust diagonals if affected by the swap
        if y1 == z1:
            hypothetical_score += temp_diff(self.diagonal_sums["xy_main"][x1], val2, val1)
        if y2 == z2:
            hypothetical_score += temp_diff(self.diagonal_sums["xy_main"][x2], val1, val2)
        if y1 == self.n - z1 - 1:
            hypothetical_score += temp_diff(self.diagonal_sums["xy_anti"][x1], val2, val1)
        if y2 == self.n - z2 - 1:
            hypothetical_score += temp_diff(self.diagonal_sums["xy_anti"][x2], val1, val2)
        if x1 == z1:
            hypothetical_score += temp_diff(self.diagonal_sums["yz_main"][y1], val2, val1)
        if x2 == z2:
            hypothetical_score += temp_diff(self.diagonal_sums["yz_main"][y2], val1, val2)
        if x1 == self.n - z1 - 1:
            hypothetical_score += temp_diff(self.diagonal_sums["yz_anti"][y1], val2, val1)
        if x2 == self.n - z2 - 1:
            hypothetical_score += temp_diff(self.diagonal_sums["yz_anti"][y2], val1, val2)
        if x1 == y1:
            hypothetical_score += temp_diff(self.diagonal_sums["zx_main"][z1], val2, val1)
        if x2 == y2:
            hypothetical_score += temp_diff(self.diagonal_sums["zx_main"][z2], val1, val2)
        if x1 == self.n - y1 - 1:
            hypothetical_score += temp_diff(self.diagonal_sums["zx_anti"][z1], val2, val1)
        if x2 == self.n - y2 - 1:
            hypothetical_score += temp_diff(self.diagonal_sums["zx_anti"][z2], val1, val2)

        # 3D main diagonals adjustments, if affected by the swap
        if x1 == y1 == z1:
            hypothetical_score += temp_diff(self.main_diagonals[0], val2, val1)
        if x2 == y2 == z2:
            hypothetical_score += temp_diff(self.main_diagonals[0], val1, val2)
        if x1 == y1 == self.n - z1 - 1:
            hypothetical_score += temp_diff(self.main_diagonals[1], val2, val1)
        if x2 == y2 == self.n - z2 - 1:
            hypothetical_score += temp_diff(self.main_diagonals[1], val1, val2)
        if x1 == self.n - y1 - 1 == z1:
            hypothetical_score += temp_diff(self.main_diagonals[2], val2, val1)
        if x2 == self.n - y2 - 1 == z2:
            hypothetical_score += temp_diff(self.main_diagonals[2], val1, val2)
        if x1 == self.n - y1 - 1 == self.n - z1 - 1:
            hypothetical_score += temp_diff(self.main_diagonals[3], val2, val1)
        if x2 == self.n - y2 - 1 == self.n - z2 - 1:
            hypothetical_score += temp_diff(self.main_diagonals[3], val1, val2)

        # Return the hypothetical objective function value
        return hypothetical_score
