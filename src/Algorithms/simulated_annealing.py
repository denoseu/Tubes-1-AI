import numpy as np
from Algorithms.strategy import AlgorithmStrategy
import math
import time
from plot import PlotManager

class SimulatedAnnealingStrategy(AlgorithmStrategy):
    def execute(self, cube, initial_temp=1000, cooling_rate=0.9999):
        start_time = time.time()
        current_score = cube.getCurrentScore()
        print(f"Initial score: {current_score}")
        temperature = initial_temp
        scores = [current_score]
        acceptance_probs = []
        iterations = []
    
        iteration = 0
        stuck_frequency = 0

        while temperature > 1e-3 and current_score != 0:
            iteration += 1
            
            pos1, pos2 = self._get_random_positions(cube.n)
            cube.swap_elements(pos1, pos2)
            new_score = cube.getCurrentScore()
            delta_score = new_score - current_score

            accepted_with_probability = False
            accepted = False
            
            if delta_score > 0:
                accepted = True
            else:
                acceptance_probability = math.exp(delta_score / temperature)
                acceptance_probs.append(acceptance_probability)
                accepted_with_probability = np.random.rand() < acceptance_probability
            
            if accepted_with_probability:
                stuck_frequency += 1

            if accepted or accepted_with_probability:
                current_score = new_score
            else:
                cube.swap_elements(pos1, pos2)

            temperature *= cooling_rate
            scores.append(current_score)
            iterations.append((cube.cube.copy(), current_score))

        end_time = time.time()
        total_time = end_time - start_time
        total_iterations = iteration
        final_score = current_score

        plot_manager = PlotManager(scores, acceptance_probs)
        plot_manager.plot_objective_function_simulated(
            total_iterations=total_iterations,
            total_time=total_time,
            final_score=final_score,
            stuck_frequency=stuck_frequency
        )
        plot_manager.plot_acceptance_simulated_annealing()
        
        return cube.cube, current_score, iterations

    def _get_random_positions(self, n):
        pos1 = tuple(np.unravel_index(np.random.randint(0, n**3), (n, n, n)))
        pos2 = tuple(np.unravel_index(np.random.randint(0, n**3), (n, n, n)))
        return pos1, pos2
