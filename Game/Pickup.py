import pygame

from Game.Entity import Entity
from Game.Map import Map
from Game.Settings import TILE_SIZE


class Pickup(Entity):
    '''Ta klasa reprezentuje zbieralny przedmiot w grze. Dziedziczy po klasie Entity. Pobiera ona pozycję (pos), sprite przedmiotu (sprite) oraz numer przedmiotu (no) jako argumenty inicjalizacyjne.'''
    def __init__(self, pos, sprite, no):
        Entity.__init__(self, sprite,pos[0]* TILE_SIZE + TILE_SIZE // 2,pos[1]* TILE_SIZE + TILE_SIZE // 2,sprite.get_size())
        self.no = no
        self.pos = pos
        self.collected = False

    def effect(self, player):
        '''Metoaa ta aktualizuje stan zdrowia gracza (player) oraz wywoł€je dźwięk jeśli jest to niemożliwe.'''
        h = player.hp
        if h >= 3:
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("Assets/Sounds/error.wav"))
            return
        self.collected = True
        player.hp = min(h+1, 3)

    def update(self, player, keys):
        '''Metoda ta aktualizuje stan zbieralnego przedmiotu, sprawdzając, czy został zebrany. Jeśli gracz (player) znajduje się na tym samym kafelku co przedmiot i naciśnie klawisz E, wywoływana jest metoda effect, która aktualizuje stan zdrowia gracza. Naciśnięte klawisze są przekazywane jako argument (keys).'''
        if self.collected:
            return
        if Map.get_tile(player.pos) == Map.get_tile(self.pos):
            if keys[pygame.K_e]:
                self.effect(player)