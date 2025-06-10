import pygame

from Game.Settings import *
from UI.Button import Button

class GameStart:
    def __init__(self, screen):
        self.screen = screen
        self.szer, self.wys = 250, 60
        self.x = self.screen.get_width() // 2 - self.szer // 2
        self.y = 200

        self.font = pygame.font.SysFont(None, 60)

        self.back = pygame.image.load("Assets/Textures/starGame.png")
        self.back = pygame.transform.scale(self.back, (self.screen.get_width(), self.screen.get_height()))

        self.buttons = [
            Button((self.x, self.y, self.szer, self.wys), "Start"),
            Button((self.x, self.y + 100, self.szer, self.wys), "Load"),
            Button((self.x, self.y + 200, self.szer, self.wys), "Reset"),
            Button((self.x + 65, self.y + 300, 120, 50), "ranking"),
            Button((self.x - 265 , self.y + 340, 120, 50), "Back")
        ]

    def update(self, events):
        '''Metoda ta odpowaida za aktualizacje guzikow czy sprawdzenia pozycji myszki w głównym oknie startu Gry (UI)'''
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()




        for button in self.buttons:
            button.update(mouse_pos)


        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "Menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.is_clicked(mouse_pos, mouse_pressed):
                        return button.text



        self.draw()
        return "game_start"

    def draw(self):
        '''Metoda ta odpowaida za rysowanie ekranu MENU gry'''
        self.screen.fill((0, 0, 0))
        offset = 200
        self.screen.blit(self.back, (offset, 0))
        title_surf = self.font.render("GRAJ", True, WHITE)
        self.screen.blit(title_surf, (self.screen.get_width() // 2 - title_surf.get_width() // 2, 100))
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()