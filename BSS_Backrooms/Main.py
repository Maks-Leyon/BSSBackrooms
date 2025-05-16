import pygame
import numpy as np
import math
import sys

from Settings import *
from Map import Map
from Player import Player
from Renderer import Renderer, floor_casting, cast_ray

pygame.init()
Map = Map()
Player = Player()
Renderer = Renderer(pygame)
# Stworzony DrawManager dla poukładania

def Main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Miki i Maksiu <333333")
    clock = pygame.time.Clock()
    pygame.mixer.music.load("Assets/Sounds/bg_dark.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    sprite = pygame.image.load("Assets/Enemy/rock.png")
    spsize = np.asarray(sprite.get_size())
    spx, spy = 13, 15

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        Player.move(keys, clock.tick())
        print(Player.x//TILE_SIZE, Player.y//TILE_SIZE)

        #
        Renderer.frame = floor_casting(Renderer.frame, Renderer.floorimage)
        surf = pygame.surfarray.make_surface(Renderer.frame*255)
        surf = pygame.transform.scale(surf, (WIDTH, HEIGHT))
        screen.blit(surf, (0, 0))

        z_buffer = cast_ray(Player.x, Player.y, Player.angle, Map.game_map)

        Renderer.draw_walls(screen, z_buffer, Player.angle)

        Renderer.draw_sprite(screen, sprite, spx, spy, spsize, Player.x, Player.y, Player.angle, z_buffer, pygame)

        pygame.display.flip()

if __name__ == "__main__":
    Main()