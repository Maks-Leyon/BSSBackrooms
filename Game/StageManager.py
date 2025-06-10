import pygame
from Game.GameManager import Game
from UI.Menu import Menu
from UI.Options import Options
from Game.SaveAndLoad import *
from UI.GameOver import GameOver
from UI.HowToPlay import HowToPlay
from UI.GameStart import GameStart
from UI.Ranking import Ranking
from UI.RealGameOver import RealGameOver

class StageManager:
    def __init__(self, screen, player, gamemap):
        self.screen = screen
        self.player = player
        self.menu = Menu(screen)
        self.map = gamemap
        self.game = Game(screen,player)
        self.options = Options(screen, player)
        self.how_to_play = HowToPlay(screen)
        self.game_start = GameStart(screen)
        self.ranking = Ranking(screen)
        self.gameover = None # daje none bo z poczatku nie jest potrzebny, czyt nie zajmujemy wiecej zasobow a czasmi i tak laguje
        self.gameLose = None
        self.stage = "Menu"
        self.gg = False

        self.need_reset = False # potrzebny przy gameover



    def update(self, events, clock):
        '''Metoda ta jest odpowiedzialana za zarzadzanie stanem gry, odpowiada za zarządzanie obecnym stanem gry i odpowiada za przejscia miedzy roznymi stanami gry'''
        if self.stage == "Menu":
            action = self.menu.update(events)
            if action == "Start":
                self.stage = "game_start"
            elif action == "Options":
                self.stage = "options"
            elif action == "Exit":
                SaveAndLoad.saveGame(self.game)
                pygame.quit()

        elif self.stage == "game_start":
            action = self.game_start.update(events)
            if action == "Load":
                SaveAndLoad.loadGame(self.game)
                self.stage = "game"
            elif action == "Start":
                #jesli jest paused time, to usuwamy go od tickow zeby ustawic nowy start dzieki czemu czas nie wzrasta podczas pauzy
                if self.game.paused_time:
                    self.game.start = pygame.time.get_ticks() - self.game.paused_time
                pygame.mixer.Channel(0).set_volume(0.5)
                if self.need_reset:
                    self.game.reset()
                    self.need_reset = False
                self.stage = "game"
            elif action == "Reset":
                self.game.reset()
                self.need_reset = False
            elif action == "Menu":
                self.stage = "Menu"
            elif action == "ranking":
                self.stage = "ranking"
            elif action == "Back":
                self.stage = "Menu"

        elif self.stage == "game":
            new_stage = self.game.update(events, clock)
            if new_stage == "gameover":

                self.gameover = GameOver(self.screen, self.game.elapsed_time)
                self.stage = "gameover"
            elif new_stage == "gameLose":

                self.gameLose = RealGameOver(self.screen, self.game.elapsed_time)
                self.stage = "gameLose"

            self.stage = new_stage

        elif self.stage == "gameover":
            new_stage = self.gameover.update(events)
            if new_stage == "Menu":
                self.need_reset = True  # Potrzebujemy resetu, aby zacząć nową grę
            self.stage = new_stage

        elif self.stage == "gameLose":
            new_stage = self.gameLose.update(events)
            if new_stage == "Menu":
                self.need_reset = True
            self.stage = new_stage

        elif self.stage == "options":
            result = self.options.update(events)
            if result == "how_to_play":
                self.stage = "how_to_play"



            if result == "Creepy":
                self.player.music = 1
                self.stage = "options"
            elif result == "Friends":
                self.player.music = 2
                self.stage = "options"
            elif result == "Femboys":
                self.player.music = 3
                self.stage = "options"
            elif result == "ASD":
                self.player.music = 4
                self.stage = "options"
            elif result == "Back":
                self.stage = "Menu"
            else:
                self.stage = result

        elif self.stage == "how_to_play":
            res = self.how_to_play.update(events)
            if res == "Back":
                self.stage = "options"

        elif self.stage == "ranking":
            res = self.ranking.update(events)
            if res == "Back":
                self.stage = "game_start"


