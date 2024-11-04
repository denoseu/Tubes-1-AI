import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class CubeDisplayManager:
    def __init__(self, initial_cube, final_cube):
        self.cube_size = 5  # Fixed size for 5x5x5 cube
        self.initial_cube = initial_cube
        self.final_cube = final_cube
        self.colors = ['red', 'green', 'blue', 'purple', 'orange']

        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.title("Initial and Final Cube Visualization")

        # Create matplotlib figure with two subplots side by side
        self.fig = plt.figure(figsize=(10, 5))
        
        # Create two subplots
        self.ax1 = self.fig.add_subplot(121, projection='3d')  # Left subplot
        self.ax2 = self.fig.add_subplot(122, projection='3d')  # Right subplot
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        # Add rotation controls
        # self.setup_controls()
        
        # Display both cubes
        self.update_display()


    def update_view(self, _):
        """Update the view angles based on slider values"""
        elev = self.elev_slider.get()
        azim = self.azim_slider.get()
        
        # Update both subplot views
        # self.ax1.view_init(elev=elev, azim=azim)
        # self.ax2.view_init(elev=elev, azim=azim)
        self.canvas.draw()

    def draw_single_cube(self, ax, cube, title):
        """Helper function to draw a single cube"""
        ax.cla()

        # Draw cube values
        for x in range(self.cube_size):
            for y in range(self.cube_size):
                for z in range(self.cube_size):
                    value = cube[x, y, z]
                    ax.text(x, y, z, str(value), color=self.colors[x % len(self.colors)], ha='center', va='center')

        # Draw grid lines
        for i in range(self.cube_size):
            for j in range(self.cube_size):
                ax.plot([i, i], [j, j], [0, self.cube_size-1], 'gray', alpha=0.2)
                ax.plot([i, i], [0, self.cube_size-1], [j, j], 'gray', alpha=0.2)
                ax.plot([0, self.cube_size-1], [i, i], [j, j], 'gray', alpha=0.2)

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        ax.set_xlim([0, self.cube_size - 1])
        ax.set_ylim([0, self.cube_size - 1])
        ax.set_zlim([0, self.cube_size - 1])
        ax.set_title(title)

    def update_display(self):
        """Display both 3D cubes"""
        # Draw initial cube on left subplot
        self.draw_single_cube(self.ax1, self.initial_cube, 'Initial Cube State')
        
        # Draw final cube on right subplot
        self.draw_single_cube(self.ax2, self.final_cube, 'Final Cube State')

        # Set initial view angles for both plots
        # self.ax1.view_init(elev=30, azim=45)
        # self.ax2.view_init(elev=30, azim=45)
        
        # Adjust layout to prevent overlap
        self.fig.tight_layout()
        
        self.canvas.draw()

    def start(self):
        """Start the Tkinter main loop"""
        self.root.mainloop()