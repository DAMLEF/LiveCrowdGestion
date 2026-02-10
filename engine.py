# Bibliothèques
import math
from typing import List, Tuple

import pygame.draw
from PIL.ImageChops import screen

from entrance import Entrance
from polygon import Polygon
from tools.all import *
from math_utils import *

from world import *
from camera import Camera
from obstacle import Obstacle
from agent import Agent
from objective import Objective


# --------------- #

class Engine:
    SIZE = (1280, 720)
    FPS = 144

    WINDOW_NAME = "LiveCrowdGestion"

    FPS_DEBUG = True

    PLACEMENT_ROTATION_OPTION = "ROTATION"
    PLACEMENT_WIDTH_EXTENSION = "WIDTH_EXTENSION"
    PLACEMENT_HEIGHT_EXTENSION = "HEIGHT_EXTENSION"
    PLACEMENT_OPTIONS = {PLACEMENT_ROTATION_OPTION: PLACEMENT_ROTATION_OPTION,
                         PLACEMENT_WIDTH_EXTENSION: PLACEMENT_WIDTH_EXTENSION,
                         PLACEMENT_HEIGHT_EXTENSION: PLACEMENT_HEIGHT_EXTENSION}

    INPUT_CAMERA_LEFT = pygame.K_q
    INPUT_CAMERA_RIGHT = pygame.K_d
    INPUT_CAMERA_UP = pygame.K_z
    INPUT_CAMERA_DOWN = pygame.K_s

    INPUT_ROTATE_MODE_ITEM = pygame.K_r
    INPUT_WIDTH_MODE_ITEM = pygame.K_w
    INPUT_HEIGHT_MODE_ITEM = pygame.K_h

    def __init__(self):
        self.screen = pygame.display.set_mode(Engine.SIZE)

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps = Engine.FPS
        self.delta = 0

        self.mouse_pos = (0, 0)

        self.camera = Camera((300, 300))

        self.world = World()

        # World Structure
        self.entrances: list = []
        self.obstacles: list = []
        self.spawn_points: list = []
        self.objective: Polygon = None
        self.agents: list = []

        # Simulation parameters
        self.agents_to_spawn = 500
        self.time_between_agent_spawn = 2        # In sec
        self.last_spawn_time = time.time()

        # Editor parameters
        self.edit = True

        self.buttons = []

        action_obstacle_placement = lambda: self.set_placement_mode(Obstacle())
        action_entrance_placement = lambda: self.set_placement_mode(Entrance())
        action_objective_placement = lambda: self.set_placement_mode(Objective())
        action_sp_placement = lambda: self.set_placement_mode(Polygon("SP", GOLD))

        self.buttons.append(
            TextButton(10, 10, 110, 30, "Obstacle", BaseStyle(15, BLACK), "OBSTACLE", action=action_obstacle_placement,
                       reset_input=True))
        self.buttons.append(
            TextButton(130, 10, 110, 30, "Entrance", BaseStyle(15, BLACK), "ENTRANCE", action=action_entrance_placement,
                       reset_input=True))
        self.buttons.append(
            TextButton(250, 10, 110, 30, "SP", BaseStyle(15, BLACK), "SPAWN POINT", action=action_sp_placement,
                       reset_input=True))
        self.buttons.append(TextButton(370, 10, 110, 30, "Objective", BaseStyle(15, BLACK), "OBJECTIVE",
                                       action=action_objective_placement, reset_input=True))

        self.placement: Polygon = None
        self.placement_option = Engine.PLACEMENT_OPTIONS[Engine.PLACEMENT_ROTATION_OPTION]

        self.placement_rotation_speed = 5  # degrees per frame
        self.placement_length_extension_speed = 2  # degrees per frame

    def display(self):
        self.screen.fill(WHITE)

        # Draw of the map boundaries
        world_start_pos = (0, 0)
        world_end_pos = self.world.get_world_size()
        pygame.draw.rect(self.screen, BLACK, (
            self.world_to_screen_pos(world_start_pos), self.world.worldVector_to_pixelVector(world_end_pos)), 2)

        # Draw all entrances
        for entrance in self.entrances:
            points = self.world_to_screen_list(entrance.points)

            pygame.draw.polygon(self.screen, entrance.color, points)

        # Draw all obstacles
        for obstacle in self.obstacles:
            points = self.world_to_screen_list(obstacle.points)

            pygame.draw.polygon(self.screen, obstacle.color, points)

        # Draw Objective
        if self.objective is not None:
            objective_ponts = self.world_to_screen_list(self.objective.points)
            pygame.draw.polygon(self.screen, self.objective.color, objective_ponts)

        # Draw Spawn-Point
        for spawn_point in self.spawn_points:
            spawn_point = self.world_to_screen_pos(spawn_point)

            pygame.draw.circle(self.screen, GOLD, spawn_point, self.world.world_to_pixel(0.3))

        # Draw agents
        for agent in self.agents:
            pygame.draw.circle(self.screen, LIGHT_RED, self.world_to_screen_pos(agent.pos),
                               self.world.agent_radius * self.world.meter)

        # TODO : Debug
        if self.obstacles and False:
            obstacles_world_position = self.world_to_screen_list(self.obstacles[0].points)
            d, impact = nearest_impact_point_polygon(self.agents[0].pos, obstacles_world_position)

            pygame.draw.line(self.screen, GREEN, impact, self.agents[0].pos, 1)

        # Edit interface section
        if self.edit:

            # Draw of the in placement element
            if self.placement is not None:
                points = self.placement.get_rectangle_points(self.mouse_pos[0], self.mouse_pos[1])

                pygame.draw.polygon(self.screen, self.placement.color, points)

                # Draw Interface value
                ts = BaseStyle(15, LIGHT_GREY)

                self.screen.blit(ts.render(
                    f"WIDTH [{key_input[Engine.INPUT_WIDTH_MODE_ITEM]}] : {round(self.world.pixel_to_world(self.placement.w), 3)} m"),
                    (Engine.SIZE[0] * 0.05, Engine.SIZE[1] * 0.45))
                self.screen.blit(ts.render(
                    f"HEIGHT [{key_input[Engine.INPUT_HEIGHT_MODE_ITEM]}] : {round(self.world.pixel_to_world(self.placement.h), 3)} m"),
                    (Engine.SIZE[0] * 0.05, Engine.SIZE[1] * 0.45 + 15))
                self.screen.blit(ts.render(
                    f"ROTATION [{key_input[Engine.INPUT_ROTATE_MODE_ITEM]}] : {round(self.world.pixel_to_world(self.placement.angle), 3)} °"),
                    (Engine.SIZE[0] * 0.05, Engine.SIZE[1] * 0.45 + 30))

            for button in self.buttons:
                button.draw(self.screen)

            # Draw Graphic scale
            pygame.draw.rect(self.screen, LIGHT_GREY,
                             (Engine.SIZE[0] * 0.05, Engine.SIZE[1] * 0.95, self.world.meter, 5))
            self.screen.blit(BaseStyle(10, LIGHT_GREY).render("Meter"),
                             (Engine.SIZE[0] * 0.05, Engine.SIZE[1] * 0.95 + 10))

        pygame.display.flip()

    def actualise(self):
        input_actualise()
        self.delta = self.clock.get_time() / 1000
        self.mouse_pos = input_info["M_POS"]

        # We move the camera within the window space when the user presses the movement keys.
        camera_vector = [0, 0]
        if input_info.get(Engine.INPUT_CAMERA_UP):
            camera_vector[1] += 1
        if input_info.get(Engine.INPUT_CAMERA_LEFT):
            camera_vector[0] -= 1
        if input_info.get(Engine.INPUT_CAMERA_DOWN):
            camera_vector[1] -= 1
        if input_info.get(Engine.INPUT_CAMERA_RIGHT):
            camera_vector[0] += 1

        self.camera.move(tuple(camera_vector), self.delta)

        if self.edit:
            if input_info.get(pygame.K_l):
                self.edit = False

            if self.placement is not None:

                if input_info.get(Engine.INPUT_ROTATE_MODE_ITEM):
                    self.placement_option = Engine.PLACEMENT_OPTIONS[Engine.PLACEMENT_ROTATION_OPTION]
                elif input_info.get(Engine.INPUT_WIDTH_MODE_ITEM):
                    self.placement_option = Engine.PLACEMENT_OPTIONS[Engine.PLACEMENT_WIDTH_EXTENSION]
                elif input_info.get(Engine.INPUT_HEIGHT_MODE_ITEM):
                    self.placement_option = Engine.PLACEMENT_OPTIONS[Engine.PLACEMENT_HEIGHT_EXTENSION]

                if self.placement_option == Engine.PLACEMENT_ROTATION_OPTION:
                    self.placement.angle += input_info["MW_2f"] * self.placement_rotation_speed
                elif self.placement_option == Engine.PLACEMENT_WIDTH_EXTENSION:
                    self.placement.w += input_info["MW_2f"] * self.placement_length_extension_speed
                elif self.placement_option == Engine.PLACEMENT_HEIGHT_EXTENSION:
                    self.placement.h += input_info["MW_2f"] * self.placement_length_extension_speed

                if input_info.get("LMB"):
                    polygon_world_positions = self.screen_to_world_list(
                        self.placement.get_rectangle_points(self.mouse_pos[0], self.mouse_pos[1]))

                    self.placement.confirm_position(polygon_world_positions)

                    if self.placement.polygon_type == "Obstacle":
                        self.obstacles.append(self.placement)
                    elif self.placement.polygon_type == "Entrance":
                        self.entrances.append(self.placement)
                    elif self.placement.polygon_type == "Objective":
                        self.objective = self.placement
                    elif self.placement.polygon_type == "SP":
                        world_pos = self.screen_to_world_pos(self.mouse_pos)
                        self.spawn_points.append((world_pos[0], world_pos[1]))

                    self.placement = None

            for button in self.buttons:
                button.actualise()
        else:

            if len(self.agents) < self.agents_to_spawn:
                if time.time() - self.last_spawn_time >= self.time_between_agent_spawn:
                    new_agent = Agent()

                    new_agent.init_agent(self.objective)

                    # TODO : Manage multi Spawn Point
                    if len(self.spawn_points) > 0:
                        new_agent.pos = [self.spawn_points[0][0], self.spawn_points[0][1]]
                    else:
                        # Agent will spawn in world at position [0, 0]
                        pass

                    self.agents.append(new_agent)

                    self.last_spawn_time = time.time()

            self.compute_forces()

            for agent in self.agents:
                agent.actualise(self.delta)

        if Engine.FPS_DEBUG:
            pygame.display.set_caption(f"{Engine.WINDOW_NAME} - FPS : {self.clock.get_fps()}")
        else:
            pygame.display.set_caption(f"{Engine.WINDOW_NAME}")

    def world_to_screen_pos(self, pos: tuple):
        # We take a position in world space (expressed in meters) and map it to screen space for rendering.
        pixel_pos = self.world.worldVector_to_pixelVector(pos)
        return self.camera.apply_offset(pixel_pos)

    def world_to_screen_list(self, points: List[tuple]) -> List[tuple]:
        result = []
        for point in points:
            result.append(self.world_to_screen_pos(point))

        return result

    def screen_to_world_pos(self, pos: tuple):
        reverted_camera_pos = self.camera.revert_offset(pos)
        return self.world.pixelVector_to_worldVector(reverted_camera_pos)

    def screen_to_world_list(self, points: List[tuple]) -> List[tuple]:
        result = []

        for point in points:
            result.append(self.screen_to_world_pos(point))

        return result

    def set_placement_mode(self, placement_polygon: Polygon):
        self.placement = placement_polygon

    def compute_forces(self):
        # This function updates the forces of all agents on the scene according to the obstacles and their current objective.

        for a in self.agents:
            # Driving forces

            objective_point = nearest_impact_point_polygon(a.pos, a.objective.points)[1]

            # Normalize direction
            agent_direction = normalize([objective_point[0] - a.pos[0], objective_point[1] - a.pos[1]])

            driving_force = [0, 0]
            driving_force[0] = (a.desired_velocity * agent_direction[0] - a.velocity[0]) / a.reaction_time
            driving_force[1] = (a.desired_velocity * agent_direction[1] - a.velocity[1]) / a.reaction_time

            obstacle_force = [0, 0]
             # TODO: Éviterr que la distance passe à zéro pour éviter l'explosion exponentielle
            for obstacle in self.obstacles:
                obstacle_impact_info = nearest_impact_point_polygon(a.pos, obstacle.points)

                obstacle_impact_distance = obstacle_impact_info[0]
                obstacle_impact_point = obstacle_impact_info[1]

                obstacle_agent_direction = normalize(
                    [a.pos[0] - obstacle_impact_point[0],  a.pos[1] - obstacle_impact_point[1]])

                # Pushing
                obstacle_force[0] += (a.repulsion_amplitude * math.exp(
                    (self.world.agent_radius - obstacle_impact_distance) / a.repulsion_characteristic_distance)
                                      + a.contact_stiffness * ramp(
                            self.world.agent_radius - obstacle_impact_distance)) * obstacle_agent_direction[0]
                obstacle_force[1] += (a.repulsion_amplitude * math.exp(
                    (self.world.agent_radius - obstacle_impact_distance) / a.repulsion_characteristic_distance)
                                      + a.contact_stiffness * ramp(
                            self.world.agent_radius - obstacle_impact_distance)) * obstacle_agent_direction[1]

                # Sliding
                tangential_oa_direction = normalize([-obstacle_agent_direction[1], obstacle_agent_direction[0]])
                sliding_dot = dot(a.velocity, tangential_oa_direction)

                obstacle_force[0] -= a.sliding_friction_coefficient * ramp(
                    self.world.agent_radius - obstacle_impact_distance) * sliding_dot * tangential_oa_direction[0]
                obstacle_force[1] -= a.sliding_friction_coefficient * ramp(
                    self.world.agent_radius - obstacle_impact_distance) * sliding_dot * tangential_oa_direction[1]

            repulsive_force = [0, 0]
            for other_agent in self.agents:
                if other_agent != a:
                    agent_to_other_direction = [a.pos[0] - other_agent.pos[0], a.pos[1] - other_agent.pos[1]]
                    distance_agent_to_other = norm(agent_to_other_direction)

                    agent_to_other_direction = normalize(agent_to_other_direction)

                    radius_agent_and_other = 2 * self.world.agent_radius

                    # Pushing
                    repulsive_force[0] += (a.repulsion_amplitude * math.exp(
                        (radius_agent_and_other - distance_agent_to_other) / a.repulsion_characteristic_distance)
                                           + a.contact_stiffness * ramp(
                                radius_agent_and_other - distance_agent_to_other)) * agent_to_other_direction[0]
                    repulsive_force[1] += (a.repulsion_amplitude * math.exp(
                        (radius_agent_and_other - distance_agent_to_other) / a.repulsion_characteristic_distance)
                                           + a.contact_stiffness * ramp(
                                radius_agent_and_other - distance_agent_to_other)) * agent_to_other_direction[1]

                    # Sliding
                    tangential_ao_direction = normalize([- agent_to_other_direction[1], agent_to_other_direction[0]])
                    velocity_difference = [a.velocity[0] - other_agent.velocity[0],
                                           a.velocity[1] - other_agent.velocity[1]]
                    sliding_dot = dot(velocity_difference, tangential_ao_direction)

                    repulsive_force[0] -= a.sliding_friction_coefficient * ramp(
                        radius_agent_and_other - distance_agent_to_other) * sliding_dot * tangential_ao_direction[0]
                    repulsive_force[1] -= a.sliding_friction_coefficient * ramp(
                        radius_agent_and_other - distance_agent_to_other) * sliding_dot * tangential_ao_direction[1]

            damping_force = [0, 0]
            # TODO
            if norm(a.velocity) > a.damping_reverse_speed and False:
                damping_force[0] -= a.gamma_damping * a.velocity[0]
                damping_force[1] -= a.gamma_damping * a.velocity[1]

            a.force[0] += driving_force[0] + obstacle_force[0] + repulsive_force[0] + damping_force[0]
            a.force[1] += driving_force[1] + obstacle_force[1] + repulsive_force[1] + damping_force[1]
            print(a.pos)
            pass

    def app_loop(self):
        running = True

        while running:

            self.display()
            self.actualise()

            for event in pygame.event.get():
                check_input(event)

                if event.type == pygame.QUIT:
                    running = False

            self.clock.tick(self.fps)
