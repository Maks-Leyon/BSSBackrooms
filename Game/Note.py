import pygame
from Game.Entity import Entity
from Game.Map import Map
from Game.Settings import *

class Note(Entity):
    '''Ta klasa reprezentuje notatkę w grze. Dziedziczy po klasie Entity i zawiera metody do rysowania, aktualizacji stanu notatki oraz zarządzania liczbą zebranych notatek. Pobiera ona pozycję (pos), tekst notatki (note), sprite notatki (sprite), jej czcionkę (font) oraz numer notatki (no) jako argumenty inicjalizacyjne.'''
    count = 0
    '''Ta zmienna statyczna przechowuje liczbę zebranych notatek.'''
    open_notes = False
    '''Ta zmienna statyczna określa czy jakaś notatka jest otwarta.'''
    note_index = 0
    '''Ta zmienna statyczna przechowuje indeks aktualnie wyświetlanej notatki.'''
    notes_to_show = []
    '''Ta zmienna statyczna przechowuje listę notatek do wyświetlenia.'''
    total_notes = 0 # zmienna do get _couner
    '''Ta zmienna statyczna przechowuje całkowitą liczbę zebranych notatek w grze.'''
    def __init__(self,pos,note,sprite,font,no):
        Entity.__init__(self,sprite,pos[0]* TILE_SIZE + TILE_SIZE // 2,pos[1]* TILE_SIZE + TILE_SIZE // 2,sprite.get_size())
        self.font = font
        self.pos = pos
        self.note = note
        self.no = no
        self.collected = False
        self.open_note = False
        Note.total_notes +=1

    def draw(self, screen):
        '''Metoda ta rysuje notatkę, w tym jej tło i tekst na ekranie (screen), jeśli jest otwarta.'''
        if self.open_note:
            #srcalpha pozwala na przezroczystosc, gratulacje
            blak = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            blak.fill((0, 0, 0, 180))
            screen.blit(blak, (0,0))
            skibidi = self.sprite
            skibidi = pygame.transform.scale(skibidi, (screen.get_width()*0.87, screen.get_height()*0.85))
            screen.blit(skibidi,(screen.get_width()*0.065,screen.get_height()*0.075))
            self.draw_multiline_text(screen, self.note, screen.get_width()*0.19, screen.get_height()*0.19, self.font, BLACK)


            inf = self.font.render("NACISNIJ SPACJE ABY ZAMKNAC", True, BLUE)
            screen.blit(inf,(screen.get_width()*0.3,screen.get_height()*0.95))

            return


    #co za gowno , font nie obsluguje /n
    def draw_multiline_text(self,screen, text, x, y, font, color, line_spacing=5):
        '''Metoda ta rysuje wieloliniowy tekst na ekranie (screen) w podanej pozycji (x, y) z użyciem podanego fontu (font) i koloru (color). Odległość między liniami można dostosować za pomocą parametru line_spacing.'''
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, color)
            screen.blit(line_surf, (x, y + i * (font.get_height() + line_spacing)))

    def update(self,player_pos, keys, ev):
        '''Metoda ta aktualizuje stan notatki, sprawdzając, czy została zebrana lub otwarta. Jeśli notatka jest otwarta, reaguje na naciśnięcie spacji, aby ją zamknąć. Jeśli gracz znajduje się na tym samym kafelku co notatka (player_pos) i naciśnie klawisz E, notatka zostanie otwarta. Naciśnięte klawisze i ewenty są przekazywane jako argumenty (keys, ev).'''
        if self.collected:
            return
        if self.open_note:
            for e in ev:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.open_note = False
                    if not self.collected:
                        Note.count += 1
                    self.collected = True
            return
        if Map.get_tile(player_pos) == Map.get_tile(self.pos):
            if keys[pygame.K_e]:
                self.open_note = True

        #dodatkowa by wyswietlac na ekranie liczbe aktualnie zebranyuch, taki getter
    @classmethod
    def get_counter_text(cls):
        '''Metoda ta zwraca tekst z liczbą zebranych notatek i całkowitą liczbą notatek.'''
        return f"Zebrane: {Note.count}/{Note.total_notes}"

    @classmethod
    def show_notes(cls, notes, keys, ev):
        '''Metoda ta obsługuje wyświetlanie notatek. Jeśli notatki są otwarte, reaguje na naciśnięcia klawiszy strzałek w lewo i w prawo, aby przełączać między notatkami, oraz na spację, aby je zamknąć. Jeśli naciśnięto klawisz N, otwiera wszystkie zebrane notatki. Naciśnięte klawisze i ewenty są przekazywane jako argumenty (keys, ev).'''
        if Note.open_notes:
            for e in ev:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RIGHT:
                        Note.note_index = (Note.note_index + 1) % len(Note.notes_to_show)
                    elif e.key == pygame.K_LEFT:
                        Note.note_index = (Note.note_index - 1) % len(Note.notes_to_show)
                    elif e.key == pygame.K_SPACE:
                        Note.open_notes = False
                        Note.notes_to_show[Note.note_index].open_note = False
                        return
            for i in range(len(Note.notes_to_show)):
                Note.notes_to_show[i].open_note = True if i == Note.note_index else False
            return
        if keys[pygame.K_n]:
            Note.notes_to_show = []
            for n in notes:
                if n.collected:
                    Note.notes_to_show.append(n)
            if len(Note.notes_to_show) == 0:
                    return
            Note.open_notes = True
            Note.note_index = 0
            Note.notes_to_show[0].open_note = True

