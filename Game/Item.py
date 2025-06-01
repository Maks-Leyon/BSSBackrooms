from operator import itemgetter

import pygame
from Settings import *

class Item:
    def __init__(self,sprite,font,screen):
        self.sprite = sprite
        self.font = font
        self.screen = screen

        # slowniki, pozcyja to doslowne koorydnaty na mapie, collected sluzy do zliczania counterem ilosci zebranych
        self.notatki = [
            {"pos": (5, 7), "note": 'Notatka 1:\nByłem na wykładzie z Javy prowadzonym przez KKMPPNDMIMT,\ngdy usłyszałem nagle: „POPRAWKA, co to takiego?”.\n\nNagle zamigotało wszystko.\n\n Obudziłem się w labiryncie, ogromnych serwerów.\nZ czerwonymi napisami.\n\n „BSS”.\n\nZ oddali dobiegł dzwięk:\n„Panie i panowie..."\nMusiałem to sprawdzić.', "collected": False},
            {"pos": (10, 12), "note": "Notatka 2: xdxdxdxd.", "collected": False},
            {"pos": (15, 9), "note": "Notatka 3:\nZnowu onn. PCH.\n Siedzi w kącie w sweterku, obgryza długopis.\n\"Algorytm nigdy nie śpi.\"\nTo powiedział. Nikt się nie śmiał.\nWyszeptał potem:\n\"Każda pętla ma swoje przeznaczenie.\nCzy to groźba?\nNa ścianie narysował drzewo binarne.\nOno patrzyło.\"", "collected": False},
            {"pos": (20, 5), "note": "Notatka 4: nigga!", "collected": False},
            {"pos": (3, 14), "note": "Notatka 5: Skrskr goclaw to nie resort ten bankroll jest suchy suko przeloczamu peso!", "collected": False}
        ]

        self.open_note = False # czy alktualnie otwarta jest notatka
        self.current_note_Text = ""
        self.current_indx = None #index notatki ktora jest aktualnie otwartta, nizej objasniam


    def draw(self):



        # by odczytywac z notatki, w momencei gdy jest otwarta robie cvaly czafny ekran, dodatkowa metoda multiline_text sluzy do tego by obslugiwac
        #teskt z /n gdyz sam font.render nie ogarnia takiej nowoczesnosci
        if self.open_note:
            background = pygame.Surface(self.screen.get_size())
            background.fill(BLACK)
            #background.set_alpha(270)
            self.screen.blit(background,(0,0))

            self.draw_multiline_text(self.screen, self.current_note_Text, 50, 50, self.font, WHITE)


            inf = self.font.render("NACISNIJ SPACJE ABY ZAMKNAC", True, BLUE)
            self.screen.blit(inf,(200,550))

            return # zeby nic wiecej sie nie rysowalo









    #co za gowno , font nie obsluguje /n
    def draw_multiline_text(self,screen, text, x, y, font, color, line_spacing=5):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, color)
            screen.blit(line_surf, (x, y + i * (font.get_height() + line_spacing)))

    def update(self,player_pos, keys, ev):
        #zamkniecie notatki i zmiana flagi na collected
        if self.open_note:
            for e in ev:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.open_note = False
                    self.notatki[self.current_indx]["collected"] = True
                    self.current_indx = None
            return


        #tutaj sprwadzam czy7 gracz jest blisko notatki, jezedli tak to po kliknieciu E automatycznie notatka sie otwiera
        px, py = player_pos # zgarniam pozcyje gracza w krotce jak zwykle pozdro
        for i, item in enumerate(self.notatki):

            item_x = (item["pos"][0] + 0.5) * TILE_SIZE # liczepo pozycje kazdej notatki
            item_y = (item["pos"][1] + 0.5) * TILE_SIZE
            dist = ( (px - item_x) ** 2 + (py - item_y) ** 2) ** 0.5 #juz euklideoswa pomiedzy notka a graczem
            if dist < TILE_SIZE: # jezeli dystans jest na tyle maly, czyli np jestesmy na tym samytm tile to przy nacisnieu e otwiera sei notatka
                if  keys[pygame.K_e]:
                    self.open_note = True
                    self.current_note_Text = item["note"]
                    self.current_indx = i
                    break


        #zwraca liczbe zebranych notatek
    def count_collected(self):
        counter = 0
        for c in self.notatki:
            if c["collected"]:
                counter += 1
                #print({counter})
        return counter

        #dodatkowa by wyswietlac na ekranie liczbe aktualnie zebranyuch, taki getter
    def get_counter_text(self):
        collected = self.count_collected()
        return f"Zebrane: {collected}/{len(self.notatki)}"
