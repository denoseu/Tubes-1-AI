import numpy as np
from strategy import AlgorithmStrategy
import math

class SimulatedAnnealingStrategy(AlgorithmStrategy):
    def execute(self, cube, initial_temp=1000, cooling_rate=0.9999):
        current_score = cube.getCurrentScore()
        temperature = initial_temp
        iterations = []

        while temperature > 1e-3:
            
            pos1, pos2 = self._get_random_positions(cube.n)
            cube.swap_elements(pos1, pos2)
            new_score = cube.getCurrentScore()
            delta_score = new_score - current_score

            if delta_score > 0 or math.exp(delta_score / temperature) > np.random.rand():
                current_score = new_score
            else:
                cube.swap_elements(pos1, pos2)

            temperature *= cooling_rate
            iterations.append((cube.cube.copy(), current_score))

        return cube.cube, current_score, iterations

    def _get_random_positions(self, n):
        pos1 = tuple(np.unravel_index(np.random.randint(0, n**3), (n, n, n)))
        pos2 = tuple(np.unravel_index(np.random.randint(0, n**3), (n, n, n)))
        return pos1, pos2
