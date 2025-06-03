import pygame
import sys
from GameManager import Game
from UI.Menu import Menu
from UI.Options import Options
from UI.GameOver import GameOver
from Player import Player

class StageManager:
    def __init__(self, screen, player, gamemap):
        self.screen = screen
        self.player = player
        self.menu = Menu(screen)
        self.map = gamemap
        self.game = Game(screen,player)
        self.options = Options(screen, player)
      #  self.gameover = None
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
          #  if new_stage == "gameover":
           #     self.gameover = GameOver(self.screen,self.game.elapsed_time)
            self.stage = new_stage
        #elif self.stage == "gameover":
         #   new_stage = self.gameover.update(events)
          #  self.stage = new_stage



        elif self.stage == "options":
            result = self.options.update(events)  # result to np. "Creepy", "Szczescie", "Gorycz", "menu" lub "options"


            if result == "Creepy":
                self.player.music = 1
                self.stage = "options"
            elif result == "Przyjaciele":
                self.player.music = 2
                self.stage = "options"
            elif result == "Femboye":
                self.player.music = 3
                self.stage = "options"
            elif result == "menu":
                self.stage = "menu"
            else:
                self.stage = result