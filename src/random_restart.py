from strategy import AlgorithmStrategy
class RandomRestartStrategy(AlgorithmStrategy):
    def execute(self, magic_cube, max_restarts=10):
            best_score = float("-inf")
            best_cube = None

            iterations = []

            for _ in range(max_restarts):
                magic_cube.initialize_cube(magic_cube.n)
                magic_cube.initialize_sums()
                current_score = magic_cube.steepest_ascent_parallel(magic_cube)

                if current_score > best_score:
                    best_score = current_score
                    best_cube = magic_cube.cube.copy()

                    iterations.append((magic_cube.cube.copy(),current_score))

            return best_cube, best_score
    

# 12 | 345
# 25341

##  12534