import sys

import pygame

from Map import Map
from Player import Player
from Renderer import Renderer
from StageManager import StageManager
from SaveAndLoad import *

pygame.init()
Renderer = Renderer(pygame)

def Main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Miki i Maksiu <333333")
    clock = pygame.time.Clock()


    gamemap = Map()
    p = Player(gamemap)
    stage_manager = StageManager(screen, p, gamemap)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                SaveAndLoad.saveGame(stage_manager.game)
                running = False
        fps = clock.tick(60)
        stage_manager.update(events, fps)


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    Main()