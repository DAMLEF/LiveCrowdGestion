# Bibliothèques
import world
from tools.all import *

from world import *
from camera import Camera

# --------------- #

class Engine:

    SIZE = (1280, 720)
    FPS = 144

    WINDOW_NAME = "LiveCrowdGestion"

    FPS_DEBUG = True

    def __init__(self):
        self.screen = pygame.display.set_mode(Engine.SIZE)

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.camera = Camera()

        self.world = World()

        self.obstacles: list = []
        self.agents: list = []

        self.fps = Engine.FPS
        self.delta = 0


    def display(self):
        self.screen.fill(WHITE)

        # Draw of the map boundaries
        world_start_pos = (0, 0)
        world_end_pos = self.world.get_world_size()
        pygame.draw.rect(self.screen, BLACK, (self.world_to_screen_pos(world_start_pos), self.world.worldVector_to_pixelVector(world_end_pos)), 2)

        pygame.display.flip()

    def actualise(self):
        input_actualise()

        self.delta = self.clock.get_time() / 1000

        # We move the camera within the window space when the user presses the movement keys.
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

        if Engine.FPS_DEBUG:
            pygame.display.set_caption(f"{Engine.WINDOW_NAME} - FPS : {self.clock.get_fps()}")
        else:
            pygame.display.set_caption(f"{Engine.WINDOW_NAME}")

    def world_to_screen_pos(self, pos: tuple):
        # We take a position in world space (expressed in meters) and map it to screen space for rendering.
        pixel_pos = self.world.worldVector_to_pixelVector(pos)
        return self.camera.apply_offset(pixel_pos)

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





