import matplotlib.pyplot as plt

class PlotManager:
    def __init__(self, scores, acceptance_probs=None):
        self.scores = scores
        self.acceptance_probs = acceptance_probs

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

    def plot_all(self):
        plt.figure(figsize=(12, 5))
        
        # Plot the objective function score
        # plt.subplot(1, 2, 1)
        self.plot_objective_function()

        # Plot acceptance probability only if available (for simulated annealing)
        if self.acceptance_probs is not None:
            # plt.subplot(1, 2, 2)
            self.plot_acceptance_probability()
        
        plt.tight_layout()
        plt.show()
