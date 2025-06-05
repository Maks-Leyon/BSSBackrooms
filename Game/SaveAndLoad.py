import json

import pygame.time

from Note import Note
class SaveAndLoad:
    @staticmethod
    def saveGame(game, file="Assets/SaveFiles/savegame.txt"):
        with open(file, "w") as f:
            f.write(f"{game.elapsed_time}\n")
            #dodalem stamine i angle
            f.write(f"{game.player.x} {game.player.y} {game.player.rotationSpeed} {game.player.angle} {game.player.stamina}\n")
            print("ddddddddddddddddddddddddddddddddddddddddddddddddddd")
            f.write(f"{game.enemy.x} {game.enemy.y} {game.enemy.stamina}\n")
            f.write(f"{Note.count} {game.level}\n")
            for note in game.notes:
                coll = 1 if note.collected else 0
                f.write(f"{coll}\n")


    @staticmethod
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
                game.notes[i].collected = col


    @staticmethod
    def saveInfo(nick,elapsed_time,file="Assets/SaveFiles/saveinfo.txt"):
        with open(file, "a") as f:
            f.write(f"{nick} {elapsed_time}\n")

    @staticmethod
    def loadInfo(file="Assets/SaveFiles/saveinfo.txt"):
        players = []
        with open(file, "r") as f:
            lines =f.readlines()
        for line in lines:
            part = line.strip().split()
            nick = part[0]
            time = int(part[1])
            players.append((nick,time))

        players.sort(key=lambda x : x[1]) #domyslnie sortuje rosnaco

        return players[:5] #narazie tylko 5 mozna zwiekszyc


