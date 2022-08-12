import pygame
import random

import World

WIDTH = 500
HEIGHT = 500
DEPTH = 500

pygame.init()

random.seed(42)

screen = pygame.display.set_mode([WIDTH, HEIGHT])

running = True

w = World.World(WIDTH, HEIGHT, DEPTH)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    w.update()
    w.draw(screen)
    pygame.display.flip()

pygame.quit()
