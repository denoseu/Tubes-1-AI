from strategy import AlgorithmStrategy
from concurrent.futures import ThreadPoolExecutor, as_completed
from plot import PlotManager
import time

class SteepestAscentStrategy(AlgorithmStrategy):
    def execute(self, cube, plot=True):
        start_time = time.time()

        current_score = cube.getCurrentScore()
        improved = True
        iterations = []
        scores = []

        print(cube.cube)

        while improved:
            improved = False
            best_score = current_score
            best_positions = None

            with ThreadPoolExecutor(8) as executor:
                futures = []
                for i in range(1, cube.n**3):
                    for j in range(i + 1, cube.n**3):
                        pos1 = cube.get_position(i)
                        pos2 = cube.get_position(j)

                        # Submit swap evaluations to the thread pool
                        futures.append(executor.submit(cube.evaluate_swap, pos1, pos2))

                for future in as_completed(futures):
                    swap_score, pos1, pos2 = future.result()
                    if swap_score > best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)

            if best_positions:
                pos1, pos2 = best_positions
                cube.swap_elements(pos1, pos2)
                current_score = best_score
                improved = True
                scores.append(current_score) 
                
            iterations.append((cube.cube.copy(), current_score))

        # Calculate the time taken for execution
        end_time = time.time()
        total_time = end_time - start_time
        total_iterations = len(scores)
        final_score = current_score

        if plot:
            plot_manager = PlotManager(scores)
            plot_manager.plot_objective_function(
                total_iterations=total_iterations, 
                total_time=total_time, 
                final_score=final_score
            )
        
        return cube.cube, current_score, iterations
