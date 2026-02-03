from tools.all import *


class Engine:

    SIZE = (1280, 720)
    FPS = 144

    WINDOW_NAME = "LiveCrowdGestion"

    FPS_DEBUG = True

    def __init__(self):
        self.screen = pygame.display.set_mode(Engine.SIZE)

        self.clock: pygame.time.Clock = pygame.time.Clock()


        self.obstacles: list = []
        self.agents: list = []

        self.fps = Engine.FPS


    def display(self):
        self.screen.fill(WHITE)

        pygame.display.flip()

    def actualise(self):
        if Engine.FPS_DEBUG:
            pygame.display.set_caption(f"{Engine.WINDOW_NAME} - FPS : {self.clock.get_fps()}")
        else:
            pygame.display.set_caption(f"{Engine.WINDOW_NAME}")





