import json

import pygame.time

from Note import Note
class SaveAndLoad:
    @staticmethod
    def saveGame(game, file="Assets/savegame.txt"):
        with open(file, "w") as f:
            f.write(f"{game.elapsed_time}\n")
            f.write(f"{game.player.x} {game.player.y} {game.player.rotationSpeed}\n")
            print("ddddddddddddddddddddddddddddddddddddddddddddddddddd")
            f.write(f"{game.enemy.x} {game.enemy.y} {game.enemy.stamina}\n")
            f.write(f"{Note.count}\n")
            for note in game.notes:
                coll = 1 if note.collected else 0
                f.write(f"{coll}\n")


    @staticmethod
    def loadGame(game, file="Assets/savegame.txt"):
        with open(file,"r") as f:
            lines = f.readlines()
            elapsed = int(lines[0].strip())
            game.start = pygame.time.get_ticks() - elapsed

            px,py,rot = map(float, lines[1].split()) # map konwertuje obiekty, tu na float
            game.player.x = px
            game.player.y = py
            game.player.rotationSpeed = rot

            ex,ey,stam = map(float,lines[2].split())
            game.enemy.x = ex
            game.enemy.y = ey
            game.enemy.stamina = stam
            note_count = int(lines[3].strip())
            Note.count = note_count
            for i, line in enumerate(lines[4:]):
                col = bool(int(line.strip()))
                game.notes[i].collected = col

