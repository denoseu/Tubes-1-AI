import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class AnimationManager:
    def __init__(self, cube_size, iterations):
        self.cube_size = cube_size
        self.iterations = iterations
        self.colors = ['red', 'green', 'blue', 'purple', 'orange']
        self.current_frame = 0
        self.playback_speed = 1.0
        self.is_playing = False

        self.root = tk.Tk()
        self.root.title("Local Search Visualisation")

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.setup_controls()
        self.update_cube(self.current_frame)  

    def setup_controls(self):
        """Initialize playback controls."""
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack()

        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT)

        self.progress_bar = tk.Scale(self.controls_frame, from_=0, to=len(self.iterations) - 1,
                                     orient=tk.HORIZONTAL, command=self.on_progress_change, label="Progress")
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add an Entry widget to allow direct frame input
        self.frame_entry = tk.Entry(self.controls_frame, width=5)
        self.frame_entry.insert(0, str(self.current_frame))
        self.frame_entry.bind("<Return>", self.on_frame_entry)
        self.frame_entry.pack(side=tk.LEFT)


        speed_label = tk.Label(self.controls_frame, text="Speed:")
        speed_label.pack(side=tk.LEFT)

        self.speed_slider = tk.Scale(self.controls_frame, from_=0.5, to=10.0, resolution=0.5,
                                     orient=tk.HORIZONTAL, label="Speed", command=self.update_speed)
        self.speed_slider.set(self.playback_speed)
        self.speed_slider.pack(side=tk.LEFT)

    def update_speed(self, value):
        """Update playback speed based on slider value."""
        self.playback_speed = float(value)

    def update_cube(self, frame):
        """Update the 3D cube display for a given frame."""
        self.ax.cla() 
        current_cube = self.iterations[frame][0]

        for x in range(self.cube_size):
            for y in range(self.cube_size):
                for z in range(self.cube_size):
                    value = current_cube[x, y, z]
                    self.ax.text(x, y, z, str(value), color=self.colors[x % len(self.colors)], ha='center', va='center')

        # Set labels, limits, and title for clarity
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_zlabel('Z-axis')
        self.ax.set_xlim([0, self.cube_size - 1])
        self.ax.set_ylim([0, self.cube_size - 1])
        self.ax.set_zlim([0, self.cube_size - 1])
        self.ax.set_title(f'Cube Iteration: {frame + 1}/{len(self.iterations)}')

        self.ax.text2D(0.5, 0.95, f'Current Score: {self.iterations[frame][1]}', transform=self.ax.transAxes, ha='center', fontsize=12)
        
        self.canvas.draw()

    def play(self):
        """Start playing the animation."""
        self.is_playing = True
        self.play_button.config(text="Pause", command=self.pause)
        self.animate()

    def pause(self):
        """Pause the animation."""
        self.is_playing = False
        self.play_button.config(text="Play", command=self.play)

    def animate(self):
        """Animation loop to handle each frame."""
        if self.is_playing:
            self.update_cube(self.current_frame)
            self.current_frame = (self.current_frame + int(self.playback_speed)) % len(self.iterations)
            self.progress_bar.set(self.current_frame)
            self.root.after(int(100 / self.playback_speed), self.animate)

    def on_progress_change(self, value):
        """Update the plot when the progress slider is changed."""
        self.current_frame = int(value)
        self.update_cube(self.current_frame)

    def on_frame_entry(self, event):
        """Handle direct frame input from the entry box."""
        try:
            frame = int(self.frame_entry.get())
            if 0 <= frame < len(self.iterations):
                self.current_frame = frame
                self.progress_bar.set(frame)  # Sync the slider with the entered frame
                self.update_cube(self.current_frame)  # Refresh the cube display
            else:
                print("Frame out of range.")
        except ValueError:
            print("Invalid frame number entered.")

    def start_animation(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()