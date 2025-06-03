import math
from typing import final

import pygame

from Entity import Entity
from Map import Map
from Settings import *

class Enemy(Entity):
    def __init__(self, x, y, map_obj, sprite, mix):
        Entity.__init__(self, sprite, x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2, sprite.get_size())
        self.map = map_obj
        self.speed = 0.7
        self.route = []
        self.stamina = 750
        self.mix = mix


    #aktualna pozycja przceiwnika
    def current_tile(self):
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
    #to samo co w graczu, zeby indeksowac na tablicy a nie na piksleach



    # MAKS-LEYON: przenioslem znajdywanie sasiadow do Map.py zbey bylo bardziej intuicyjnie


    # odelglsoc Manhattana, o tyle lepsza ze dziaal na poruszasnie sie TEORETYCZNIE
    #w pionie i poziomie, nie bedzzie szedl po przekatnej, euklidesowa przechodzila mi na przekatnej wiec zmienilem
    def SpidermanDistance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    #boze jak ja kocham astar
    def astar(self, playerpos):
        start_tile = Map.get_tile(self.current_tile()) #poczatkowy tile (na ktorym stoi gruby)
        target_tile = Map.get_tile(playerpos) # tile gracza
        opent = [] #lista tile'ow do odwiedzenia
        closedt = [] #lista odwiedonych
        opent.append(start_tile) #dodajemy pocaztkowy
        #print(opent)

        while True: #mega fajny while true
            if not any(opent):
                return [] #to sie nie powinno nigdy zdarzyc ale mi wywalalo bledy wiec jest i nie ruszaj tego
            current_tile = min(opent, key=lambda t: t.cost) #znajduje kafel o najtanszym koszcie
            #print("Step 1:",any(opent),"iswall:", self.map.is_wall(current_tile.center[0], current_tile.center[1]), current_tile.x, current_tile.y)
            opent.remove(current_tile) #odwiedzil wiec usuwa z open i wstawia do closed
            closedt.append(current_tile)

            if current_tile == target_tile: #jesli to jest nasz target to resetujemy wszystkie tile i zwracamy sciezke
                route = current_tile.get_path(start_tile)
                for tile in opent:
                    tile.cost = 0
                    tile.path = None
                for tile in closedt:
                    tile.cost = 0
                    tile.path = None
                return route # tu zwracamy sciezke o tutaj tu ja zwracamy

            for tile in self.map.get_tile_neighbours(current_tile): # dla kazdego sasiada
                if self.map.is_wall(tile.center[0], tile.center[1]) or (tile in closedt): # ignorujemy jesli odwiedzony lub sciana
                    continue
                # kalkulacja kosztu - dystans od konca + dystans od poczatku
                cstart = tile.get_distance(start_tile)
                cend = tile.get_distance(target_tile)
                c = cstart + cend
                # jesli pierwsze napotkanie, lub nowy koszt jest lepszy to zmieniamu
                if tile not in opent or tile.cost > c:
                    tile.cost = c
                    tile.parent = current_tile # tu wazne bo teraz kafel wskazuje na poprzedni dzieki czemu tworzy sie sciezka
                    if tile not in opent:
                        opent.append(tile)

    def update(self, player):
        player_tile = (int(player.x // TILE_SIZE), int(player.y // TILE_SIZE)) #pozycja gracza caly czas zeby mogl skedzic jak chciales
        current = self.current_tile() # aktual pozycja przeciwnika
        self.route = self.astar(player.pos)  # sciezka hell yeah baby

        #distance to odleglosc od gracza euklidesowa ORAZ ilosc kafelkow * 10 zeby gracz nie robil kiwki
        distance = Entity.distance_to_player(self, player.x, player.y) + 10*len(self.route)

        sound = 1/max(1, distance / 7)
        self.mix.Channel(1).set_volume(sound)

        #bieg enemy
        if distance < 310:
            if self.stamina > 1:
                self.stamina -= 2
                self.speed = 1.05 + (self.stamina / 1000)
            else:
                self.speed = 0.78
        elif distance < 700:
            if distance > 340:
                self.stamina = self.stamina + (1 if self.stamina < 750 else 0)
            self.speed = 0.72
        else:
            self.stamina = 900
            self.speed = 1.8

        if current != player_tile and any(self.route) and len(self.route) > 0: #czy sciezka jest wgl
            next_tile = self.route[0] # bierze nastepny kafel no i ogolnie [0] bo jak dochodzi do kafla no to juz ogarnia nastepny es
            target_x, target_y = next_tile.center # jego srodek

            #zmiana we wspolrzednych
            dx = target_x - self.x
            dy = target_y - self.y

            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.x = target_x
                self.y = target_y
            else:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed


        # trzeba wykminic i dodac tak jak pisalem wyzej implemetnacje w tym miejscu co sie dzieej jak gracz i gruby stoja na tym samym poly

        #print(f"Enemy pozcyja: x={self.x:.1f}, y={self.y:.1f}, tile={self.current_tile()}")
        #print(f"Gruby: ({self.x//TILE_SIZE},{self.y//TILE_SIZE})")
        print(f"Gruby: (speed={self.speed:.2f}, stamina={self.stamina}), distance={Entity.distance_to_player(self, player.x, player.y):.2f})")
