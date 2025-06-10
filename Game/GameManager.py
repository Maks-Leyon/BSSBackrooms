import pygame
from Game.Enemy import Enemy
from Game.Pickup import Pickup
from Game.Map import Map
from Game.Renderer import Renderer, floor_casting, cast_ray
from Game.Settings import *
from Game.Note import Note

class Game:
    '''Ta klasa reprezentuje główną logikę gry, zarządza stanem gry, aktualizuje oraz rysuje wszystkie elementy na ekranie. Pobiera ona ekran (screen) oraz gracza (player) jako argumenty inicjalizacyjne.'''
    def __init__(self, screen, player):
        self.start = None # przy pierwszym ruchu zaczyna dopiero sie robic
        self.screen = screen
        self.player = player
        self.current_music = None
        self.map = player.map
        self.game_over = False
        self.elapsed_time = 0
        self.level = 1
        self.jumpscare_fadeout = 0
        self.gg = False
        #nowy epicki paused time ktory naprawia wszystko B)
        self.paused_time = None

        self.min = 0
        self.sec = 0
        self.ms = 0

        self.music_files = {
            1: "Assets/Sounds/bg_dark.mp3",
            2: "Assets/Sounds/bgsound.mp3",
            3: "Assets/Sounds/bg_PPJ.mp3",
            4: "Assets/Sounds/asd.wav"
        }

        self.renderer = Renderer(pygame)
        self.renderer.wall_texture = pygame.image.load("Assets/Textures/servergray.png").convert()
        self.font = pygame.font.Font("Assets/Fonts/messy.ttf", 25)


        self.note_bg = pygame.image.load("Assets/Textures/note_base.png")
        self.pickup_bg = pygame.image.load("Assets/Textures/rj45.png")

        self.notes = [  #NOTATKI DOTYCZACE PIERWSZEGO LVL, TKZ LVL PSM ROMAN MAKS PDF
            Note((11,12), 'Notatka 1:\nCo on tu robi?!\n\nRoman.\nMialem nadzieje, ze juz nigdy go nie spotkam\nA jednak jest.\nZaczalem uciekac w druga strone.\nPoczulem nagly bol.\njakby strzala.\n\nOn zawsze trafia.', self.note_bg, self.font, 1),
            Note((4, 7), "Notatka 2:\nJego zdjecia.\nNasze zdjecia\nprzyjal moja forme\n  zabral mi twarz\n\nczuje jego wzrok\nczuje jego oddech\nczuje jego dotyk\n\nnie moze mnie zlapac. nie moze.", self.note_bg, self.font, 2),
            Note((14, 5), "Notatka 3:\nTo nie byla prawda\ntylko fasada ukrywajaca wszystko\nwypisalem sie z PSM juz dawno temu\n\nmusialem zrobic to znowu.\nGdybym sobie przypomnial\n\nmusialem zejsc glebiej. Musialem zobaczyc prawde", self.note_bg, self.font, 3)
        ]

        self.pickups =[
            Pickup((11,2), self.pickup_bg, 1),
            Pickup((2,11), self.pickup_bg, 2)
        ]



       # self.enemy_sprite = pygame.image.load("Assets/Textures/rock.png")
        self.enemy_sprite = pygame.image.load("Assets/Textures/konwerterJSONnaYAML.png")


        #self.spsize = np.asarray(self.enemy_sprite.get_size())
       # self.spx, self.spy = 13, 15
        self.enemy = Enemy(8, 8, self.map, self.enemy_sprite, pygame.mixer) #srodek kafla

        #pygame.mixer.music.load("Assets/Sounds/bg_dark.mp3")
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("Assets/Sounds/bg_dark.mp3"),-1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("Assets/Sounds/oddychanie.wav"),-1)
        pygame.mixer.Channel(0).set_volume(0.0)
        pygame.mixer.Channel(1).set_volume(0.0)

    def reset(self):
        '''Metoda ta resetuje stan gry oraz przywraca domyślne wartości'''
        self.start = None
        self.paused_time = None
        self.renderer.wall_texture = pygame.image.load("Assets/Textures/servergray.png").convert()
        pygame.mixer.Channel(0).set_volume(0.0) # nie stopuj, tylko wyciszaj
        pygame.mixer.Channel(1).set_volume(0.0)
        self.min = 0
        self.sec = 0
        self.ms = 0
        self.jumpscare_fadeout = 0
        self.player.pos = (self.player.x // TILE_SIZE, self.player.y // TILE_SIZE)

        self.game_over = False

        self.level = 1
        self.map.game_map = MAP1
        self.enemy.x = 9 * TILE_SIZE + TILE_SIZE // 2
        self.enemy.y = 9 * TILE_SIZE + TILE_SIZE // 2
        Map.tiles = {}



        self.player.reset()

        self.enemy.reset()

        Note.count = 0
        Note.total_notes = 0
        for note in self.notes:
            note.collected = False
            note.open_note = False

        self.notes = [  # NOTATKI DOTYCZACE PIERWSZEGO LVL, TKZ LVL PSM ROMAN MAKS PDF
            Note((11, 12),
                 'Notatka 1:\nCo on tu robi?!\n\nRoman.\nMialem nadzieje, ze juz nigdy go nie spotkam\nA jednak jest.\nZaczalem uciekac w druga strone.\nPoczulem nagly bol.\njakby strzala.\n\nOn zawsze trafia.',
                 self.note_bg, self.font, 1),
            Note((4, 7),
                 "Notatka 2:\nJego zdjecia.\nNasze zdjecia\nprzyjal moja forme\n  zabral mi twarz\n\nczuje jego wzrok\nczuje jego oddech\nczuje jego dotyk\n\nnie moze mnie zlapac. nie moze.",
                 self.note_bg, self.font, 2),
            Note((14, 5),
                 "Notatka 3:\nTo nie byla prawda\ntylko fasada ukrywajaca wszystko\nwypisalem sie z PSM juz dawno temu\n\nmusialem zrobic to znowu.\nGdybym sobie przypomnial\n\nmusialem zejsc glebiej. Musialem zobaczyc prawde",
                 self.note_bg, self.font, 3)
        ]
        self.pickups = [
            Pickup((11, 2), self.pickup_bg, 1),
            Pickup((2, 11), self.pickup_bg, 2)
        ]



    def update(self, events, fps):
        '''Metoda ta aktualizuje stan gry, w tym pozycję gracza, przeciwnika, notatek i pickupów,'''
        if self.start is None:  #dopoki gracz sie nie ruszy
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_s]:
                self.enemy.start_chase = True
                self.start = pygame.time.get_ticks() # po pierwszym nacisniecu w/s
                print("Start time:", self.start)

        if self.start is not None:

            elapsed = pygame.time.get_ticks() - self.start
            self.elapsed_time = elapsed
            self.min = int(self.elapsed_time // 60000)
            self.sec = int((self.elapsed_time % 60000) // 1000)
            self.ms = int(self.elapsed_time % 1000)

        if self.gg:
            pygame.mixer.Channel(0).set_volume(0.0)
            pygame.mixer.Channel(1).set_volume(0.0)
            self.reset()
            self.gg = False
            return "gameLose"

        pygame.mixer.Channel(0).set_volume(0.5)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                #zapisuje czas podczas zapauzowania, aby potem wykorzystac go do offsetu czasu w stagemanager
                self.paused_time = self.elapsed_time
                pygame.mixer.Channel(0).set_volume(0.0)
                pygame.mixer.Channel(1).set_volume(0.0)
                for n in self.notes:
                    n.open_note = False
                return "game_start"

            ##
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return "gameLose"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                print(self.elapsed_time)
                return "gameover"

        keys = pygame.key.get_pressed()
        if Note.open_notes:
            Note.show_notes(self.notes, keys, events)
            # musze je rysowac bo inaczej nie dziala scrollowanie
            for n in self.notes:
                if n.open_note:
                    n.draw(self.screen)
            pygame.display.flip()

        #essa
        for n in self.notes:
            if n.open_note:
                keys = pygame.key.get_pressed()
                n.update(self.player.pos, keys, events)
                return "game"

        #Jesli jest enemy blisko gracza, to:
        if self.enemy.distance_to_player(self.player.x, self.player.y) < 40 or Map.get_tile(self.enemy.current_tile()) == Map.get_tile(self.player.pos):
            #jumpscare sound
            pygame.mixer.Channel(2).set_volume(4)
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("Assets/Sounds/jumpsker.wav"))
            #przsecinwik sie tepa na drugi koniec areny
            self.enemy.teleport()
            #gracz traci zycie i jest gg jesli ma 0
            self.gg = self.player.take_damage()
            # Potrzeben zeby jumpscare powoli znikal
            self.jumpscare_fadeout = 500


        keys = pygame.key.get_pressed()
        self.player.move(keys, fps)
        self.enemy.update(self.player)

        for p in self.pickups:
            p.update(self.player, keys)
        for n in self.notes:
            n.update(self.player.pos, keys, events)
        Note.show_notes(self.notes, keys, events)

        if self.player.music != self.current_music:
            self.current_music = self.player.music
            music_path = self.music_files.get(self.current_music) # get dziala bo jest slownik jakby co moj femboyu
            if music_path:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_path),-1)

        #przechodzenie miedzy levelami, nowa mpa,a nowe notatki i game over
        if self.level == 1 and Note.count == 3:
            self.update_level(2)
        elif self.level == 2 and Note.count == 6:
            self.update_level(3)
        elif self.level == 3 and Note.count == 9:
            self.game_over = True
            self.elapsed_time = pygame.time.get_ticks() - self.start
            print(self.elapsed_time)

            pygame.mixer.Channel(0).set_volume(0.0)
            pygame.mixer.Channel(1).set_volume(0.0)
            return "gameover"

        self.draw()
        #tu rysujemy jumpscare hihi
        self.flash_jumpscare()
        self.draw_info()
        pygame.display.flip()
        return "game"

    def update_level(self, lvl):
        '''Metoda ta aktualizuje poziom gry, zmienia mapę, przeciwnika, notatki i pickupy w zależności od poziomu (lvl)'''
        print("ROBIE UPDATE LVL")
        if lvl == 2:
            print("ROBIE LVL 2")
            self.level = 2
            self.map.game_map = MAP2
            if len(self.notes) == 3:                #NOTATKI DOTYCZACE 2 LVL, TKZW LVL TOMASZEW+PCH
                self.notes.append(Note((9, 9), 'Notatka 4:\nPamietam.\n\nBylem na wykladzie z Javy prowadzonym przezz KKMPPNDMIMT\ngdy uslyszalem : „POPRAWKA? Co to takiego?”\n\nNagle zamigotalo wszystko.\n\nObudzilem sie w labiryncie, ogromnych serwerow.\nZ czerwonymi napisami.\n\n„BSS”', self.note_bg, self.font, 4))
                self.notes.append(Note((3, 11), 'Notatka 5:\nZnowu onn. PCH.\nSiedzi w kacie w sweterku, obgryza dlugopis.\n"Algorytm nigdy nie spi"\nTo powiedzial. Nikt sie nie smial\nWyszeptal potem:\n"Kazda petla ma swoje przeznaczenie."\nCzy to grozba?\nNa scianie narysowal drzewo binarne.\n\nOno patrzylo.', self.note_bg, self.font, 5))
                self.notes.append(Note((16, 6), 'Notatka 6:\nPoprawka? Co to jest poprawka? Poprawka? Co to jest \npoprawka? Poprawka? Co to jest poprawka? Poprawka? \nCo to jest poprawka? Poprawka? Co to jest poprawka?\nPoprawka? Co to jest poprawka? Poprawka? Co to \njest poprawka? Poprawka? Co to jest poprawka? Poprawka?\n Co to jest poprawka? Poprawka? Co to jest \npoprawka? Poprawka? Co to jest poprawka? Poprawka?', self.note_bg, self.font, 6))
            self.pickups = [
                Pickup((6,12), self.pickup_bg, 3),
                Pickup((9,4), self.pickup_bg, 4)
            ]
            self.enemy.x = 9 * TILE_SIZE + TILE_SIZE // 2
            self.enemy.y = 1 * TILE_SIZE + TILE_SIZE // 2
            Map.tiles = {}
        elif lvl == 3:
            print("ROBIE LVL 3")
            self.renderer.wall_texture = pygame.image.load("Assets/Textures/serverred.png").convert()
            self.update_level(2)
            self.level = 3
            self.map.game_map = MAP3
            if len(self.notes) == 6:                #NOTATKI DOTYCZACE 3 LVL, TKZW LVL SMYK
                self.notes.append(Note((3, 15),'Notatka 7:\nPoszedlem sprawdzic, skad ten głos.\nZnalazlem go.\n\nPan Adam.\nSiedzial bez ruchu, wpatrzony w ekran.\npowtarzal komendy Basha jak mantre.\nNie moglem sie ruszyc.\nOn kontrolowal wszystko.',self.note_bg, self.font, 7))
                self.notes.append(Note((6, 2),'Notatka 8:\nNie jestem tu sam.\n z oddali słyszę znane słowa.\n"Panie i Panowie".\nMam nadzieje ze to niemozliwe.\nSłabo mi na samą myśl.\n\nMusze to sprawdzic.',self.note_bg, self.font, 8))
                self.notes.append(Note((13, 11),'Notatka 9:\nSzukaja mnie.\nWiedza, ze tu jestem, a ja niewiem nawet ile dni tu spedziłem.\nWidze ich.\nBrunet z lokami, dosyc dziwny.\nCos co probuje mnie imitowac\nMoje najgorsze koszmary\nAle czuje ze jestem juz blisko\n\nSlysze ze cos mnie wola',self.note_bg, self.font, 9))
            self.pickups = [
                Pickup((12, 13), self.pickup_bg, 5),
                Pickup((9, 9), self.pickup_bg, 6)
            ]
            self.enemy.x = 9 * TILE_SIZE + TILE_SIZE // 2
            self.enemy.y = 16 * TILE_SIZE + TILE_SIZE // 2
            Map.tiles = {}
        else:
            print("ROBIE ELSE")
            return

    # ta metodo jest po to zeby wyseiwtlic sprite wroga na ekrani jako jumpscare i powoli go zanikac
    def flash_jumpscare(self):
        '''Metoda ta wyświetla sprite przeciwnika na ekranie jako jumpscare i stopniowo go zanika'''
        if self.jumpscare_fadeout < 1:
            return
        spsurf = pygame.transform.scale(self.enemy.sprite, (WIDTH, HEIGHT)).convert_alpha()
        spsurf.set_alpha(self.jumpscare_fadeout)
        self.screen.blit(spsurf, (0, 0))
        self.jumpscare_fadeout -= 10
        pygame.display.flip()

    def draw_info(self):
        '''Metoda ta rysuje informacje o grze, takie jak prędkość obrotu gracza, czas gry, życie, licznik notatek i pasek staminy'''
        for n in self.notes:
            if n.open_note:
                return

        text_surface = self.font.render(f"Rotation speed: {self.player.rotationSpeed:.4f}", True, WHITE)
        self.screen.blit(text_surface, (10, 10))
        timje_surface = self.font.render(f"Timer: {self.min:02}:{self.sec:02}:{self.ms:0}", True, WHITE)
        self.screen.blit(timje_surface, (600,10))

        counter_text = Note.get_counter_text()
        counter_surf = self.font.render(counter_text,True,RED)
        self.screen.blit(counter_surf,(WIDTH* 0.8,HEIGHT * 0.9))

        stamina_rec = pygame.Rect(WIDTH//4, HEIGHT * 0.9, WIDTH//2, HEIGHT * 0.05)
        stamina_rec.width = (WIDTH//2)/(300/self.player.stamina+0.0001)
        pygame.draw.rect(self.screen,(0,0,255),stamina_rec)

        #zycie jako wifi hehe

        wifi1 = pygame.image.load("Assets/Textures/wififull.png")
        wifi2 = pygame.image.load("Assets/Textures/wifimid.png")
        wifi3 = pygame.image.load("Assets/Textures/wifilow.png")

        wifi_current = wifi1 if self.player.hp == 3 else wifi2 if self.player.hp == 2 else wifi3

        spsurf = pygame.transform.scale(wifi_current, (25, 25))
        self.screen.blit(spsurf, (WIDTH * 0.2, HEIGHT * 0.9))

    def change_music(self, music_file):
        '''Metoda ta zmienia aktualną muzykę w grze na podany plik muzyczny (music_file)'''

        pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_file),-1)
        pygame.mixer.Channel(0).set_volume(0.5)


    def draw(self):
        '''Metoda ta rysuje wszystkie elementy gry na ekranie, w tym tło, ściany, przeciwnika, notatki i pickupy'''

        self.renderer.frame = floor_casting(self.renderer.frame, self.renderer.floorimage)
        surf = pygame.surfarray.make_surface(self.renderer.frame * 255)
        surf = pygame.transform.scale(surf, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(surf, (0, 0))

        z_buffer = cast_ray(self.player.x, self.player.y, self.player.angle, self.map.game_map)
        self.renderer.draw_walls(self.screen, z_buffer, self.player.angle, self.player.x, self.player.y)

        entities_to_draw = [n for n in self.notes if not n.open_note and not n.collected]
        for p in self.pickups:
            if not p.collected:
                entities_to_draw.append(p)
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

        for n in self.notes:
            n.draw(self.screen)
