import pygame
import numpy as np
from numba.core.imputils import for_iter

from Enemy import Enemy
from Renderer import Renderer, floor_casting, cast_ray
from Settings import *
from Note import Note

class Game:
    def __init__(self, screen, player):
        self.start = pygame.time.get_ticks()
        self.screen = screen
        self.player = player
        self.current_music = None
        self.map = player.map
        self.game_over = False
        self.elapsed_time = 0


        self.music_files = {
            1: "Assets/Sounds/bg_dark.mp3",
            2: "Assets/Sounds/bgsound.mp3",
            3: "Assets/Sounds/bg_PPJ.mp3"
        }

        self.renderer = Renderer(pygame)
        #self.font = pygame.font.SysFont("Arial", 25)
        self.font = pygame.font.Font("Assets/Fonts/messy.ttf", 25)


        self.note_bg = pygame.image.load("Assets/Textures/note_base.png")


        self.notes = [
            Note((5, 7), 'Notatka 1:\nByłem na wykładzie z Javy prowadzonym przez KKMPPNDMIMT,\ngdy usłyszałem nagle: „POPRAWKA, co to takiego?”.\n\nNagle zamigotało wszystko.\n\n Obudziłem się w labiryncie, ogromnych serwerów.\nZ czerwonymi napisami.\n\n „BSS”.\n\nZ oddali dobiegł dzwięk:\n„Panie i panowie..."\nMusiałem to sprawdzić.', self.note_bg, self.font),
            Note((11, 12), "Notatka 2: xdxdxdxd.", self.note_bg, self.font),
            Note((15, 9), "Notatka 3:\nZnowu onn. PCH.\n Siedzi w kącie w sweterku, obgryza długopis.\n\"Algorytm nigdy nie śpi.\"\nTo powiedział. Nikt się nie śmiał.\nWyszeptał potem:\n\"Każda pętla ma swoje przeznaczenie.\nCzy to groźba?\nNa ścianie narysował drzewo binarne.\nOno patrzyło.\"", self.note_bg, self.font),
            Note((20, 5), "Notatka 5: Skrskr goclaw to nie resort ten bankroll jest suchy suko przeloczamu peso!", self.note_bg, self.font)
        ]


       # self.enemy_sprite = pygame.image.load("Assets/Textures/rock.png")
        self.enemy_sprite = pygame.image.load("Assets/Textures/konwerterJSONnaYAML.png")


        #self.spsize = np.asarray(self.enemy_sprite.get_size())
       # self.spx, self.spy = 13, 15
        self.enemy = Enemy(13, 15, self.map, self.enemy_sprite, pygame.mixer) #srodek kafla

        #pygame.mixer.music.load("Assets/Sounds/bg_dark.mp3")
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("Assets/Sounds/bg_dark.mp3"),-1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("Assets/Sounds/oddychanie.wav"),-1)
        pygame.mixer.Channel(0).set_volume(0.0)
        pygame.mixer.Channel(1).set_volume(0.0)
        #pygame.mixer.music.play(-1)

    def update(self, events, fps):
        elapsed = pygame.time.get_ticks() - self.start # ile miliseuknd od startu
        self.min = elapsed // 60000
        self.sec = (elapsed % 60000) // 1000
        self.ms = elapsed % 1000



        pygame.mixer.Channel(0).set_volume(0.5)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.Channel(0).set_volume(0.0)
                for n in self.notes:
                    n.open_note = False
                return "menu"  # tutaj trzeba bedzei ddoac zapis postepu
        keys = pygame.key.get_pressed()
        if Note.open_notes:
            Note.show_notes(self.notes, keys, events)
            #musze je rysowac bo inaczej nie dziala scrollowanie
            for n in self.notes:
                if n.open_note:
                    n.draw(self.screen)
            pygame.display.flip()
            return "game"

        #essa
        for n in self.notes:
            if n.open_note:
                keys = pygame.key.get_pressed()
                n.update(self.player.pos, keys, events)
                return "game"

        keys = pygame.key.get_pressed()
        self.player.move(keys, fps)
        self.enemy.update(self.player)
        for n in self.notes:
            n.update(self.player.pos, keys, events)
        Note.show_notes(self.notes, keys, events)

        if self.player.music != self.current_music:
            self.current_music = self.player.music
            music_path = self.music_files.get(self.current_music) # get dziala bo jest slownik jakby co moj femboyu
            if music_path:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_path),-1)

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
        for n in self.notes:
            if n.open_note:
                return



        text_surface = self.font.render(f"Rotation speed: {self.player.rotationSpeed:.4f}", True, WHITE)
        self.screen.blit(text_surface, (10, 10))
        timje_surface = self.font.render(f"Timer: {self.min:02}:{self.sec:02}:{self.ms:0}", True, WHITE)
        self.screen.blit(timje_surface, (600,10))

        counter_text = Note.get_counter_text()
        counter_surf = self.font.render(counter_text,True,RED)
        self.screen.blit(counter_surf,(HALF_WIDTH,550))

    def change_music(self, music_file):

        pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_file),-1)
        pygame.mixer.Channel(0).set_volume(0.5)
    def draw(self):


        self.renderer.frame = floor_casting(self.renderer.frame, self.renderer.floorimage)
        surf = pygame.surfarray.make_surface(self.renderer.frame * 255)
        surf = pygame.transform.scale(surf, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(surf, (0, 0))

        z_buffer = cast_ray(self.player.x, self.player.y, self.player.angle, self.map.game_map)
        self.renderer.draw_walls(self.screen, z_buffer, self.player.angle)

        for n in self.notes:
            n.draw(self.screen)

        entities_to_draw = [n for n in self.notes if not n.open_note and not n.collected]
        entities_to_draw.append(self.enemy)

        entities_to_draw.sort(key=lambda e: -e.distance_to_player(self.player.x, self.player.y))

        for e in entities_to_draw:
            e_tile_x = e.x / TILE_SIZE
            e_tile_y = e.y / TILE_SIZE
            self.renderer.draw_sprite(self.screen, e.sprite,
                                      e_tile_x, e_tile_y,
                                      e.size,
                                      self.player.x, self.player.y, self.player.angle,
                                      z_buffer, pygame)

        '''enemy_tile_x = self.enemy.x / TILE_SIZE
        enemy_tile_y = self.enemy.y / TILE_SIZE
        enemy_size = np.asarray(self.enemy_sprite.get_size())



        self.renderer.draw_sprite(self.screen, self.enemy_sprite,
                                  enemy_tile_x, enemy_tile_y,
                                  enemy_size,
                                  self.player.x, self.player.y, self.player.angle,
                                  z_buffer, pygame)

        for note in self.notes:
            if note.open_note or note.collected:
                continue
            self.renderer.draw_sprite(self.screen, note.sprite,
                                      note.pos[0]+0.5, note.pos[1]+0.5,
                                      note.sprite.get_size(),
                                      self.player.x, self.player.y, self.player.angle,
                                      z_buffer, pygame)'''