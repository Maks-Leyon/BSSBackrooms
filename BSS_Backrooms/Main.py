import pygame
import math
import sys

from Settings import *
pygame.init()
from Map import Map
from Player import Player
from RayCasting import RayCasting


Map = Map()
Player = Player()
RayCasting = RayCasting()

def Main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Miki i Maksiu <333333")
    clock = pygame.time.Clock()
    bgmusic = pygame.mixer.music.load("Assets/Sounds/bgsound.mp3")
    pygame.mixer.music.set_volume(0.1)
    bgmusic = pygame.mixer.music.play(-1)

    # Images
    bgimage = pygame.image.load("Assets/Textures/background.png")
    bgimage = pygame.transform.scale(bgimage, (WIDTH, HEIGHT))
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        Player.move(keys)

        # Draw
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (100, 100, 100), (0, 0, WIDTH, HALF_HEIGHT)) # Sky
        #Draw background
        screen.blit(bgimage, (0 ,0))
        pygame.draw.rect(screen, (50, 50, 50), (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))  # Floor

        RayCasting.ray_casting(screen, Player.x, Player.y, Player.angle)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    Main()