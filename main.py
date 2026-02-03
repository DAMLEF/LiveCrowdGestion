# Bibliothèques
from engine import *
# ----------- #

E = Engine()


running = True
while running:
    E.display()
    E.actualise()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    E.clock.tick(E.fps)