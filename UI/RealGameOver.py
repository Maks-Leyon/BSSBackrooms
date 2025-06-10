import pygame
from UI.Button import Button
from Game.Settings import *
from Game.SaveAndLoad import *

class RealGameOver:
    def __init__(self, screen,elapsed_time):


        self.screen = screen



        self.note_bg = pygame.image.load("Assets/Textures/note_base.png") # fake notatka
        self.font = pygame.font.Font("Assets/Fonts/messy.ttf", 30)


        szer, wys = 250, 60
        x = screen.get_width() // 2 - 130
        y = 100
        self.buttons = [
            Button((x, y + 300, szer, wys), "Menu")
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
                        print(button.text)
                        return button.text



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Menu"



        self.draw()

        return "gameLose"

    def draw(self):
        '''AGHAFRASDFADSFSDAFADFDAFASD'''
        self.screen.fill((0, 0, 0))

        note_bg_scaled = pygame.transform.scale(self.note_bg, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(note_bg_scaled, (0, 0))
        good_ending = "Zle zakonczenie"
        time = f"Czas: {self.min:02}:{self.sec:02}:{self.ms:0}"
        end_history_text = "\nNie udalo sie...\nCzuje, ze serwerownia mnie otacza.\nJeszcze nie wszystko rozumiem...\nMusze wrocic i dokonczyc to, co zaczalem.\n To jeszcze nie koniec.\n\nCzeka mnie kolejna proba."
        def draw_multiline_text(screen, text, x, y, font, color):
            lines = text.split("\n")
            line_height = font.get_height()
            for i, line in enumerate(lines):
                line_surface = font.render(line, True, color)
                screen.blit(line_surface, (x, y + i * line_height))
        draw_multiline_text(self.screen, end_history_text, self.screen.get_width()*0.19, self.screen.get_height()*0.19, self.font, BLACK)

        time_sruface = self.font.render(time, True, BLACK)
        self.screen.blit(time_sruface, (self.screen.get_width() // 2 - 150 // 2 + 200, 70))
        ending_surface = self.font.render(good_ending, True, RED)
        self.screen.blit(ending_surface, (self.screen.get_width() // 2 - 150 // 2, 100))

        for button in self.buttons:
            button.drawWithouBG(self.screen)


        pygame.display.flip()