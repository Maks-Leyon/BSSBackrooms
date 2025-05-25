import sys

import pygame

from Player import Player
from Renderer import Renderer
from StageManager import StageManager

pygame.init()

Player = Player()
Renderer = Renderer(pygame)
# Stworzony DrawManager dla poukładania

def Main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Miki i Maksiu <333333")
    clock = pygame.time.Clock()



    stage_manager = StageManager(screen)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        fps = clock.tick(60)
        stage_manager.update(events, fps)


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    Main()