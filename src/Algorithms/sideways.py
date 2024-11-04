from Algorithms.strategy import AlgorithmStrategy
from concurrent.futures import ThreadPoolExecutor, as_completed
from plot import PlotManager
import os
import time

class SidewaysStrategy(AlgorithmStrategy):
    def execute(self, cube, max_sideways=100):
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

            with ThreadPoolExecutor(os.cpu_count()) as executor:
                futures = []
                for i in range(1, cube.n**3):
                    for j in range(i + 1, cube.n**3):
                        pos1 = cube.get_position(i)
                        pos2 = cube.get_position(j)
                        futures.append(executor.submit(cube.evaluate_swap, pos1, pos2))

                for future in as_completed(futures):
                    swap_score, pos1, pos2 = future.result()
                    if swap_score > best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)
                        found_better = True
                        sideways_moves = 0
                    elif swap_score == best_score and not found_better:
                        best_positions = (pos1, pos2)
            
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
                    improved = False # max sideway alr
            
            iterations.append((cube.cube.copy(), current_score))

        end_time = time.time()
        total_time = end_time - start_time
        total_iterations = len(scores)
        final_score = current_score

        plot_manager = PlotManager(scores)
        plot_manager.plot_sideways_strategy(total_iterations, total_time, sideways_moves, final_score)

        return cube.cube, current_score, iterations