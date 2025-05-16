import pygame
from Settings import *
from Map import Map

Map = Map()
class Player:
    def __init__(self):
        self.x = 12 * TILE_SIZE
        self.y = 13 * TILE_SIZE
        self.angle= -(math.pi/2)
        self.speed = 0.05
        self.rotationSpeed = 0.001

    # Na necie przeczytalem ze jak pomnozysz przez clock.tick() to wtedy masz szybkosc niezależną od fps wiec nie bedzie
    # np. roznych szybkosci na lepszych/gorszych kompach
    def move(self,keys, framerate):

        dx = 0
        dy = 0

        #sprint
        if keys[pygame.K_LSHIFT]:
            self.speed = 0.1
        else:
            self.speed = 0.05

        if keys[pygame.K_LEFT]:
            self.angle -= self.rotationSpeed * framerate
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotationSpeed * framerate
        if keys[pygame.K_w]:
            dx += self.speed * math.cos(self.angle) * framerate
            dy += self.speed * math.sin(self.angle) * framerate
        if keys[pygame.K_s]:
            dx -= self.speed * math.cos(self.angle) * framerate
            dy -= self.speed * math.sin(self.angle) * framerate



        if not Map.is_wall(self.x + dx, self.y):
            self.x += dx
            #print(self.x, "< - Moj x hehe")
        if not Map.is_wall(self.x, self.y + dy):
            self.y += dy
            #print(self.y, "< - Moj x hehe")





