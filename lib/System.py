import math


class System:
  def __init__(
      self,
      radius=0.001,  # cross section area of the moving body in m2
      Cd=0.47,  # drag coefficient, 0.47 for a sphere
      rho=1.225,  # density of the fluid (kg/m3)
      mass=0.01,  # mass of the moving body (kg),
      initial_velocity=[0, 0, 0],  # initial velocity of the moving body (m/s)
      initial_position=[0, 0, 0],  # initial position of the moving body (m)
      wind_force=[0, 0, 0],  # wind force (m/s2)
      delta_t=0.0001,  # time step (s)
      g=9.81,  # gravity
      target_coordinate=[0, 0, -100],  # target coordinate (m)
      target_radius=0.1,  # target radius (m)
  ):
    self.radius = radius
    self.area = math.pi * (radius ** 2) / 2
    self.Cd = Cd
    self.rho = rho
    self.g = g
    self.mass = mass
    self.wind_force = wind_force
    self.weight_force = [0, 0, -mass * g]  # weight force (m/s2)
    self.delta_t = delta_t

    self.F = [
        wind_force[0] + self.weight_force[0],
        wind_force[1] + self.weight_force[1],
        wind_force[2] + self.weight_force[2],
    ]
    self.initial_velocity = initial_velocity
    self.initial_position = initial_position

    self.current_speed = initial_velocity
    self.current_position = initial_position

    self.time_in_air = 0
    self.trajectory = []
    self.speeds = []

    self.target_coordinate = target_coordinate
    self.target_radius = target_radius
    self.hit_target = False
    self.hit_speed = 0
    self.hit_time = 0

    self.find_trajectory()

  def find_trajectory(self):
    while True:
      current_speed = self.new_speed(self.current_speed)
      current_position = [
          self.current_position[0] + current_speed[0] * self.delta_t,
          self.current_position[1] + current_speed[1] * self.delta_t,
          self.current_position[2] + current_speed[2] * self.delta_t,
      ]

      self.current_speed = current_speed

      if self.touching_target(current_position) and not self.hit_target:
        self.hit_target = True
        self.hit_speed = current_speed
        self.hit_time = self.time_in_air

      if current_position[2] < 0:
        break

      self.current_speed = current_speed
      self.current_position = current_position
      self.trajectory.append(self.current_position)
      self.speeds.append(self.current_speed)
      self.time_in_air += self.delta_t

  @property
  def final_position(self):
    return self.current_position

  @property
  def final_speed(self):
    return self.current_speed

  def touching_target(self, current_position):
    x, y, z = current_position
    x_target, y_target, z_target = self.target_coordinate
    r = math.sqrt(
        (x - x_target) ** 2
        + (y - y_target) ** 2
        + (z - z_target) ** 2
    )
    return r < self.target_radius + self.radius

  def new_speed(self, prev_speed):
    Vx, Vy, Vz = prev_speed
    Fx, Fy, Fz = self.F
    V = math.sqrt(Vx ** 2 + Vy ** 2 + Vz ** 2)
    Vx_new = Vx + (Fx - Vx * V * self.area * self.Cd *
                   self.rho * 0.5) * self.delta_t / self.mass
    Vy_new = Vy + (Fy - Vy * V * self.area * self.Cd *
                   self.rho * 0.5) * self.delta_t / self.mass
    Vz_new = Vz + (Fz - Vz * V * self.area * self.Cd *
                   self.rho * 0.5) * self.delta_t / self.mass
    return [Vx_new, Vy_new, Vz_new]
