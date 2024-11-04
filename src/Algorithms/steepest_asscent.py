from itertools import combinations
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from Algorithms.strategy import AlgorithmStrategy
from plot import PlotManager

class SteepestAscentStrategy(AlgorithmStrategy):
    def execute(self, cube, plot=True):
        start_time = time.time()
        current_score = cube.getCurrentScore()

        improved = True
        iterations = []
        scores = []

        while improved:
            improved = False
            best_score = current_score
            best_positions = None

            # Generate all unique pairs of positions
            positions = [cube.get_position(i) for i in range(1, cube.n**3)]
            
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = {
                    executor.submit(cube.evaluate_swap_score, pos1, pos2): (pos1, pos2)
                    for pos1, pos2 in combinations(positions, 2)
                }

                # Retrieve swap scores as they complete
                for future in as_completed(futures):
                    swap_score = future.result()
                    pos1, pos2 = futures[future]
                    
                    if swap_score > best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)

            if best_positions:
                print(f"Best Score: {best_score}")
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
