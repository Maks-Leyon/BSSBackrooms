import pygame
import sys
from GameManager import Game
from UI.Menu import Menu
from UI.Options import Options

class StageManager:
    def __init__(self, screen):
        self.screen = screen
        self.menu = Menu(screen)
        self.game = Game(screen)
        self.options = Options(screen)
        self.stage = "menu"

    def update(self, events, clock):
        if self.stage == "menu":
            action = self.menu.update(events)
            if action == "Start":
                self.stage = "game"
            elif action == "Options":

                self.stage = "options"
            elif action == "Exit":
                pygame.quit()
                sys.exit()

        elif self.stage == "game":
            new_stage = self.game.update(events, clock)
            self.stage = new_stage


        elif self.stage == "options":
            new_stage = self.options.update(events)
            self.stage = new_stage