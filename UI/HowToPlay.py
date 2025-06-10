import pygame
from UI.Button import Button
from Game.Settings import *


class HowToPlay:
    '''Ta klasa reprezentuje Podsekcje klasy Options - a dokladniej sterowanie, pobiera ona ekran (screen) jako argumenty inicjalizacyjne'''
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 40)
        self.szer, self.wys = 250, 60
        self.x = self.screen.get_width() // 2 - self.szer // 2
        self.y = 200
        self.buttons = [
            Button((self.x - 265, self.y + 340, 120, 50), "Back")
        ]

    def update(self, events):
        '''Metoda ta odpowaida za aktualizacje guzika czy sprawdzenia pozycji myszki w Dodatkowym oknie options'''
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
        return "how_to_play"

    def draw(self):
        '''Metoda ta odpowiada za rysowanie ekranu sterowania'''
        self.screen.fill((0, 0, 0))
        instructions_text = [
            "Sterowanie:",
            "Strzałki lewa/prawa - obrót lewo/prawo",
            "W, S - przód/tył",
            "Shift - bieg (korzysta ze staminy)",
            "E - interakcja (zebranie notatke, użycie RJ-45)",
            "N - Przegladanie notatek",
            "Esc - wyjście do menu"
        ]
        y_offset = 50
        for line in instructions_text:
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, (WIDTH * 0.1, y_offset))
            y_offset += 60
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()