from Algorithms.strategy import AlgorithmStrategy
from concurrent.futures import ThreadPoolExecutor, as_completed
from plot import PlotManager
import os
import time
from itertools import combinations

class SidewaysStrategy(AlgorithmStrategy):
    def execute(self, cube, **kwargs):
        max_sideways = kwargs.get("max_sideways", 10)
        start_time = time.time()

        current_score = cube.getCurrentScore()
        improved = True
        sideways_moves = 0 
        scores = [current_score] 
        iterations = []

        while improved:
            improved = False
            best_score = current_score
            best_positions = None
            found_better = False

            # Generate all unique position pairs and evaluate scores
            positions = [cube.get_position(i) for i in range(1, cube.n**3)]
            with ThreadPoolExecutor(os.cpu_count()) as executor:
                futures = {
                    executor.submit(cube.evaluate_swap_score, pos1, pos2): (pos1, pos2)
                    for pos1, pos2 in combinations(positions, 2)
                }

                for future in as_completed(futures):
                    swap_score = future.result()
                    pos1, pos2 = futures[future]
                    
                    if swap_score > best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)
                        found_better = True
                        sideways_moves = 0  # Reset sideways moves on improvement
                    elif swap_score == best_score and not found_better:
                        # Allow sideways move if no better score is found
                        best_positions = (pos1, pos2)
                    

            
            # If a swap was selected, apply it and update scores
            if best_positions:
                pos1, pos2 = best_positions
                cube.swap_elements(pos1, pos2)
                current_score = best_score
                scores.append(current_score)
                
                if found_better:
                    improved = True
                elif sideways_moves < max_sideways:
                    sideways_moves += 1
                    improved = True
                else:
                    improved = False  # Stop if max sideways moves reached
            
            # Store the current iteration state
            iterations.append((cube.cube.copy(), current_score))

        # Calculate the time taken for execution
        end_time = time.time()
        total_time = end_time - start_time
        total_iterations = len(scores)
        final_score = current_score

        # Plot the results
        plot_manager = PlotManager(scores)
        plot_manager.plot_sideways_strategy(total_iterations, total_time, sideways_moves, final_score)

        return cube.cube, current_score, iterations
