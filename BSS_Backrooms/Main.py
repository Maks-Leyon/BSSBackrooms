import pygame
import math
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BSS Backrooms")
clock = pygame.time.Clock()

# Images
bgimage = pygame.image.load("Assets/Textures/background.png")
bgimage = pygame.transform.scale(bgimage, (WIDTH, HEIGHT))

# Map (1 = wall, 0 = empty)
game_map = [
    [1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,1,1,1],
    [1,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1],
]
TILE_SIZE = 64
MAP_WIDTH = len(game_map[0]) * TILE_SIZE #x
MAP_HEIGHT = len(game_map) * TILE_SIZE #y

# Player
player_x = TILE_SIZE *4
player_y = TILE_SIZE *4
player_angle = -(math.pi / 2)  # w radianach
player_speed = 2

# Raycasting settings
FOV = math.pi / 3.5  # w radianach
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

# Bullet list
bullets = []

# Collision check
def is_wall(x, y):
    i = int(x // TILE_SIZE)
    j = int(y // TILE_SIZE)
    if 0 <= i < len(game_map[0]) and 0 <= j < len(game_map):
        return game_map[j][i] == 1
    return True

# Raycasting -> ekran, pozycja gracza x i y, kąt patrzeina gracza
def ray_casting(sc, px, py, angle):
    cur_angle = angle - FOV / 2 # cur_angle to początkowy kąt promienia
    for ray in range(NUM_RAYS): # dla każdego promienia
        sin_a = math.sin(cur_angle) #wertykalny ruch promienia | y
        cos_a = math.cos(cur_angle) #horyzontalny ruch promienia | x


        for depth in range(MAX_DEPTH):
            x = px + depth * cos_a  # horyzontalna pozycja (odchodząca od pozycji gracza)
            y = py + depth * sin_a  # wertykalna pozycja (odchodząca od pozycji gracza)
            i = int(x / TILE_SIZE)  # obecny tile
            j = int(y / TILE_SIZE)

            if 0 <= i < len(game_map[0]) and 0 <= j < len(game_map):  # jeśli znajduje się w obrębach mapy
                if game_map[j][i] == 1:                               # jeśli tile jest ścianą
                    depth *= math.cos(angle - cur_angle)              # Usuwanie efektu rybiego oka | wyobrazic sobie trojkat prostokatny
                    proj_height = PROJ_COEFF / (depth + 0.0001)       # Ustalanie wysokości ściany PROJ_COEFF
                    color = 255 / (1 + depth * depth * 0.0001)
                    pygame.draw.rect(sc, (color, color, color),
                        (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))  #rysowanie sciany
                #ray * SCALE -> indeks promienia (zaczynający się od 0) razy jego szerokość, określa lewą krawędź
                #HALF_HEIGHT - proj_height //2 -> Połowa ekranu odjąć połowa wysokości, określa górną krawędź
                #SCALE -> Szerokość jako szerokość promienia
                #proj_height -> Wysokość ściany
                    break
        cur_angle += DELTA_ANGLE # dodajemy kąt między promieniami DELTA_ANGLE aby pracować na kącie następnego promienia

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        player_angle -= 0.03
    if keys[pygame.K_RIGHT]:
        player_angle += 0.03
    if keys[pygame.K_w]:
        dx += player_speed * math.cos(player_angle)
        dy += player_speed * math.sin(player_angle)
    if keys[pygame.K_s]:
        dx -= player_speed * math.cos(player_angle)
        dy -= player_speed * math.sin(player_angle)

    if not is_wall(player_x + dx, player_y):
        player_x += dx
    if not is_wall(player_x, player_y + dy):
        player_y += dy

    # Draw
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, WIDTH, HALF_HEIGHT)) # Sky
    #Draw background
    screen.blit(bgimage, (0 ,0))
    pygame.draw.rect(screen, (50, 50, 50), (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))  # Floor

    ray_casting(screen, player_x, player_y, player_angle)

    pygame.display.flip()
    clock.tick(60)
