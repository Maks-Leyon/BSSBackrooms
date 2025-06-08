import pygame
from Entity import Entity
from Map import Map
from Settings import *

class Note(Entity):
    count = 0
    open_notes = False
    note_index = 0
    notes_to_show = []
    total_notes = 0 # zmienna do get _couner
    def __init__(self,pos,note,sprite,font,no):
        Entity.__init__(self,sprite,pos[0]* TILE_SIZE + TILE_SIZE // 2,pos[1]* TILE_SIZE + TILE_SIZE // 2,sprite.get_size())
        self.font = font
        self.pos = pos
        self.note = note
        self.no = no
        self.collected = False
        self.open_note = False
        Note.total_notes +=1

    '''def reset(self):
        Note.total_notes = 0'''


    def draw(self, screen):
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
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, color)
            screen.blit(line_surf, (x, y + i * (font.get_height() + line_spacing)))

    def update(self,player_pos, keys, ev):
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
        return f"Zebrane: {Note.count}/{Note.total_notes}"

    @classmethod
    def show_notes(cls, notes, keys, ev):
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

