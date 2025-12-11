import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
g = 9.81  # gravity (m/s^2)

def simulate_no_drag(v0, angle, dt=0.01):
    theta = np.radians(angle)
    vx, vy = v0 * np.cos(theta), v0 * np.sin(theta)
    x, y = [0], [0]
    while y[-1] >= 0:
        x.append(x[-1] + vx * dt)
        vy -= g * dt
        y.append(y[-1] + vy * dt)
    return np.array(x), np.array(y)

def simulate_with_drag(v0, angle, m=1.0, c=0.1, dt=0.01):
    theta = np.radians(angle)
    vx, vy = v0 * np.cos(theta), v0 * np.sin(theta)
    x, y = [0], [0]
    while y[-1] >= 0:
        ax = -(c/m) * vx
        ay = -g - (c/m) * vy
        vx += ax * dt
        vy += ay * dt
        x.append(x[-1] + vx * dt)
        y.append(y[-1] + vy * dt)
    return np.array(x), np.array(y)

# Parameters
v0 = 50      # initial speed (m/s)
angle = 45   # launch angle (degrees)

# Simulations
x1, y1 = simulate_no_drag(v0, angle)
x2, y2 = simulate_with_drag(v0, angle, m=1.0, c=0.2)

# Plot comparison
plt.figure(figsize=(8,6))
plt.plot(x1, y1, label="No Drag")
plt.plot(x2, y2, label="With Drag")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Projectile Motion Comparison")
plt.legend()
plt.grid(True)
plt.show()

# Animation
fig, ax = plt.subplots(figsize=(8,6))
ax.set_xlim(0, max(x1.max(), x2.max())*1.1)
ax.set_ylim(0, max(y1.max(), y2.max())*1.1)
line1, = ax.plot([], [], 'r-', label="No Drag")
line2, = ax.plot([], [], 'b-', label="With Drag")
point1, = ax.plot([], [], 'ro')
point2, = ax.plot([], [], 'bo')
ax.legend()

def update(frame):
    if frame < len(x1):
        line1.set_data(x1[:frame], y1[:frame])
        point1.set_data(x1[frame], y1[frame])
    if frame < len(x2):
        line2.set_data(x2[:frame], y2[:frame])
        point2.set_data(x2[frame], y2[frame])
    return line1, line2, point1, point2

ani = FuncAnimation(fig, update, frames=max(len(x1), len(x2)), interval=20, blit=True)
plt.show()