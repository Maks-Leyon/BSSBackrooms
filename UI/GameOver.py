import pygame
from UI import Button
from Game.Settings import *

class GameOver:
    def __init__(self, screen,time):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)

        szer, wys = 250, 60
        x = screen.get_width() // 2 - 130
        y = 200
        self.buttons = [
            Button.Button((x, y + 200, szer, wys), "Menu")
        ]


        self.time = time
        self.min = self.time // 60000
        self.sec = (self.time % 60000) // 1000
        self.ms = self.time % 1000


    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()



        for button in self.buttons:
            button.update(mouse_pos) #dla kazdej pozycji sprawdzane czy myszka ni jest na guziku


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #jednorazowo za kazda proba klikniecia
                for button in self.buttons:
                    if button.is_clicked(mouse_pos, mouse_pressed):
                        print("fueah")
                        return button.text

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        self.draw()
        return "gamover" # jak nic sie nie zemin to zostjamy w options

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("GOAT!", True, GREEN)
        self.screen.blit(text, (100, 100))

        time_text = f"Czas gry: {self.min:02}:{self.sec:02}:{self.ms:02}"
        time_surface = self.font.render(time_text, True, WHITE)
        self.screen.blit(time_surface, (100, 200))

        for button in self.buttons:
            button.draw(self.screen)
