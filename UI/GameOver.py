import pygame
from UI import Button
from Game.Settings import *

class GameOver:
    def __init__(self, screen,elapsed_time):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)

        szer, wys = 250, 60
        x = screen.get_width() // 2 - 130
        y = 200
        self.buttons = [
            Button.Button((x, y + 200, szer, wys), "Menu")
        ]


        self.elapsed_time = elapsed_time
        self.min = self.elapsed_time // 60000
        self.sec = (self.elapsed_time % 60000) // 1000
        self.ms = self.elapsed_time % 1000


    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()



        for button in self.buttons:
            button.update(mouse_pos)


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #jednorazowo za kazda proba klikniecia
                for button in self.buttons:
                    if button.is_clicked(mouse_pos, mouse_pressed):
                        print("fueah")
                        print(button.text)
                        return button.text

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        self.draw()
        return "gameover"

    def draw(self):
        self.screen.fill((0, 0, 0))
        win_text = self.font.render("WYGRANA!", True, GREEN)
        self.screen.blit(win_text, (self.screen.get_width() // 2 - win_text.get_width() // 2, 100))

        time_text = f"Czas : {self.min:02}:{self.sec:02}:{self.ms:03}"
        time_surface = self.font.render(time_text, True, WHITE)
        self.screen.blit(time_surface, (self.screen.get_width() // 2 - time_surface.get_width() // 2, 200))

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()