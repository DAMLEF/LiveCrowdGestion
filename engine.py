# Bibliothèques
from typing import List, Tuple

from entrance import Entrance
from polygon import Polygon
from tools.all import *
from math_utils import *

from world import *
from camera import Camera
from obstacle import Obstacle
from agent import Agent

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

    def __init__(self):
        self.screen = pygame.display.set_mode(Engine.SIZE)

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps = Engine.FPS
        self.delta = 0

        self.mouse_pos = (0, 0)

        self.camera = Camera((300, 300))

        self.world = World()

        # World Structure
        self.entrances: list =  []
        self.obstacles: list = []
        self.spawn_point: list = []
        self.objective: Polygon = None
        self.agents: list = [Agent()]


        # Editor parameters
        self.edit = True

        self.buttons = []

        action_obstacle_placement = lambda: self.set_placement_mode(Obstacle())
        action_entrance_placement = lambda: self.set_placement_mode(Entrance())

        self.buttons.append(TextButton(10, 10, 110, 30, "Obstacle", BaseStyle(15, BLACK), "OBSTACLE", action=action_obstacle_placement, reset_input=True))
        self.buttons.append(TextButton(130, 10, 110, 30, "Entrance", BaseStyle(15, BLACK), "ENTRANCE", action=action_entrance_placement, reset_input=True))
        self.buttons.append(TextButton(250, 10, 110, 30, "Obstacle", BaseStyle(15, BLACK), "SPAWN POINT", reset_input=True))
        self.buttons.append(TextButton(370, 10, 110, 30, "Entrance", BaseStyle(15, BLACK), "OBJECTIVE", reset_input=True))

        self.placement: Polygon = None
        self.placement_option = Engine.PLACEMENT_OPTIONS[Engine.PLACEMENT_ROTATION_OPTION]

        self.placement_rotation_speed = 5   # degrees per frame
        self.placement_length_extension_speed = 2  # degrees per frame


    def display(self):
        self.screen.fill(WHITE)

        # Draw of the map boundaries
        world_start_pos = (0, 0)
        world_end_pos = self.world.get_world_size()
        pygame.draw.rect(self.screen, BLACK, (self.world_to_screen_pos(world_start_pos), self.world.worldVector_to_pixelVector(world_end_pos)), 2)

        # Draw all entrances
        for entrance in self.entrances:
            points = self.world_to_screen_list(entrance.points)

            pygame.draw.polygon(self.screen, GREEN, points)

        # Draw all obstacles
        for obstacle in self.obstacles:
            points = self.world_to_screen_list(obstacle.points)

            pygame.draw.polygon(self.screen, BLACK, points)

        # Draw agents
        for agent in self.agents:
            pygame.draw.circle(self.screen, LIGHT_RED, agent.pos, self.world.agent_radius * self.world.meter)

        # TODO : Debug
        if self.obstacles:
            obstacles_world_position = self.world_to_screen_list(self.obstacles[0].points)
            d, impact = nearest_impact_point_polygon(self.agents[0].pos, obstacles_world_position)

            pygame.draw.line(self.screen, GREEN, impact, self.agents[0].pos, 1)

        # Edit interface section
        if self.edit:

            # Draw of the in placement element
            if self.placement is not None:
                points = self.placement.get_rectangle_points(self.mouse_pos[0], self.mouse_pos[1])

                pygame.draw.polygon(self.screen, BLACK, points)

            for button in self.buttons:
                button.draw(self.screen)

            # Draw Graphic scale
            pygame.draw.rect(self.screen, LIGHT_GREY, (Engine.SIZE[0] * 0.05, Engine.SIZE[1] * 0.95, self.world.meter, 5))
            self.screen.blit(BaseStyle(10, LIGHT_GREY).render("Meter"), (Engine.SIZE[0] * 0.05, Engine.SIZE[1] * 0.95 + 10))

        pygame.display.flip()

    def actualise(self):
        input_actualise()
        self.delta = self.clock.get_time() / 1000
        self.mouse_pos = input_info["M_POS"]

        # We move the camera within the window space when the user presses the movement keys.
        # TODO: Manage KEY_INTERACTION
        camera_vector = [0, 0]
        if input_info.get(pygame.K_z):
            camera_vector[1] += 1
        if input_info.get(pygame.K_q):
            camera_vector[0] -= 1
        if input_info.get(pygame.K_s):
            camera_vector[1] -= 1
        if input_info.get(pygame.K_d):
            camera_vector[0] += 1

        self.camera.move(tuple(camera_vector), self.delta)

        if self.placement is not None:

            if input_info.get(pygame.K_r):
                self.placement_option = Engine.PLACEMENT_OPTIONS[Engine.PLACEMENT_ROTATION_OPTION]
            elif input_info.get(pygame.K_w):
                self.placement_option = Engine.PLACEMENT_OPTIONS[Engine.PLACEMENT_WIDTH_EXTENSION]
            elif input_info.get(pygame.K_h):
                self.placement_option = Engine.PLACEMENT_OPTIONS[Engine.PLACEMENT_HEIGHT_EXTENSION]

            if self.placement_option == Engine.PLACEMENT_ROTATION_OPTION:
                self.placement.angle += input_info["MW_2f"] * self.placement_rotation_speed
            elif self.placement_option == Engine.PLACEMENT_WIDTH_EXTENSION:
                self.placement.w += input_info["MW_2f"] * self.placement_length_extension_speed
            elif self.placement_option == Engine.PLACEMENT_HEIGHT_EXTENSION:
                self.placement.h += input_info["MW_2f"] * self.placement_length_extension_speed

            if input_info.get("LMB"):
                polygon_world_positions = self.screen_to_world_list(self.placement.get_rectangle_points(self.mouse_pos[0], self.mouse_pos[1]))

                self.placement.confirm_position(polygon_world_positions)

                if self.placement.polygon_type == "Obstacle":
                    self.obstacles.append(self.placement)
                elif self.placement.polygon_type == "Entrance":
                    self.entrances.append(self.placement)

                self.placement = None

        if self.edit:
            for button in self.buttons:
                button.actualise()

        # TODO : Debug Section
        self.agents[0].pos = [self.mouse_pos[0], self.mouse_pos[1]]

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





