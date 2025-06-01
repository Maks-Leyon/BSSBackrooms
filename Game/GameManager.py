import pygame
import numpy as np
from Map import Map
from Enemy import Enemy
from Player import Player
from Renderer import Renderer, floor_casting, cast_ray
from Settings import *
from Item import Item

class Game:
    def __init__(self, screen, player):
        self.start = pygame.time.get_ticks()
        self.screen = screen
        self.player = player
        self.current_music = None
        self.map = Map()
        self.game_over = False
        self.elapsed_time = 0


        self.music_files = {
            1: "Assets/Sounds/bg_dark.mp3",
            2: "Assets/Sounds/bgsound.mp3",
            3: "Assets/Sounds/bg_PPJ.mp3"
        }

        self.renderer = Renderer(pygame)
        self.font = pygame.font.SysFont("Arial", 25)


        self.note = pygame.image.load("Assets/Textures/note.png")
        self.Notes = Item(self.note, self.font, self.screen)


        self.enemy_sprite = pygame.image.load("Assets/Textures/rock.png")


        #self.spsize = np.asarray(self.enemy_sprite.get_size())
       # self.spx, self.spy = 13, 15
        self.enemy = Enemy(13, 15, self.map, self.enemy_sprite) #srodek kafla

        pygame.mixer.music.load("Assets/Sounds/bg_dark.mp3")
        pygame.mixer.music.set_volume(0.0)
        pygame.mixer.music.play(-1)

    def update(self, events, fps):




        elapsed = pygame.time.get_ticks() - self.start # ile miliseuknd od startu
        self.min = elapsed // 60000
        self.sec = (elapsed % 60000) // 1000
        self.ms = elapsed % 1000



        pygame.mixer.music.set_volume(0.5)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.set_volume(0.0)
                return "menu"  # tutaj trzeba bedzei ddoac zapis postepu


        #WAZNE!!!!!! w tym momencei przy otwarciu notatki, wywoluje update z klasy Item, dopoki nie skoncze i dopoki nie wywolam return game, gra zastyua wtedy nic sie nie porusza, timer nie leci itd
        if self.Notes.open_note:
            keys = pygame.key.get_pressed()
            self.Notes.update((self.player.x, self.player.y), keys, events)
            return "game"

        keys = pygame.key.get_pressed()
        self.player.move(keys, fps)
        self.enemy.update(self.player)
        self.Notes.update((self.player.x, self.player.y), keys, events)

        if self.player.music != self.current_music:
            self.current_music = self.player.music
            music_path = self.music_files.get(self.current_music) # get dziala bo jest slownik jakby co moj femboyu
            if music_path:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)





        # TO NAPRAWIE
       # if self.notes_class.count_collected() == len(self.notes_class.notatki):
        #    self.game_over = True
         #   self.elapsed_time = pygame.time.get_ticks() - self.start # chcaoielm czas przeniesc na koncowy ekran
          #  return "gameover"


        self.draw()
        self.draw_info()
        pygame.display.flip()
        return "game"

    def draw_info(self):
        if self.Notes.open_note:
            return



        text_surface = self.font.render(f"Rotation speed: {self.player.rotationSpeed:.4f}", True, WHITE)
        self.screen.blit(text_surface, (10, 10))
        timje_surface = self.font.render(f"Timer: {self.min:02}:{self.sec:02}:{self.ms:0}", True, WHITE)
        self.screen.blit(timje_surface, (600,10))

        counter_text = self.Notes.get_counter_text()
        counter_surf = self.font.render(counter_text,True,RED)
        self.screen.blit(counter_surf,(HALF_WIDTH,550))

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

        self.Notes.draw()


        enemy_tile_x = self.enemy.x / TILE_SIZE
        enemy_tile_y = self.enemy.y / TILE_SIZE
        enemy_size = np.asarray(self.enemy_sprite.get_size())

        self.renderer.draw_sprite(self.screen, self.enemy_sprite,
                                  enemy_tile_x, enemy_tile_y,
                                  enemy_size,
                                  self.player.x, self.player.y, self.player.angle,
                                  z_buffer, pygame)