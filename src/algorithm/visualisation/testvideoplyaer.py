import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Dummy data to simulate cube iterations
# Replace this with your actual iteration data
cube_iterations = [np.random.rand(5, 5) for _ in range(50)]

# Initialize Tkinter root window
root = tk.Tk()
root.title("Magic Cube Replay Player")

# Create the Matplotlib figure
fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Variables to control playback
current_frame = tk.IntVar(value=0)
playback_speed = tk.DoubleVar(value=1.0)
is_playing = False

def update_plot(frame_index):
    """Function to update the plot with the new cube state."""
    ax.clear()
    ax.imshow(cube_iterations[frame_index], cmap='viridis')  # Display the current frame
    ax.set_title(f"Frame: {frame_index}")
    canvas.draw()

def play():
    """Play the video by iterating through frames."""
    global is_playing
    is_playing = True
    play_button.config(text="Pause", command=pause)
    animate()

def pause():
    """Pause the video playback."""
    global is_playing
    is_playing = False
    play_button.config(text="Play", command=play)

def animate():
    """Animation loop for playing the frames."""
    global is_playing
    if is_playing:
        frame = current_frame.get()
        update_plot(frame)
        
        # Move to the next frame based on playback speed
        next_frame = (frame + int(playback_speed.get())) % len(cube_iterations)
        current_frame.set(next_frame)
        
        # Schedule the next update
        root.after(int(100 / playback_speed.get()), animate)

def on_progress_change(value):
    """Update the plot when the progress slider is changed."""
    update_plot(int(value))

# Playback controls
controls_frame = tk.Frame(root)
controls_frame.pack()

play_button = tk.Button(controls_frame, text="Play", command=play)
play_button.pack(side=tk.LEFT)

progress_bar = tk.Scale(controls_frame, from_=0, to=len(cube_iterations) - 1,
                        orient=tk.HORIZONTAL, variable=current_frame,
                        command=on_progress_change, label="Progress")
progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

speed_label = tk.Label(controls_frame, text="Speed:")
speed_label.pack(side=tk.LEFT)

speed_slider = tk.Scale(controls_frame, from_=0.1, to=3.0, resolution=0.1,
                        orient=tk.HORIZONTAL, variable=playback_speed, label="Speed")
speed_slider.pack(side=tk.LEFT)

# Initialize the first frame
update_plot(current_frame.get())

# Run the Tkinter main loop
root.mainloop()
