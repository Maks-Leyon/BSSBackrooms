import pygame

from Settings import *

class Map:
    def __init__(self):
            self.game_map = [
                [1,1,1,1,1,1,1,1,1],
                [1,0,1,0,0,0,0,0,1],
                [1,0,0,0,0,0,1,0,1],
                [1,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,1,1],
                [1,1,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1],
            ]

    def is_wall(self, x, y):
        i = int(x // TILE_SIZE)
        j = int(y // TILE_SIZE)
        if 0 <= i < len(self.game_map[0]) and 0 <= j < len(self.game_map):
            return self.game_map[j][i] == 1
        return True

    def render(self,screen,x,y,width,height,color):
        pygame.draw.rect(screen,(color,color,color),(x,y,width,height))


