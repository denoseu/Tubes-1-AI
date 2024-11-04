import matplotlib.pyplot as plt
import numpy as np

class PlotManager:
    def __init__(self, scores=None, acceptance_probs=None):
        self.scores = scores if scores is not None else []
        self.acceptance_probs = acceptance_probs if acceptance_probs is not None else []

    def plot_objective_function(self, total_iterations=None, total_time=None, final_score=None):
        plt.figure(figsize=(10, 6))
        plt.plot(self.scores)
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Score')
        
        title = 'Objective Function Score vs Iteration'
        if final_score is not None:
            title += f" | Final Score: {final_score}"
        plt.title(title)
        
        textstr = f'Total Iterations: {total_iterations}\nTotal Time: {total_time:.2f} seconds'
        plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes,
                       fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        plt.show()

    def plot_sideways_strategy(self, total_iterations, total_time, max_sideways, final_score):
        plt.figure(figsize=(10, 6))
        plt.plot(self.scores, label="Score over Iterations")
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Score')
        
        title = f'Objective Function Score vs Iteration (Sideways Strategy)\nFinal Score: {final_score}'
        plt.title(title)
        
        textstr = (f'Total Iterations: {total_iterations}\n'
                   f'Total Time: {total_time:.2f} seconds\n'
                   f'Number of Sideways Moves Done: {max_sideways}')
        plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes,
                       fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        plt.legend()
        plt.show()

    def plot_objective_function_simulated(self, total_iterations, total_time, final_score, stuck_frequency):
        plt.figure(figsize=(10, 6))
        plt.plot(self.scores, label="Objective Function Score")
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Score')
        
        title = f'Simulated Annealing: Objective Function vs Iteration\nFinal Score: {final_score}'
        plt.title(title)
        
        textstr = (f'Total Iterations: {total_iterations}\n'
                   f'Total Time: {total_time:.2f} seconds\n'
                   f'Frequency of Getting Stuck: {stuck_frequency}')
        plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes,
                       fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        plt.legend()
        plt.show()

    def plot_acceptance_probability(self):
        window_size = 200
        smoothed_probs = np.convolve(self.acceptance_probs, np.ones(window_size)/window_size, mode='valid')
        plt.plot(smoothed_probs)
        plt.xlabel('Iterations')
        plt.ylabel('Acceptance Probability')
        plt.title('Acceptance Probability vs Iterations')
        plt.show()

    def plot_multiple_objective_functions(self, all_scores):
        plt.figure(figsize=(10, 6))
        for i, scores in enumerate(all_scores):
            plt.plot(scores, label=f'Restart {i + 1}')
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function Score')
        plt.title('Objective Function Score vs. Iterations for Each Restart')
        plt.legend()
        plt.show()
    
    def plot_acceptance_simulated_annealing(self):
        if self.acceptance_probs is not None:
            self.plot_acceptance_probability()

    def plot_random_restart_summary(self, all_scores, restart_times, restart_iterations, final_exec_time):
        plt.figure(figsize=(12, 8))
        
        for i, scores in enumerate(all_scores):
            max_score = max(scores)
            plt.plot(scores, label=f'Restart {i + 1} (Max Score: {max_score}, Time: {restart_times[i]:.2f}s, Iterations: {restart_iterations[i]})')

        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Score')
        plt.title('Objective Function Score Across Random Restarts')
        
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=8)
        plt.tight_layout()
        
        textstr = f'Total Execution Time: {final_exec_time:.2f} seconds'
        plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes,
                    fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        plt.show()


    def plot_genetic_algorithm(self, max_fitness, avg_fitness, total_time):
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(max_fitness) + 1), max_fitness, label="Max Fitness", color="blue")
        plt.plot(range(1, len(avg_fitness) + 1), avg_fitness, label="Average Fitness", color="green")
        plt.xlabel("Generation (Iteration)")
        plt.ylabel("Fitness (Objective Function)")
        plt.title("Maximum and Average Fitness over Generations")
        plt.legend()
        plt.grid()

        textstr = f'Total Execution Time: {total_time:.2f} seconds'
        plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes,
                    fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        plt.show()
