import pygame
from Settings import *
from Game.Map import Map

class Player:
    def __init__(self, gamemap):
        self.start_x = 12 * TILE_SIZE
        self.start_y = 13 * TILE_SIZE

        self.x = self.start_x
        self.y = self.start_y
        self.pos = (self.x//TILE_SIZE,self.y//TILE_SIZE)
        self.angle= -(math.pi/2)
        self.speed = 0.05
        self.rotationSpeed = 0.002
        self.music = 1
        self.map = gamemap



    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.pos = (self.x // TILE_SIZE, self.y // TILE_SIZE)
        self.angle = -(math.pi / 2)
        self.speed = 0.05
        self.rotationSpeed = 0.002
        self.music = 1
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

      #  print(self.x//TILE_SIZE, self.y//TILE_SIZE, self.angle)
        #print(f"Gracz poz: x={self.x:.1f}, y={self.y:.1f}, angle mrodo={self.angle}, ({self.x//TILE_SIZE},{self.y//TILE_SIZE})")
        print(f"Gracz: ({self.x//TILE_SIZE},{self.y//TILE_SIZE})")

        if not self.map.is_wall(self.x + dx, self.y):
            self.x += dx
            #print(self.x, "< - Moj x hehe")
        if not self.map.is_wall(self.x, self.y + dy):
            self.y += dy
            #print(self.y, "< - Moj x hehe")

        self.pos = (self.x // TILE_SIZE, self.y // TILE_SIZE)
