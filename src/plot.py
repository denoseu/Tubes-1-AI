import matplotlib.pyplot as plt

class PlotManager:
    def __init__(self, scores=None, acceptance_probs=None):
        self.scores = scores if scores is not None else []
        self.acceptance_probs = acceptance_probs if acceptance_probs is not None else []

    def plot_objective_function(self, total_iterations=None, total_time=None, final_score=None):
        plt.figure(figsize=(10, 6))
        plt.plot(self.scores)
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Score')
        
        # Include the score, iteration, and time in the title or as text
        title = 'Objective Function Score vs Iteration'
        if final_score is not None:
            title += f" | Final Score: {final_score}"
        plt.title(title)
        
        # Display additional details as annotations on the plot
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

    def plot_acceptance_probability(self):
        plt.plot(self.acceptance_probs)
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
    
    def plot_simulated_annealing(self):
        # Plot the objective function score
        self.plot_objective_function()

        # Plot acceptance probability only if available (for simulated annealing)
        if self.acceptance_probs is not None:
            self.plot_acceptance_probability()

    def plot_genetic_algorithm(self, max_fitness, avg_fitness):
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(max_fitness) + 1), max_fitness, label="Max Fitness", color="blue")
        plt.plot(range(1, len(avg_fitness) + 1), avg_fitness, label="Average Fitness", color="green")
        plt.xlabel("Generation (Iteration)")
        plt.ylabel("Fitness (Objective Function)")
        plt.title("Maximum and Average Fitness over Generations")
        plt.legend()
        plt.grid()
        plt.show()
