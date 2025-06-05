
import pygame
from UI.Button import Button
from Game.Settings import *
from Game.SaveAndLoad import *

class Ranking:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 60)
        self.szer, self.wys = 250, 60
        self.x = self.screen.get_width() // 2 - self.szer // 2
        self.y = 200
        self.buttons = [
            Button((self.x - 265, self.y + 340, 120, 50), "Back")
        ]

    def update(self, events):
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
        return "ranking"

    def draw(self):
        self.screen.fill((0, 0, 0))
        label = self.font.render("Biggest Goats", True, WHITE)
        self.screen.blit(label, (200, 20))


        top5 = SaveAndLoad.loadInfo()
        font = pygame.font.SysFont("Arial", 30)
        y_offset = 120
        for i, (nick, time) in enumerate(top5):
            minutes = time // 60000
            seconds = (time % 60000) // 1000
            milliseconds = time % 1000
            text = f"{i + 1}. {nick} - {minutes}:{seconds:02d}.{milliseconds:03d}"
            label = font.render(text, True, WHITE)


            self.screen.blit(label, (260, y_offset))
            y_offset += 70

        for button in self.buttons:
            button.draw(self.screen)


        pygame.display.flip()