from Algorithms.strategy import AlgorithmStrategy
from plot import PlotManager

class RandomRestartStrategy(AlgorithmStrategy):
    def execute(self, cube, max_restarts=100):
        best_score = float("-inf")
        best_cube = None
        best_iterations = None
        all_scores = []

        for _ in range(max_restarts):
            cube.initialize_cube(cube.n)
            cube.initialize_sums()

            _, current_score, iterations = self.steepest_ascent_parallel(cube, plot=False)
            
            restart_scores = [score for _, score in iterations]
            all_scores.append(restart_scores)
            
            if current_score > best_score:
                best_score = current_score
                best_cube = cube.cube.copy()
                best_iterations = iterations

        plot_manager = PlotManager()
        plot_manager.plot_multiple_objective_functions(all_scores)

        return best_cube, best_score, best_iterations