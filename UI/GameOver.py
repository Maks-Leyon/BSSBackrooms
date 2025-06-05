import pygame
from UI import Button
from Game.Settings import *
from Game.SaveAndLoad import *

class GameOver:
    def __init__(self, screen,elapsed_time, win):
        if not win:
            print("HALO")
        self.screen = screen
        self.font = pygame.font.SysFont(None, 60)
        self.win = win

        szer, wys = 250, 60
        x = screen.get_width() // 2 - 130
        y = 200
        self.buttons = [
            Button.Button((x, y + 300, szer, wys), "Menu")
        ]

        self.input_text = ""
        self.active_input = False
        self.input_rect = pygame.Rect(self.screen.get_width() // 2 - 150, 300, 300, 50)

        self.elapsed_time = elapsed_time
        self.min = self.elapsed_time // 60000
        self.sec = (self.elapsed_time % 60000) // 1000
        self.ms = self.elapsed_time % 1000


    def update(self, events):
        if not self.win:
            print("update false")
        elif self.win:
            print("update true")
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()



        for button in self.buttons:
            button.update(mouse_pos)


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #jednorazowo za kazda proba klikniecia

                if self.input_rect.collidepoint(mouse_pos):
                    self.active_input = True

                for button in self.buttons:
                    if button.is_clicked(mouse_pos, mouse_pressed):
                        print("fueah")
                        print(button.text)
                        return button.text


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Menu"
                if self.active_input:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        SaveAndLoad.saveInfo(self.input_text,self.elapsed_time)
                        print(f"{self.input_text}")
                        return "Menu"
                    else:
                        if len(self.input_text) < 15:
                            self.input_text += event.unicode

        self.draw()
        return "gameover"

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.win:
            win_text = self.font.render("WYGRANA!", True, GREEN)
        else:
            win_text = self.font.render("PRZEGRANA!", True, RED)
        self.screen.blit(win_text, (self.screen.get_width() // 2 - win_text.get_width() // 2, 100))
        time_text = f"Czas : {self.min:02}:{self.sec:02}:{self.ms:03}"
        time_surface = self.font.render(time_text, True, WHITE)
        self.screen.blit(time_surface, (self.screen.get_width() // 2 - time_surface.get_width() // 2, 200))
        if self.win:
            color = WHITE if self.active_input else BLUE
            pygame.draw.rect(self.screen, color, self.input_rect, 2)

            txt_surface = self.font.render(self.input_text, True, WHITE)
            self.screen.blit(txt_surface, (self.input_rect.x + 5, self.input_rect.y + 10))

            info_surf = self.font.render("Wpisz nick i ENTER", True, WHITE)
            self.screen.blit(info_surf, (self.screen.get_width() // 2 - info_surf.get_width() // 2, 370))
        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()