import pygame
from Button import Button
from Settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        szer, wys = 250, 60
        x = screen.get_width() // 2 - 130
        y = 200


        self.buttons = [
            Button((x, y, szer, wys), "Start"),Button((x, y + 100,szer,wys ), "Options"),Button((x, y + 200,szer,wys ), "Exit"),
        ]

        self.font = pygame.font.SysFont(None, 60)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()


        for button in self.buttons:
            button.update(mouse_pos) #dla kazdej pozycji sprawdzane czy myszka ni jest na guziku


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #jednorazowo za kazda proba klikniecia
                for button in self.buttons:
                    if button.is_clicked(mouse_pos, mouse_pressed):
                        return button.text

        self.draw()
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surf = self.font.render("A zrobiles konwertery", True, WHITE)
        self.screen.blit(title_surf, (self.screen.get_width() // 2 - title_surf.get_width() // 2, 100))

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()