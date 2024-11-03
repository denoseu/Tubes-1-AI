from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import math
import time
import os
from cube import MagicCube

class AlgorithmManager:

    def solve(self, magic_cube, algorithm="steepest_ascent_parallel", **kwargs):
        if algorithm == "steepest_ascent":
            return self.steepest_ascent_parallel(magic_cube)
        elif algorithm == "hill_climbing_with_sideways":
            return self.hill_climbing_with_sideways(magic_cube)
        elif algorithm == "random_restart_hill_climbing":
            return self.random_restart_hill_climbing(magic_cube, **kwargs)
        elif algorithm == "simulated_annealing":
            initial_temp = kwargs.get("initial_temp", 1000)
            cooling_rate = kwargs.get("cooling_rate", 0.9999) 
            return self.simulated_annealing(magic_cube, initial_temp, cooling_rate)
        elif algorithm == "stochastic_hill_climbing":
            return self.stochastic_hill_climbing(magic_cube, **kwargs)
        else:
            raise ValueError("Invalid algorithm specified")
    
    def simulated_annealing(self, cube, initial_temp, cooling_rate):
        current_score = cube.getCurrentScore()
        temperature = initial_temp

        iteration = 0
        while temperature > 1e-3:
            iteration += 1
            # Choose two random positions for swapping
            pos1 = tuple(np.unravel_index(np.random.randint(0, cube.n**3), (cube.n, cube.n, cube.n)))
            pos2 = tuple(np.unravel_index(np.random.randint(0, cube.n**3), (cube.n, cube.n, cube.n)))

            # Swap elements and calculate new score
            cube.swap_elements(pos1, pos2)
            new_score = cube.getCurrentScore()
            delta_score = new_score - current_score

            if delta_score > 0 or math.exp(delta_score / temperature) > np.random.rand():
                current_score = new_score
            else:
                cube.swap_elements(pos1, pos2)

            temperature *= cooling_rate

            ## KALAU BUTUH DATA BUAT VISUALISASI TARUH SINI
            print(f"Iter {iteration} | Temp: {temperature:.5f} | Pos1: {pos1} <-> Pos2: {pos2} | Current Score: {current_score} | Delta: {delta_score}")

        print(f"Final Score: {current_score}")
        print(f"Final Cube:\n{cube.cube}")
        return cube.cube, current_score
    



    def steepest_ascent_parallel(self, cube):
        current_score = cube.getCurrentScore()
        improved = True

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

        return cube.cube, current_score

    
    def hill_climbing_with_sideways(self, cube):
        current_score = cube.getCurrentScore()
        improved = True

        while improved:
            improved = False
            best_score = current_score
            best_positions = None

            with ThreadPoolExecutor(os.cpu) as executor:
                futures = []
                for i in range(1, cube.n**3):
                    for j in range(i + 1, cube.n**3):
                        pos1 = cube.get_position(i)
                        pos2 = cube.get_position(j)

                        # Submit swap evaluations to the thread pool
                        futures.append(executor.submit(cube.evaluate_swap, pos1, pos2))

                for future in as_completed(futures):
                    swap_score, pos1, pos2 = future.result()
                    if swap_score >= best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)

            if best_positions:
                pos1, pos2 = best_positions
                cube.swap_elements(pos1, pos2)
                current_score = best_score
                improved = True

        return cube, current_score
     
    def random_restart_hill_climbing(self, magic_cube, max_restarts=10, max_steps=100):
        best_score = float("-inf")
        best_cube = None

        for _ in range(max_restarts):
            magic_cube.initialize_cube(magic_cube.n)
            magic_cube.initialize_sums()
            current_score = magic_cube.steepest_ascent(magic_cube, max_steps)

            if current_score > best_score:
                best_score = current_score
                best_cube = magic_cube.cube.copy()

        return best_cube, best_score

    def steepest_ascent(self, magic_cube, max_steps=100):
        current_score = magic_cube.getCurrentScore()
        steps = 0
        improved = True

        while improved and steps < max_steps:
            improved = False
            best_score = current_score
            best_positions = None
            steps += 1

            for i in range(1, magic_cube.n**3):
                for j in range(i + 1, magic_cube.n**3):
                    pos1 = magic_cube.get_position(i)
                    pos2 = magic_cube.get_position(j)

                    magic_cube.swap_elements(pos1, pos2)
                    swap_score = magic_cube.getCurrentScore()

                    if swap_score > best_score:
                        best_score = swap_score
                        best_positions = (pos1, pos2)

                    # Revert swap
                    magic_cube.swap_elements(pos1, pos2)

            if best_positions:
                pos1, pos2 = best_positions
                magic_cube.swap_elements(pos1, pos2)
                current_score = best_score
                improved = True

        return current_score

    def stochastic_hill_climbing(cube, magic_cube, max_steps=100):
        current_score = magic_cube.getCurrentScore()
        steps = 0

        while steps < max_steps:
            steps += 1
            # Choose two random positions to swap
            pos1 = tuple(np.unravel_index(np.random.randint(0, magic_cube.n**3), (magic_cube.n, magic_cube.n, magic_cube.n)))
            pos2 = tuple(np.unravel_index(np.random.randint(0, magic_cube.n**3), (magic_cube.n, magic_cube.n, magic_cube.n)))

            magic_cube.swap_elements(pos1, pos2)
            new_score = magic_cube.getCurrentScore()

            # If the swap improves the score, accept it; otherwise, revert it
            if new_score > current_score:
                current_score = new_score
            else:
                magic_cube.swap_elements(pos1, pos2)  # Revert swap

            print(f"Step {steps} | Pos1: {pos1} <-> Pos2: {pos2} | Current Score: {current_score}")

        return magic_cube.cube, current_score

    def evaluate_swap(self, magic_cube, pos1, pos2):
        magic_cube.swap_elements(pos1, pos2)
        score = magic_cube.getCurrentScore()
        magic_cube.swap_elements(pos1, pos2)
        return score, pos1, pos2


# Instantiate MagicCube and run parallelized steepest ascent
n = 5
magic_cube = MagicCube(n)
algorithm_manager = AlgorithmManager()
start_time = time.time()
final_cube, final_score = algorithm_manager.solve(magic_cube, "steepest_ascent")
end_time = time.time()
print(f"Final Cube:\n{final_cube}")
print(f"Final Score: {final_score}")
print(f"Elapsed time: {end_time - start_time:.2f} seconds")


