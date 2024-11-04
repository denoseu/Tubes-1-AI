import matplotlib.pyplot as plt

class PlotManager:
    def __init__(self, scores=None, acceptance_probs=None):
        self.scores = scores if scores is not None else []
        self.acceptance_probs = acceptance_probs if acceptance_probs is not None else []

    def plot_objective_function(self):
        plt.plot(self.scores)
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Score')
        plt.title('Objective Function Score vs Iteration')
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
        # plt.subplot(1, 2, 1)
        self.plot_objective_function()

        # Plot acceptance probability only if available (for simulated annealing)
        if self.acceptance_probs is not None:
            # plt.subplot(1, 2, 2)
            self.plot_acceptance_probability()
