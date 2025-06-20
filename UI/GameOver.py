import pygame
from UI.Button import Button
from Game.Settings import *
from Game.SaveAndLoad import *

class GameOver:
    '''Ta klasa reprezentuje Ekran po wygraniu gry, pobiera ona ekran (screen) oraz czas ukoczenia gry(elapsed_time) jako argumenty inicjalizacyjne'''
    def __init__(self, screen,elapsed_time):

        self.screen = screen

        self.note_bg = pygame.image.load("Assets/Textures/note_base.png") # fake notatka
        self.font = pygame.font.Font("Assets/Fonts/messy.ttf", 30)


        szer, wys = 250, 60
        x = screen.get_width() // 2 - 130
        y = 100
        self.buttons = [
            Button((x + 50, y + 370, szer, wys), "Obecny")
        ]

        self.input_text = ""

        self.input_rect = pygame.Rect(self.screen.get_width() // 2 - 150, 300, 300, 50)

        self.elapsed_time = elapsed_time
        self.min = self.elapsed_time // 60000
        self.sec = (self.elapsed_time % 60000) // 1000
        self.ms = self.elapsed_time % 1000


    def update(self, events):
        '''Metoda ta odpowaida za aktualizacje guzikow czy sprawdzenia pozycji myszki'''

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
                        if button.text == "Obecny":
                            SaveAndLoad.saveInfo(self.input_text, self.elapsed_time)
                            return "Menu"


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Menu"

                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                    '''elif event.key == pygame.K_RETURN:
                    SaveAndLoad.saveInfo(self.input_text,self.elapsed_time)
                    print(f"{self.input_text}")
                    return "Menu"'''
                else:
                     if len(self.input_text) < 15:
                         self.input_text += event.unicode

        self.draw()

        return "gameover"

    def draw(self):
        '''Metoda ta odpowiada za rysowanie ekranu po wygranej grze'''
        self.screen.fill((0, 0, 0))

        note_bg_scaled = pygame.transform.scale(self.note_bg, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(note_bg_scaled, (0, 0))
        good_ending = "Dobre zakonczenie"
        time = f"Czas: {self.min:02}:{self.sec:02}:{self.ms:0}"
        end_history_text = "\nW koncu rozumiem…\nZebralem notatki z calego wykladu.\nSerwerownia BSS to miejsce, ktore wyciaga z ciebie\nnajglebsze koszmary.\nJuz nigdy nie moge zaspac na wykladzie.\nPozostaje jedna rzecz.\nJedyny sposob na wyjscie.\n\nWpisz sie na liste obecnosci:"
        def draw_multiline_text(screen, text, x, y, font, color):
            lines = text.split("\n")
            line_height = font.get_height()
            for i, line in enumerate(lines):
                line_surface = font.render(line, True, color)
                screen.blit(line_surface, (x, y + i * line_height))


        draw_multiline_text(self.screen, end_history_text, self.screen.get_width()*0.14, self.screen.get_height()*0.17, self.font, BLACK)

        time_sruface = self.font.render(time,True,BLACK)
        self.screen.blit(time_sruface,(self.screen.get_width() // 2 - 150 // 2 + 200,70))
        ending_surface = self.font.render(good_ending, True, GREEN)
        self.screen.blit(ending_surface,(self.screen.get_width() // 2 - self.screen.get_width()*0.19 // 2,self.screen.get_width()*0.12))
        txt_surface = self.font.render(self.input_text, True, RED)
        self.screen.blit(txt_surface, (self.input_rect.x + self.screen.get_width()*0.22, self.input_rect.y + self.screen.get_width()*0.155))

        for button in self.buttons:
            button.drawWithouBG(self.screen)


        pygame.display.flip()