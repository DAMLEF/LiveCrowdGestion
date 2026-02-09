from polygon import Polygon

import math

class Agent:
    def __init__(self):
        self.pos = [0, 0]



        self.objective: Polygon = None

        # Self properties
        self.mass = 80

        self.reaction_time = 0.0001                       # In sec
        self.desired_velocity = 2.5                     # In m/s (vi0)

        self.repulsion_amplitude = 2000                 # In Newton
        self.repulsion_characteristic_distance = 0.08   # In meter

        self.contact_stiffness = 120000                 # In kg/s²

        self.damping_reverse_speed = 4                  # In m/s
        self.gamma_damping = 1000                       # In kg/s

        self.sliding_friction_coefficient = 240000        # In kg/(m.s)

        # --------

        # Physics properties

        self.force = [0., 0.]

        self.acceleration = [0., 0.]
        self.velocity = [0., 0.]

        # -----------------

    def init_agent(self, objective: Polygon):
        self.objective = objective

    def actualise(self, delta_time: float):

        self.acceleration[0] = self.force[0] / self.mass
        self.acceleration[1] = self.force[1] / self.mass

        print("Vitesse : ", math.sqrt(self.velocity[0]**2 + self.velocity[1]**2))

        self.velocity[0] += self.acceleration[0] * delta_time
        self.velocity[1] += self.acceleration[1] * delta_time

        self.pos[0] += self.velocity[0] * delta_time
        self.pos[1] += self.velocity[1] * delta_time

        self.force = [0, 0]



