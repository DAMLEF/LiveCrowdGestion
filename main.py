# Bibliothèques
import pygame
import sys

# ----------- #

SIZE = (1280, 720)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("LiveCrowdGestion")

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False