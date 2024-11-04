from strategy import AlgorithmStrategy
from plot import PlotManager
import numpy as np

class StochasticStrategy(AlgorithmStrategy):
    def execute(self, cube, max_steps=100):
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
            
            iterations.append((cube.cube.copy(),current_score))

            print(f"Step {steps} | Pos1: {pos1} <-> Pos2: {pos2} | Current Score: {current_score}")

            scores.append(current_score)
    
        plot_manager = PlotManager()
        plot_manager.plot_objective_function(scores)

        return cube.cube, current_score, iterations