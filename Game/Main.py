import sys

import pygame

from Game.Map import Map
from Game.Player import Player
from Game.StageManager import StageManager
from Game.SaveAndLoad import *

pygame.init()

def Main():
    '''Metoda ta inicializuje grę, tworzy ekran, gracza, mapę i menedżera etapu, a następnie rozpoczyna główną pętlę gry.'''
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