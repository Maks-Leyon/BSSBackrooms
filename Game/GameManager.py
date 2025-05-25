import pygame
import numpy as np
from Map import Map
from Player import Player
from Renderer import Renderer, floor_casting, cast_ray

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.map = Map()
        self.player = Player()
        self.renderer = Renderer(pygame)

        self.sprite = pygame.image.load("Assets/Textures/rock.png")
        self.spsize = np.asarray(self.sprite.get_size())
        self.spx, self.spy = 13, 15
        pygame.mixer.music.load("Assets/Sounds/bg_dark.mp3")
        pygame.mixer.music.set_volume(0.0)
        pygame.mixer.music.play(-1)

    def update(self, events, fps):
        pygame.mixer.music.set_volume(0.5)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.set_volume(0.0)
                return "menu"  # tutaj trzeba bedzei ddoac zapis postepu

        keys = pygame.key.get_pressed()
        self.player.move(keys, fps)


        self.draw()
        pygame.display.flip()
        return "game"


    def draw(self):
        self.renderer.frame = floor_casting(self.renderer.frame, self.renderer.floorimage)
        surf = pygame.surfarray.make_surface(self.renderer.frame * 255)
        surf = pygame.transform.scale(surf, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(surf, (0, 0))

        z_buffer = cast_ray(self.player.x, self.player.y, self.player.angle, self.map.game_map)
        self.renderer.draw_walls(self.screen, z_buffer, self.player.angle)
        self.renderer.draw_sprite(self.screen, self.sprite, self.spx, self.spy, self.spsize,
                                  self.player.x, self.player.y, self.player.angle, z_buffer, pygame)