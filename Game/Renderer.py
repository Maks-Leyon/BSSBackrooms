import numpy as np
import pygame

# Biblioteka kompilacyjna, dzięki której mamy 10x więcej FPS pozdro i ktora jednoczesnie 2x wolniej laduje gre pozdro(jeden z dwoch jest przeciwnikiem i hejterem tej blbioitrki)
from numba import njit

from Game.Settings import *
from Game.Map import Map

NUM_RAYS = int(WIDTH / 4) #Resolution
MAX_DEPTH = 400
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(FOV / 2))
# Basically:
# NUM_RAYS -> określa 'długość' podstawy trójkąta FOV w 'pikselach'
# math.tan(FOV/2) -> math.tan(fov / 2) = DIST * NUM_RAYS/2 z tangensa, połowa trójkata FOV
# po przekształceniu wzoru dostajemy DIST, które określa skalę naszej odległości od ściany
PROJ_COEFF = 3 * DIST * TILE_SIZE
SCALE = (WIDTH / NUM_RAYS)

Map = Map()

# Jako że ma dekorator njit, musi być static, czyli w sumie to może być
# poza klasą bo i tak dostarczamy wszyskto oddzielnie od klasy
@njit()
def floor_casting(frame, floorimage):
    # Przez każdy horyzontalny promień
    for ray in range(NUM_RAYS):
        # Przez połowę wertykalnych promieni
        for vray in range(VRESOLUTION):
            # Przyciemnienie dające efekt mgły
            shade = 0.1 + 0.5 * (1 - vray / VRESOLUTION)
            shadebg = 0.1 + 0.15 * (1 - vray / VRESOLUTION)

            # Dla góry i dołu danej klatki rózne przyciemnienia
            frame[ray][VRESOLUTION*2-vray-1] = shade*floorimage[0, 0]/255
            frame[ray][vray] = shadebg*floorimage[0, 0]/255
    return frame

#Podzieliłem castowanie promieni na sam cast promienia, który zachowuje
@njit()
def cast_ray(px, py, angle, game_map):
    cur_angle = angle - FOV / 2 #Zaczynamy z lewej strony FOV

    #To jest buffer, który zapamięta odległość (z axis) od gracza każdego trafionego obiektu
    #Basically, tam gdzie konczy sie promien(trafia) tam zapisujemy jego odleglosc, za pomoca ktorej potem
    # rysujemy warstwy scian/znajdziek/przecinwikow. INF na poczatek dla promieni ktore w nic nie trafiaja
    z_buffer = [float('inf')] * NUM_RAYS

    for ray in range(NUM_RAYS): #Dla kazdego promienia
        sin_a = math.sin(cur_angle)  # wertykalny ruch promienia | y
        cos_a = math.cos(cur_angle)  # horyzontalny ruch promienia | x

        for depth in range(MAX_DEPTH):
            x = px + depth * cos_a  # horyzontalna pozycja (odchodząca od pozycji gracza)
            y = py + depth * sin_a  # wertykalna pozycja (odchodząca od pozycji gracza)
            i = int(x / TILE_SIZE)  # obecny tile
            j = int(y / TILE_SIZE)

            if 0 <= i < game_map.shape[1] and 0 <= j < game_map.shape[0]:  # jeśli znajduje się w obrębach mapy
                if game_map[j, i] == 1:  # jeśli tile jest ścianą
                    depth *= math.cos(angle - cur_angle) # Usuwanie efektu rybiego oka | wyobrazic sobie trojkat prostokatny
                    z_buffer[ray] = depth # Zapisujemy odległość do buffera
                    break
        cur_angle += DELTA_ANGLE # dodajemy kąt między promieniami DELTA_ANGLE aby pracować na kącie następnego promienia
    return z_buffer # zwracamy buffer

class Renderer:
    def __init__(self, py):
        self.py = py
        self.frame = np.random.uniform(0,1, (NUM_RAYS, VRESOLUTION*2, 3))
        self.floorimage = py.surfarray.array3d(py.image.load("Assets/Textures/floor.png"))

        self.wall_texture = self.py.image.load("Assets/Textures/servergray.png").convert()
        self.texture_width = self.wall_texture.get_width()
        self.texture_height = self.wall_texture.get_height()

    def draw_walls(self, sc, z_buffer, player_angle, px, py):
        cur_angle = player_angle - FOV / 2  # Zaczynamy z lewej strony FOV

        for ray in range(NUM_RAYS):  # Dla każdego promienia
            if z_buffer[ray] != float('inf'): #Jesli w cos trafil
                ogdepth = z_buffer[ray]  # bierzemy depth z buffera dla obecnego promienia
                proj_height = PROJ_COEFF / (ogdepth + 0.0001)  # wysokosc sciany obliczana

                #literalnie przywracamy efekt rybiego oka bo inaczej takie czarne linie sie robia, max by nie dzielic przez zero
                # ogolnie to przez to ze rybie oko korzysta z innej (prawdziwej) odleglosci, ktorej potrzebujemy do obliczenia prawdziwych kordow
                depth = ogdepth / max(math.cos(player_angle - cur_angle), 0.00001)

                #kordy punktu, w kotry uderzyl promien
                hit_x = px + depth * math.cos(cur_angle)
                hit_y = py + depth * math.sin(cur_angle)

                #offset sprawdza, w kotra czesc kafelka trafilismy.
                #nasz tile size to 64, wiec jesli mamy x=130 to z tego wynika ze x w danym kafelku
                #to 2, czyli jestesmy na 2 pikselu w kafelku na x pozdro to samo dla y
                offset_x = hit_x % TILE_SIZE
                offset_y = hit_y % TILE_SIZE

                # tutaj sprawdzamy po prostu czy jestesmy blizej do pionowej czy poziomej krawedzi
                dist_to_vert = min(offset_x, TILE_SIZE - offset_x)
                dist_to_horiz = min(offset_y, TILE_SIZE - offset_y)

                # switch zaraz wytluamcze
                switch = False

                if dist_to_vert < dist_to_horiz:
                    #jesli trafilismy w pionowa, to bierzemy offset y do szukania w teksturze sciany
                    texture_offset = offset_y
                    switch = TILE_SIZE - offset_x < offset_x  # jest blizej prawej krawedzi sciany
                else:
                    # a jesli pozioma to offset x oczywiscie
                    texture_offset = offset_x
                    switch = TILE_SIZE - offset_y > offset_y # jest blizej gornej krawedzi sciany

                #mega essowo zrobiony procent kafelka na procent wielkosci tekstury bo nie wiedzialem jak inaczej to przeliczyc
                #no i on nam x z ktorego startujemy pokazuj
                texture_x = int((texture_offset / TILE_SIZE) * self.texture_width)
                #wywalalo out of bounds wiec musialem ogranizyc
                texture_x = max(0, min(texture_x, self.texture_width - 1))

                #ODWRACAMY X TEKSTURy, ABY NIE BYLA ONA BRANA Z PRAWEJ DO LEWEJ, TYLKO ZAWSZE LEWA DO PRAWEJ WAZNE!!
                if switch:
                    texture_x = max(0, min(self.texture_width - texture_x, self.texture_width - 1))

                #tworzy kolumne z tekstury, zaczyna sie na x ktory przed chwila obliczylismy, zaczyna sie na gorze zawsze
                # szerokosc jeden zeby nie wywalalo poza skale od razu, i wysokosc tekstury
                wall_column = self.wall_texture.subsurface(texture_x, 0, 1, self.texture_height)
                #skalujemy ja, szerokosc razy skala czyli wiadomo przestrzen meidzy promieniami, wysokosc razy wielkosc sciany
                wall_column_scaled = self.py.transform.scale(wall_column, (SCALE, proj_height))
                #zeby idealnie wycentrowacna byla sciana
                draw_y = HALF_HEIGHT - proj_height // 2
                #blitujemy
                sc.blit(wall_column_scaled, (ray * SCALE, draw_y))

                #cieniowanie takie samo jak zawsze
                dark = 255 / (1 + depth * depth * 0.0003)
                dark_color = (dark, dark, dark)

                # tworzymy nakladke po prostu, ktorea przyciemniamu
                darksrf = pygame.Surface(wall_column_scaled.get_size())
                darksrf.fill(dark_color)
                # BLEND_RGB_MULT sluzy do mnozenia kolorow wiec jest idealne
                sc.blit(darksrf, (ray * SCALE, draw_y), special_flags=pygame.BLEND_MULT)

            cur_angle += DELTA_ANGLE # dodajemy kąt między promieniami DELTA_ANGLE aby pracować na kącie następnego promienia


    # Metoda do rysowania dowolnego sprit'ea na danej pozycji (spx i spy to x i y tego sprite)
    def draw_sprite(self, screen, sprite, spx, spy, spsize, px, py, pangle, z_buffer, pg):
        # Tutaj zamieniamy jego x i y w postaci pozycji na mapie na pozycje pikselowe, + TILE_SIZE //2 zeby byl na srodku tile'a
        sprite_x = spx * TILE_SIZE
        sprite_y = spy * TILE_SIZE

        #pitagoras - hypot to doslownie krotszy pitagoras - oblicza droge od gracza do sprite'a
        dx = sprite_x - px
        dy = sprite_y - py
        dist = math.hypot(dx, dy)

        #oblicz kąt pomiędzy droga od gracza do sprite'a a osią X, po czym odejmujemy kat gracza zeby wiedziec jak bardzo
        # od kata patrzenia gracza odchylony jest sprite
        relative_angle = math.atan2(dy, dx) - pangle

        # Tutaj zamienaimy poprostu redundancje pi czyli jak jest 3 pi czy cos takiego to wracamy do przedzialu od
        # -pi do pi poprzez odjecie -2pi po prostu zeby to koleczko bylo dalej i mozna bylo liczyc na przedizale
        while relative_angle > math.pi: relative_angle -= 2 * math.pi
        while relative_angle < -math.pi: relative_angle += 2 * math.pi

        # Sprawdzamy czy jest w render distance (MAX_DEPTH)
        if dist < MAX_DEPTH:

            #Wielkosc sprite'a zaleznie od odleglosci - 500 to losowa liczba ktora dalem
            proj_height = (TILE_SIZE / (dist+0.0001)) * 500
            max_proj_height = HEIGHT * 2
            proj_height = min(proj_height, max_proj_height)
            #Jego szerokosc proporcjonalna do texkstury
            proj_width = proj_height * (spsize[0] / spsize[1])


            # Kąt odpowiadający połowie szerokości sprite'a na ekranie aby nie znikał nam z pola widzenia jak jest blisko
            half_sprite_angle = (proj_width / 2) / WIDTH * FOV
            # Sprawdzamy czy jakas czesc sprite'a jest w FOV
            if -FOV / 2 - half_sprite_angle < relative_angle < FOV / 2 + half_sprite_angle:
                #Lewa krawędź - Basically: ten kat ktory obliczylismy dzielimy przez FOV: to nam daje od -1 do 1 wartosc gdzie wedlug
                # naszego FOV jest sprite. Jesli sie patrzymy na wprost, czyli relative_angle to 0, to wynikiem jest 0.
                # Dlatego tez dodajemy 0.5 i mnozymy przez szerkosc ekranu - jesli patrzymy sie na wprost, do 0 jest dodane
                # 0.5 i wtedy mamy 0.5*WIDTH czyli polowe ekranu (od ktorej potem odejmujemy polowe szerokosci sprite)
                # zeby go wycentrowac), a dla reszty katow jest taka sama matematyka
                screen_x = int((0.5 + (relative_angle / FOV)) * WIDTH - proj_width / 2)
                # Tutaj po prostu tysujemy go w na srodku ekranu zawsze
                screen_y = int(HEIGHT / 2 - proj_height / 2)

                #Skalujemy go z obliczonymi wymiarami I ZAMIENIAMY NA KANAL ALFA ZEBY AUTOMATYCZNIE ZROBIL MASKE PRZEZROCZYSTYCH PIKSELI
                spsurf = pg.transform.scale(sprite, (int(proj_width), int(proj_height))).convert_alpha()

                # Jak jest blisko to po propstu rysujemy zeby nie robic trudnych obliczen
                if dist < 40:
                    screen.blit(spsurf, (screen_x, screen_y))
                    return
                #tutaj po prostu szybka skala przyciemniana na essie
                dark = max(0.01, 1 - dist**1.0003 / MAX_DEPTH)

                #bierzemy arraya wszysstkich pikseli gdzie 0 to R, 1 to G i B to 2 elo
                arr = pg.surfarray.pixels3d(spsurf)
                arr[:, :, 0] = (arr[:, :, 0] * dark) # przyciemniamy
                arr[:, :, 1] = (arr[:, :, 1] * dark)
                arr[:, :, 2] = (arr[:, :, 2] * dark)

                del arr # trza usunac i odblokowac bo inaczej blit sie pruje
                spsurf.unlock()

                #Potrzebne do wyswietlania czesci sprite'a - iterujemy po kazdym pikselu szerokosci
                for i in range(int(proj_width)):
                    # screen_x to lewa krawędź, obliczamy obecną kolumnę sprite'a poprzez dodanie obecneog i
                    xi = screen_x + i
                    if 0 <= i < spsurf.get_width() and 0 <= xi < WIDTH: #Póki jest w obrębach sprite'a/mapy
                        # Znajdujemy index promienia odpowiadajacemu kolumnie
                        ray_index = int(xi / SCALE)
                        # Jeśli promień istnieje i NIE JEST ZASŁONIĘTY przez ścianę!
                        if 0 <= ray_index < NUM_RAYS and dist < z_buffer[ray_index]:
                            # Wycinamy pionową kolumnę sprite'a i-lewa krawedz, 0-gorna krawedz, szerokosc, wysokosc
                            column = spsurf.subsurface((i, 0, 1, int(proj_height)))
                            # Rysujemy kolumnę sprite'a na ekranie
                            screen.blit(column, (xi, screen_y))
                            #print("rendering!")  gdzie okreslam kolor scian ktore tworze


    """@njit() #konwertery dla usprawnienia programu
    def converter(file, stary, nowy):
        with open(file, "r") as f:
            data = f.read()

        data_new = None

        match stary:
            case "yaml":
                data_new = yaml.safe_load(data)
            case "json":
                data_new = json.loads(data)
            case "toml":
                data_new = toml.loads(data)
            case _:
                raise ValueError(f"{stary} to nie jest typ, podaj yaml,json lub toml")

        match nowy:
            case "yaml":
                with open("convertedYAML.yaml", 'w') as f:
                    yaml.dump(data_new, f)
                print("OK")
            case "json":
                with open("convertedJSON", "w") as f:
                    json.dump(data_new, f, indent=3)
                print("ok")
            case "toml":
                with open("convertedTOML", "w") as f:
                    toml.dump(data_new, f)
                print("OK")
            case _:
                raise ValueError(f"{nowy} zly typ, podaj yaml,json lub toml")"""