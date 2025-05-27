import pygame
import numpy as np
from Map import Map
from Player import Player
from Renderer import Renderer, floor_casting, cast_ray

class Game:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.current_music = None
        self.map = Map()


        self.music_files = {
            1: "Assets/Sounds/bg_dark.mp3",
            2: "Assets/Sounds/bgsound.mp3",
            3: "Assets/Sounds/bg_PPJ.mp3"
        }

        self.renderer = Renderer(pygame)
        self.font = pygame.font.SysFont(None, 30)

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

        if self.player.music != self.current_music:
            self.current_music = self.player.music
            music_path = self.music_files.get(self.current_music) # get dziala bo jest slownik jakby co moj femboyu
            if music_path:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)

        self.draw()
        self.draw_info()
        pygame.display.flip()
        return "game"

    def draw_info(self):
        text_surface = self.font.render(f"Rotation speed: {self.player.rotationSpeed:.4f}", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

    def change_music(self, music_file):

        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    def draw(self):

        self.renderer.frame = floor_casting(self.renderer.frame, self.renderer.floorimage)
        surf = pygame.surfarray.make_surface(self.renderer.frame * 255)
        surf = pygame.transform.scale(surf, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(surf, (0, 0))

        z_buffer = cast_ray(self.player.x, self.player.y, self.player.angle, self.map.game_map)
        self.renderer.draw_walls(self.screen, z_buffer, self.player.angle)
        self.renderer.draw_sprite(self.screen, self.sprite, self.spx, self.spy, self.spsize,
                                  self.player.x, self.player.y, self.player.angle, z_buffer, pygame)