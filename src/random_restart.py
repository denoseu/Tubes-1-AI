import time
from strategy import AlgorithmStrategy
from plot import PlotManager
from steepest_asscent import SteepestAscentStrategy

steepestAscent = SteepestAscentStrategy()

class RandomRestartStrategy(AlgorithmStrategy):
    def execute(self, cube, max_restarts=3):
        start_time_all = time.time()
        best_score = float("-inf")
        best_cube = None
        best_iterations = None
        all_scores = []
        restart_times = []
        restart_iterations = []

        for _ in range(max_restarts):
            cube.initialize_cube(cube.n)
            cube.initialize_sums()
            
            start_time = time.time()
            _, current_score, iterations = steepestAscent.execute(cube, plot=False)
            end_time = time.time()
            
            restart_scores = [score for _, score in iterations]
            all_scores.append(restart_scores)
            restart_times.append(end_time - start_time)
            restart_iterations.append(len(iterations))

            if current_score > best_score:
                best_score = current_score
                best_cube = cube.cube.copy()
                best_iterations = iterations

        end_time_all = time.time()
        final_exec_time = end_time_all - start_time_all

        plot_manager = PlotManager()
        plot_manager.plot_random_restart_summary(all_scores, restart_times, restart_iterations, final_exec_time)

        return best_cube, best_score, best_iterations
