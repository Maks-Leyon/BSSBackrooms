import math
from Settings import *

class Enemy:
    def __init__(self, x, y, map_obj, sprite):
        self.x = x # w gameManager robie /2 zeby byl srodek kafla, mozna tez tu niby
        self.y = y
        self.map = map_obj
        self.sprite = sprite
        self.speed = 2.0


    #aktualna pozycja przceiwnika
    def current_tile(self):
        return (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
    #to samo co w graczu, zeby indeksowac na tablicy a nie na piksleach



    # ogolem zamyls byl taki ze w momencie jak on zmienia pozcyje i jest na innym tile,
    #to autoamtycznie sprawdza najblisze cztery swoje boki ze prawo lewo tyl przod i sprawdzal te
    # do ktorych moze przejsc, cchailem ograniczcy by nie wlazil w sciany - udalo sie polowicznie bo
    #wchodzi czasami polowa ciala w sciany boczne - do naprawy
    def get_free_tile(self, tile):
        x, y = tile
        knn = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)] # wspolrzedfne cztery
        scianyktoresaKoks = []
        for nx, ny in knn:
            if 0 <= ny < self.map.game_map.shape[0] and 0 <= nx < self.map.game_map.shape[1]: # wymiary mapy
                px = (nx + 0.5) * TILE_SIZE
                py = (ny + 0.5) * TILE_SIZE

                if not self.map.is_wall(px, py):
                    scianyktoresaKoks.append((nx, ny))
        return scianyktoresaKoks # tutaj juz wrzcuam tylko te po ktoruch moze isc


    # odelglsoc Manhattana, o tyle lepsza ze dziaal na poruszasnie sie TEORETYCZNIE
    #w pionie i poziomie, nie bedzzie szedl po przekatnej, euklidesowa przechodzila mi na przekatnej wiec zmienilem
    def SpidermanDistance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def update(self, player):
        player_tile = (int(player.x // TILE_SIZE), int(player.y // TILE_SIZE)) #pozycja gracza caly czas zeby mogl skedzic jak chciales
        current = self.current_tile() # aktual pozycja przeciwnika


        #Tutaj bedzei trzeba dodac potem metody jakiegos ataku czy cos
        if current != player_tile: # idk czemu jak sie nie ruszam szczerez to to nie dziala XD
            sasiednie = self.get_free_tile(current)
            print(f"Neighbors: {sasiednie}") #debug
            if sasiednie:
                # zabrane z projetku knn Nai pozdro wielkie, zwracasz najblizszego sasiada knn lambda
                next_tile = min(sasiednie, key=lambda t: self.SpidermanDistance(t, player_tile)) # tutaj sprawiam zeby wybieral ten kafel ktory jest nablizej do gracza wiec on zawsze wybierez kierunek w nasza storne
                target_x = (next_tile[0] + 0.5) * TILE_SIZE #nadal probuje wysriodkowac
                target_y = (next_tile[1] + 0.5) * TILE_SIZE



                dx = target_x - self.x
                dy = target_y - self.y


                #Ogolem tak, wpeirw zrobilem odlelosc euklidesowa, ogolem on wtedy gubil sie na prostych
                #drtogach i zakrecal w sciane czasami, jak szlo sie tlyko po x, natomiast druga wersja ktora obecnie
                #dziala jest spoko, on chodzi okej ale jak przejdziesz na wiecej niz 2  zakrety on omija sciane - spojrz na to prosze

                '''dist = math.hypot(dx, dy)

                if dist < self.speed:
                    self.x = target_x
                    self.y = target_y
                else:
                    self.x += (dx / dist) * self.speed
                    self.y += (dy / dist) * self.speed'''


                #dobra, ooglem troche znalzlem tego na githubie
                if abs(dx) > abs(dy): # check czy idzie w pionie czy poziomie
                    step = self.speed if dx > 0 else -self.speed # pytanie czyu lewo czy prawo. Maksie P
                    new_x = self.x + step
                    new_y = self.y
                    if not self.map.is_wall(new_x, new_y):
                        if abs(dx) < abs(step):
                            self.x = target_x
                        else:
                            self.x = new_x

                else:
                    step = self.speed if dy > 0 else -self.speed
                    new_x = self.x
                    new_y = self.y + step
                    if not self.map.is_wall(new_x, new_y):
                        if abs(dy) < abs(step):
                            self.y = target_y
                        else:
                            self.y = new_y


        # trzeba wykminic i dodac tak jak pisalem wyzej implemetnacje w tym miejscu co sie dzieej jak gracz i gruby stoja na tym samym poly

        print(f"Enemy pozcyja: x={self.x:.1f}, y={self.y:.1f}, tile={self.current_tile()}")
