import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Simulate cube transformations (replace this with your actual transformation data)
iterations = [np.random.randint(1, 125, (5, 5, 5)) for _ in range(50)]  # 50 frames of random states

# Colors for each layer
colors = ['red', 'green', 'blue', 'purple', 'orange']

# Initialize Tkinter root window
root = tk.Tk()
root.title("3D Cube Replay Player")

# Set up the Matplotlib figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Control variables
current_frame = tk.IntVar(value=0)
playback_speed = tk.DoubleVar(value=1.0)
is_playing = False

def update_cube(frame):
    """Update function to render each cube state."""
    ax.cla()  # Clear the previous plot

    # Get the current cube state
    current_cube = iterations[frame]

    # Plot each number in its (x, y, z) location
    for x in range(5):
        for y in range(5):
            for z in range(5):
                value = current_cube[x, y, z]
                ax.text(x, y, z, str(value), color=colors[x], ha='center', va='center')

    # Set labels, limits, and title for clarity
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_xlim([0, 4])
    ax.set_ylim([0, 4])
    ax.set_zlim([0, 4])
    ax.set_title(f'Cube Iteration: {frame + 1}/{len(iterations)}')
    canvas.draw()

def play():
    """Start playing the animation."""
    global is_playing
    is_playing = True
    play_button.config(text="Pause", command=pause)
    animate()

def pause():
    """Pause the animation."""
    global is_playing
    is_playing = False
    play_button.config(text="Play", command=play)

def animate():
    """Animation loop to handle each frame."""
    global is_playing
    if is_playing:
        frame = current_frame.get()
        update_cube(frame)

        # Move to the next frame based on playback speed
        next_frame = (frame + int(playback_speed.get())) % len(iterations)
        current_frame.set(next_frame)

        # Schedule the next frame
        root.after(int(100 / playback_speed.get()), animate)

def on_progress_change(value):
    """Update the plot when the progress slider is changed."""
    update_cube(int(value))

# Playback controls
controls_frame = tk.Frame(root)
controls_frame.pack()

play_button = tk.Button(controls_frame, text="Play", command=play)
play_button.pack(side=tk.LEFT)

progress_bar = tk.Scale(controls_frame, from_=0, to=len(iterations) - 1,
                        orient=tk.HORIZONTAL, variable=current_frame,
                        command=on_progress_change, label="Progress")
progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

speed_label = tk.Label(controls_frame, text="Speed:")
speed_label.pack(side=tk.LEFT)

speed_slider = tk.Scale(controls_frame, from_=0.1, to=3.0, resolution=0.1,
                        orient=tk.HORIZONTAL, variable=playback_speed, label="Speed")
speed_slider.pack(side=tk.LEFT)

# Initialize the first frame
update_cube(current_frame.get())

# Run the Tkinter main loop
root.mainloop()
