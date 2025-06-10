import pygame

from Game.Settings import *

class Tile: #Dodałem TILE klasę żeby łatwiej używać a*
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.center = x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2
        self.parent = None
        self.cost = 0

    def get_path(self, start_tile): #iteruje po rodzicach (kaflach na ktore wskazuje) zeby zwrocic liste trasy
        '''Metoda ta zwraca ścieżkę od startowego obiektu Tile (start_tile) do obecnego obiektu Tile'''
        path = []
        current = self
        while current is not start_tile:
            path.append(current)
            current = current.parent
        return path[::-1]

    def get_distance(self, target_tile): #oblicza dystans pomiedzy kaflami
        '''Metoda ta zwraca dystans pomiędzy obecnym obiektem Tile a podanym obiektem Tile (target_tile) używając wzoru Manhattan'''
        distx = abs(self.x-target_tile.x)
        disty = abs(self.y-target_tile.y)
        return 10 * (distx + disty)

class Map:
    '''Ta zmienna statyczna przechowuje kafelki mapy, gdzie kluczem jest krotka z współrzędnymi (x, y), a wartością jest obiekt Tile.'''
    tiles = {
        (0, 0): Tile(0, 0)
    }

    def __init__(self):
        #przeniosłem mapy do SETTINGS
        self.game_map = MAP1
    def is_wall(self, x, y):
        '''Metoda ta sprawdza, czy podane współrzędne (x, y) wskazują na ścianę w grze. Zwraca True, jeśli jest to ściana, w przeciwnym razie False.'''
        i = int(x // TILE_SIZE)
        j = int(y // TILE_SIZE)
        if 0 <= i < self.game_map.shape[1] and 0 <= j < self.game_map.shape[0]:
            return self.game_map[j, i] == 1
        return True

    # ogolem zamyls byl taki ze w momencie jak on zmienia pozcyje i jest na innym tile,
    # to autoamtycznie sprawdza najblisze cztery swoje boki ze prawo lewo tyl przod i sprawdzal te
    # do ktorych moze przejsc, cchailem ograniczcy by nie wlazil w sciany - udalo sie polowicznie bo
    # wchodzi czasami polowa ciala w sciany boczne - do naprawy
    def get_tile_neighbours(self, tile):
        '''Metoda ta zwraca listę sąsiednich obiektów Tile na których da się poruszać dla podanego obiektu Tile (tile).'''
        x, y = tile.x, tile.y
        knn = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]  # wspolrzedfne cztery
        scianyktoresaKoks = []
        for nx, ny in knn:
            if 0 <= ny < self.game_map.shape[0] and 0 <= nx < self.game_map.shape[1]:  # wymiary mapy
                px = (nx + 0.5) * TILE_SIZE
                py = (ny + 0.5) * TILE_SIZE

                if not self.is_wall(px, py):
                    scianyktoresaKoks.append(Map.get_tile((nx, ny)))
        return scianyktoresaKoks  # tutaj juz wrzcuam tylko te po ktoruch moze isc

    @classmethod
    def get_tile(cls, pos): #dodaje tile do slownika jesli nie istnieje, a jesli istnieje to go zwraca
        '''Metoda ta zwraca obiekt Tile dla podanej pozycji (pos), tworząc go, jeśli jeszcze nie istnieje.'''
        x, y = pos[0],pos[1]
        if (x,y) in Map.tiles:
            return Map.tiles[(x,y)]
        Map.tiles[(x,y)] = Tile(x,y)
        return Map.tiles[(x,y)]

