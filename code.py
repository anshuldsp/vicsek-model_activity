import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import hsv_to_rgb

# Parameters
N = 500                # Number of particles
L = 10.0               # Box size (LxL)
v0 = 0.2               # Particle speed
eta = 0.05             # Noise strength (0 = no noise, 2*pi = random)
r = 1.0                # Interaction radius
dt = 0.5               # Time step
steps = 1              # Number of time steps


# Initialization
pos = np.random.rand(N, 2) * L
theta = np.random.rand(N) * 2 * np.pi

# Initialize figure
fig, ax = plt.subplots(figsize=(6, 6))
U, V = np.cos(theta), np.sin(theta)
colors = hsv_to_rgb(np.stack([theta / (2 * np.pi), np.ones(N), np.ones(N)], axis=1))  # HSV to RGB
sc = ax.quiver(pos[:, 0], pos[:, 1], U, V, color=colors, scale=30, width=0.003)
ax.set_xlim(0, L)
ax.set_ylim(0, L)
plt.xticks([])
plt.yticks([])
ax.set_aspect('equal')
#ax.set_title("Vicsek Model (Color = Angle)")

def update():
    global pos, theta

    # Vectorized pairwise distance with periodic BCs
    dpos = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
    dpos -= L * np.round(dpos / L)
    dist2 = np.sum(dpos**2, axis=-1)
    mask = dist2 < r**2

    # Mean direction of neighbors
    avg_sin = mask @ np.sin(theta) / mask.sum(axis=1)
    avg_cos = mask @ np.cos(theta) / mask.sum(axis=1)
    mean_angle = np.arctan2(avg_sin, avg_cos)

    # Add angular noise
    noise = eta * (np.random.rand(N) - 0.5) * 2 * np.pi
    theta[:] = mean_angle + noise

    # Update positions with new direction
    pos[:, 0] += v0 * np.cos(theta) * dt
    pos[:, 1] += v0 * np.sin(theta) * dt
    pos %= L  # Periodic BCs

def animate(frame):
    update()
    U, V = np.cos(theta), np.sin(theta)
    colors = hsv_to_rgb(np.stack([theta / (2 * np.pi) % 1.0, np.ones(N), np.ones(N)], axis=1))
    sc.set_offsets(pos)
    sc.set_UVC(U, V)
    sc.set_color(colors)
    return sc,

ani = FuncAnimation(fig, animate, frames=steps, interval=30, blit=False)
ani.save("animation.gif", fps=30, dpi=100, writer='pillow')  # Or writer='imagemagick'

plt.show()