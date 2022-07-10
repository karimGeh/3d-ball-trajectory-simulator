from lib.System import System
import matplotlib.pyplot as plt
import numpy as np

# this delta_t is the time step of the simulation it
# the much smaller the delta_t the more accurate the simulation
# but the more time it takes to run the simulation
delta_t = 0.001

# this is the wind force that is applied to the system (ball)
# we suppose that the wind force is uniformly distributed
# notice that the wind force have its own formula based on
#  - wind speed
#  - air pressure
#  - air density
#  - area facing the wind which is the cross section area of the ball
#  - drag coefficient
#  - mass of the ball
# notice that the force applied at two different balls will be different
# even if they have the same wind speed and air pressure and air density
# if the two balls has different section or different weight
# conclusion: the wind force should be calculated to each ball separately
wind_force = [0.1, -0.01, 0]

# ball information
initial_position = [0, 0, 2]  # initial position of the ball (m)
initial_velocity = [0, 50, 50]  # initial velocity of the moving body (m/s)
mass = 0.01  # kg
radius = 10 * (10 ** -2)  # cm -> m  (100 cm = 1 m)

# target information
target_coordinate = [2, 5, 5.3]  # target coordinate (m)
target_radius = 0.1  # target radius (m)

# initializing the system (the ball)
ball = System(
    # simulation parameters
    delta_t=delta_t,
    wind_force=wind_force,
    Cd=0.47,  # drag coefficient
    rho=1.225,  # density of the fluid (kg/m3)
    g=9.81,  # gravity

    # ball information
    initial_velocity=initial_velocity,
    initial_position=initial_position,
    mass=mass,
    radius=radius,

    # target information
    target_coordinate=target_coordinate,
    target_radius=target_radius,
)

# get the trajectory of the ball as a numpy array of coordinates
trajectory = np.array(ball.trajectory)

# save the trajectory to a file
path_to_trajectory_file = "files/trajectory.txt"
with open(path_to_trajectory_file, 'w') as f:
  for i, position in enumerate(trajectory):
    f.write(f"{i}: {position}\n")


# notice that the trajectory could contain too many points
# which may slow down the graph plotting
# so we need to reduce the number of points
# we can do this by defining the number of points we want to plot
# and then we can plot the trajectory using the following code
number_of_points = 1000
step = max(1, int(trajectory.shape[0] / number_of_points))
trajectory = trajectory[::step]

# hit the target
# we can use the following code to check if the ball hit the target
hit_target = ball.hit_target  # boolean
hit_speed = ball.hit_speed  # speed of the ball at the time of hitting the target
hit_time = ball.hit_time  # time in air at the time of hitting the target

print("hit_target:", hit_target)
if hit_target:
  print("hit_speed:", hit_speed)
  print("hit_time:", hit_time)


# plot the trajectory of the ball in the 3d space
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(
    trajectory[:, 0],
    trajectory[:, 1],
    trajectory[:, 2],
    s=1,
    color="red"
)


# show the target
# the dimension of the target in the plot is not real
# we can use the following code to show the target
ax.scatter(
    [target_coordinate[0]],
    [target_coordinate[1]],
    [target_coordinate[2]],
    s=100,
    color="blue"
)

ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_zlabel("z (m)")
ax.set_title("Trajectory of the ball")

plt.show()
