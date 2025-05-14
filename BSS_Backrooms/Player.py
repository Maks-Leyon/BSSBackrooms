import pygame
from Settings import *
from Map import Map

Map = Map()
class Player:
    def __init__(self):
        self.x = 12 * TILE_SIZE
        self.y = 13 * TILE_SIZE
        self.angle= -(math.pi/2)
        self.speed = 1.6
        self.rotationSpeed = 0.03

    def move(self,keys):

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            self.angle -= self.rotationSpeed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotationSpeed
        if keys[pygame.K_w]:
            dx += self.speed * math.cos(self.angle)
            dy += self.speed * math.sin(self.angle)
            print(dx, dy, "HEHEHEHEH")
        if keys[pygame.K_s]:
            dx -= self.speed * math.cos(self.angle)
            dy -= self.speed * math.sin(self.angle)
            print(dx, dy, "bzzzzz")



        if not Map.is_wall(self.x + dx, self.y):
            self.x += dx
            #print(self.x, "< - Moj x hehe")
        if not Map.is_wall(self.x, self.y + dy):
            self.y += dy
            #print(self.y, "< - Moj x hehe")





