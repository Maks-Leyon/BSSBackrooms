import pygame

from Game.Settings import WHITE,RED
from UI.Button import Button
from Game import Settings

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.szer, self.wys = 250, 60
        self.x = self.screen.get_width() // 2 - self.szer // 2  # Wyśrodkowanie buttonow
        self.y = self.screen.get_height() // 4

        self.back = pygame.image.load("Assets/Textures/pjatkKoniec.png")
        self.back = pygame.transform.scale(self.back, (self.screen.get_width(), self.screen.get_height()))

        self.buttons = [
            Button((self.x, self.y +50, self.szer, self.wys), "Start"),
            Button((self.x, self.y + 150, self.szer, self.wys), "Options"),
            Button((self.x, self.y + 250, self.szer, self.wys), "Exit")
        ]

        self.font = pygame.font.Font("Assets/Fonts/AlumniSansSC-Italic.ttf", 60)
        self.fontAuthors = pygame.font.Font("Assets/Fonts/AlumniSansSC-Italic.ttf",30)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()


        for button in self.buttons:
            button.update(mouse_pos)


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #jednorazowo za kazda proba klikniecia
                for button in self.buttons:
                    if button.is_clicked(mouse_pos, mouse_pressed):
                        return button.text

        self.draw()
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.back, (0,0))
        title_surf = self.font.render("BSS Backrooms", True, WHITE)
        authors = self.fontAuthors.render("By Stulejon&MikseGame04",True,RED)
        self.screen.blit(title_surf, (self.screen.get_width() // 2 - title_surf.get_width() // 2, 100))
        self.screen.blit(authors, (self.screen.get_width() // 2 , 150))

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()