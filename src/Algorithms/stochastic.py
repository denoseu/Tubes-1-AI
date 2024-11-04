from Algorithms.strategy import AlgorithmStrategy
from plot import PlotManager
import numpy as np
import time

class StochasticStrategy(AlgorithmStrategy):
    def execute(self, cube, max_steps=1500000):
        start_time = time.time()
        
        current_score = cube.getCurrentScore()
        steps = 0
        scores = [current_score]
        iterations = []

        while steps < max_steps:
            steps += 1
            # Choose two random positions to swap
            pos1 = tuple(np.unravel_index(np.random.randint(0, cube.n**3), (cube.n, cube.n, cube.n)))
            pos2 = tuple(np.unravel_index(np.random.randint(0, cube.n**3), (cube.n, cube.n, cube.n)))

            cube.swap_elements(pos1, pos2)
            new_score = cube.getCurrentScore()

            # If the swap improves the score, accept it; otherwise, revert it
            if new_score > current_score:
                current_score = new_score
            else:
                cube.swap_elements(pos1, pos2)
            
            iterations.append((cube.cube.copy(), current_score))
            scores.append(current_score)

            print(f"Step {steps} | Pos1: {pos1} <-> Pos2: {pos2} | Current Score: {current_score}")

        end_time = time.time()
        total_time = end_time - start_time
        final_score = current_score
        total_iterations = steps

        plot_manager = PlotManager(scores)
        plot_manager.plot_objective_function(total_iterations=total_iterations, total_time=total_time, final_score=final_score)

        return cube.cube, final_score, iterations
