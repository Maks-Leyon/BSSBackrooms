from Settings import *
from Map import Map

NUM_RAYS = int(WIDTH / 4)
MAX_DEPTH = 600
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(FOV / 2))
# Basically:
# NUM_RAYS -> określa 'długość' podstawy trójkąta FOV w 'pikselach'
# math.tan(FOV/2) -> math.tan(fov / 2) = DIST * NUM_RAYS/2 z tangensa, połowa trójkata FOV
# po przekształceniu wzoru dostajemy DIST, które określa skalę naszej odległości od ściany
PROJ_COEFF = 3 * DIST * TILE_SIZE
SCALE = (WIDTH / NUM_RAYS)

Map = Map()
class RayCasting:

    # Raycasting -> ekran, pozycja gracza x i y, kąt patrzeina gracza
    def ray_casting(self,sc, px, py, angle):
        cur_angle = angle - FOV / 2  # cur_angle to początkowy kąt promienia
        for ray in range(NUM_RAYS):  # dla każdego promienia
            sin_a = math.sin(cur_angle)  # wertykalny ruch promienia | y
            cos_a = math.cos(cur_angle)  # horyzontalny ruch promienia | x

            for depth in range(MAX_DEPTH):
                x = px + depth * cos_a  # horyzontalna pozycja (odchodząca od pozycji gracza)
                y = py + depth * sin_a  # wertykalna pozycja (odchodząca od pozycji gracza)
                i = int(x / TILE_SIZE)  # obecny tile
                j = int(y / TILE_SIZE)

                if 0 <= i < len(Map.game_map[0]) and 0 <= j < len(Map.game_map):  # jeśli znajduje się w obrębach mapy
                    if Map.game_map[j][i] == 1:  # jeśli tile jest ścianą
                        depth *= math.cos(
                            angle - cur_angle)  # Usuwanie efektu rybiego oka | wyobrazic sobie trojkat prostokatny
                        proj_height = PROJ_COEFF / (depth + 0.0001)  # Ustalanie wysokości ściany PROJ_COEFF
                        color = 255 / (1 + depth * depth * 0.0001)

                        Map.render(sc, ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height,
                                   color)  # rysowanie sciany
                        # ray * SCALE -> indeks promienia (zaczynający się od 0) razy jego szerokość, określa lewą krawędź
                        # HALF_HEIGHT - proj_height //2 -> Połowa ekranu odjąć połowa wysokości, określa górną krawędź
                        # SCALE -> Szerokość jako szerokość promienia
                        # proj_height -> Wysokość ściany
                        break
            cur_angle += DELTA_ANGLE  # dodajemy kąt między promieniami DELTA_ANGLE aby pracować na kącie następnego promienia
