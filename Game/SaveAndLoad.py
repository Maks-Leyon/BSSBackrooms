import json

import pygame.time
from peewee import DoesNotExist

from Game.Db import db, GameInfo, PlayerInfo, EnemyInfo, NoteModel, WinInfo, PickupModel
from Game.Note import Note

class SaveAndLoad:

    @staticmethod
    def saveGame(game):
        '''Metoda ta sluzy do zapisania danych gry w bazie ORM po calkowitym wyjsciu z aplikacji, zapisywane sa najwazniejsze informacje, w tym polozenie gracza, Enemy, obecna ilosc zebranych notatek, czy obecny czas, potrzebna jest ona do pozniejszego mozliwego wczytania gry'''
        #operacje atomowe, by w razie bledu nastapil rollback wszystkich danych
        with db.atomic():
            #Usuwamy wszystkie dane dotyczace ostatniego zapisu
            PlayerInfo.truncate_table()
            EnemyInfo.truncate_table()
            GameInfo.truncate_table()
            NoteModel.truncate_table()
            PickupModel.truncate_table()

            #Tworzymy nowe info
            PlayerInfo.create(
                x=game.player.x,
                y=game.player.y,
                rotationSpeed=game.player.rotationSpeed,
                angle=game.player.angle,
                stamina=game.player.stamina,
                hp = game.player.hp
            )
            EnemyInfo.create(
                x=game.enemy.x,
                y=game.enemy.y,
                stamina=game.enemy.stamina,
                start_chase=game.enemy.start_chase
            )
            GameInfo.create(
                elapsed_time=game.elapsed_time,
                paused_time=game.paused_time,
                level=game.level,
                note_count=Note.count
            )

            for note in game.notes:
                NoteModel.create(
                    index=note.no,
                    collected=note.collected
                )

            for pickup in game.pickups:
                PickupModel.create(
                    index=pickup.no,
                    collected=pickup.collected
                )

    '''@staticmethod
    def saveGame(game):
        with open(file, "w") as f:
            f.write(f"{game.elapsed_time}\n")
            #dodalem stamine i angle
            f.write(f"{game.player.x} {game.player.y} {game.player.rotationSpeed} {game.player.angle} {game.player.stamina}\n")
            f.write(f"{game.enemy.x} {game.enemy.y} {game.enemy.stamina}\n")
            f.write(f"{Note.count} {game.level}\n")
            for note in game.notes:
                coll = 1 if note.collected else 0
                f.write(f"{coll}\n")'''

    @staticmethod
    def loadGame(game):
        '''Metoda ta sluzy do odtworzenia danych zapisanych metoda SaveGame z bazy ORM, by gracz mogl rozpoczac rozgrywke od momentu zamkniecia gry'''
        #try w razie jakby to byla pierwsza gra i nie ma zapisanych plikow
        try:
            # powinno wystarczyc get bez warunku zadnego bo i tak jest jeden rekord
            player_data = PlayerInfo.get()
            game.player.x = player_data.x
            game.player.y = player_data.y
            game.player.rotationSpeed = player_data.rotationSpeed
            game.player.angle = player_data.angle
            game.player.stamina = player_data.stamina
            game.player.hp = player_data.hp

            game_info = GameInfo.get()
            Note.count = game_info.note_count

            game.elapsed_time = game_info.elapsed_time
            game.start = pygame.time.get_ticks() - game_info.elapsed_time
            game.level = game_info.level

            game.update_level(game_info.level)
            print(len(game.notes))

            enemy_data = EnemyInfo.get()
            game.enemy.x = enemy_data.x
            game.enemy.y = enemy_data.y
            game.enemy.stamina = enemy_data.stamina
            game.enemy.start_chase = enemy_data.start_chase

            for note in NoteModel:
                for n in game.notes:
                    if n.no == note.index:
                        n.collected = note.collected

            for pickup in PickupModel:
                for p in game.pickups:
                    if p.no == pickup.index:
                        p.collected = pickup.collected


        except DoesNotExist:
            game.reset()

    '''@staticmethod
    def loadGame(game, file="Assets/SaveFiles/savegame.txt"):
      #  game.game_over = False
        with open(file,"r") as f:
            lines = f.readlines()
            elapsed = int(lines[0].strip())
            game.start = pygame.time.get_ticks() - elapsed

            px,py,rot,ang,stam = map(float, lines[1].split()) # map konwertuje obiekty, tu na float
            game.player.x = px
            game.player.y = py
            game.player.rotationSpeed = rot
            #dodalem stamine i angle
            game.player.angle = ang
            game.player.stamina = stam

            ex,ey,stam = map(float,lines[2].split())
            note_count, lvl = map(int,lines[3].split())
            Note.count = note_count
            game.level = lvl
            game.update_level(lvl)
            #update przeciwnika po updacie lvla zeby pozycje byle lepsze
            game.enemy.x = ex
            game.enemy.y = ey
            game.enemy.stamina = stam
            for i, line in enumerate(lines[4:]):
                col = bool(int(line.strip()))
                game.notes[i].collected = col'''


    @staticmethod
    def saveInfo(nick,elapsed_time):
        '''Metoda ta odpowiada za zapisywanie informacji o graczu, ktory ukonczyl gre w Bazie ORM, zapisywany jest jego nick oraz czas w jakim ukonczyl gre'''
        with db.atomic():
            WinInfo.create(
                time = elapsed_time,
                nick = nick
            )

    @staticmethod
    def loadInfo():
        '''Metoda ta odpowiada za odczytywanie informacji z bazy danych ORM, wykorzystywana jest w klasie Ranking w ktorej wizualnie odtwarzane sa informacje o najlepszych graczach'''
        players = []
        #limit 5 dla 5 najlepszych
        for info in WinInfo.select().order_by(WinInfo.time.asc()).limit(5):
            players.append((info.nick, int(info.time)))
        return players


