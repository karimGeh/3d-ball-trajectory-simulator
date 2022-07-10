from lib.System import System
import matplotlib.pyplot as plt
import numpy as np


# you can add or change colors with hexa decimal colors like this: '#ff0000' = red
colors = ["red", "green", "blue", "orange", "purple", "black", "brown", "pink"]

delta_t = 0.001

# simulate two identical balls with only difference being mass
balls = [
    # ball 1
    System(
        # simulation parameters
        delta_t=delta_t,
        wind_force=[0.1, -0.01, 0],

        # ball information
        initial_velocity=[0, 50, 50],
        initial_position=[0, 0, 2],
        mass=0.01,
        radius=0.05,
    ),
    # ball 2
    System(
        # simulation parameters
        delta_t=delta_t,
        wind_force=[0.05, -0.005, 0],

        # ball information
        initial_velocity=[0, 50, 50],
        initial_position=[0, 0, 2],
        mass=0.02,
        radius=0.05,
    ),
]


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

number_of_points = 1000
for i, ball in enumerate(balls):
  trajectory = np.array(ball.trajectory)
  step = max(1, int(trajectory.shape[0] / number_of_points))
  trajectory_simple = trajectory[::step]

  ax.scatter(
      trajectory_simple[:, 0],
      trajectory_simple[:, 1],
      trajectory_simple[:, 2],
      s=1,
      color=colors[i]
  )

ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_zlabel("z (m)")
ax.set_title("Trajectory of the ball")

plt.show()
