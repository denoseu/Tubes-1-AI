import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Given 5x5x5 numpy array representing the cube
cube = np.array([
    [[12, 82, 34, 87, 100], [25, 16, 80, 104, 90], [42, 111, 85, 2, 75], [121, 108, 7, 20, 59], [67, 18, 119, 106, 5]],
    [[91, 77, 71, 6, 70], [52, 64, 117, 69, 13], [30, 118, 21, 123, 23], [26, 39, 92, 44, 114], [116, 17, 14, 73, 95]],
    [[47, 61, 45, 76, 86], [107, 43, 38, 33, 94], [89, 68, 63, 58, 37], [32, 93, 88, 83, 19], [56, 120, 55, 49, 35]],
    [[31, 53, 112, 109, 10], [115, 98, 4, 1, 97], [103, 3, 105, 8, 96], [113, 57, 9, 62, 74], [40, 50, 81, 65, 79]],
    [[66, 72, 27, 102, 48], [29, 28, 122, 125, 11], [51, 15, 41, 124, 84], [36, 110, 46, 22, 101], [78, 54, 99, 24, 60]]
])

# Step 1: Convert to Hash Map
cube_hash_map = {(x, y, z): cube[x, y, z] for x in range(5) for y in range(5) for z in range(5)}

# Step 2: Visualize in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set up colors for each layer (arbitrary choice to differentiate layers)
colors = ['red', 'green', 'blue', 'purple', 'orange']

# Plot each number in its (x, y, z) location
for (x, y, z), value in cube_hash_map.items():
    ax.text(x, y, z, str(value), color=colors[x], ha='center', va='center')

# Set labels and title for clarity
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('3D Magic Cube Visualization')

# Set the aspect ratio and limits for clarity
ax.set_box_aspect([1,1,1])
ax.set_xlim([0, 4])
ax.set_ylim([0, 4])
ax.set_zlim([0, 4])

plt.show()
