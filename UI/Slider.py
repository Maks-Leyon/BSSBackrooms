import pygame
from Game.Settings import  *

class Slider:
    def __init__(self, x, y, size : tuple, val : float, min_val : float, max_val : float):
        self.x = x
        self.y = y# to tuple bo ustawiam srodek ekranu (Hal_WIDTH i HALF_HEIGHT)
        self.size = size

        # konce suwakow
        self.slider_left_pos = self.x - (size[0]//2)
        self.slider_right_pos = self.x + (size[0] // 2)
        self.slider_top_pos = self.y - (size[1] // 2) - 150

        self.min = min_val #min wartosc suwak
        self.max = max_val # max wartosc suwak
        self.val = (self.slider_right_pos - self.slider_left_pos) * val # %, poczatkowa watosc sywaka

        self.container_rect = pygame.Rect(self.slider_left_pos,self.slider_top_pos,self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.val - 5, self.slider_top_pos, 10, self.size[1])

    def move(self, mouse_pos):
        '''Metoda ta odpowiada za aktualizowanie sie widoczengo slidera, gdy uzytkownik go przeciaga'''
        new_x = mouse_pos[0] # pozycja na podstawie osi x nowa
        #ograncizenie za lewy a nizej za prawy
        if new_x < self.slider_left_pos:
            new_x = self.slider_left_pos
        if new_x > self.slider_right_pos:
            new_x = self.slider_right_pos
        self.button_rect.centerx = new_x
        self.val = new_x # update

    def get_val(self):
        '''Metoda ta odpowiada za zmiane wartosci z pikseli na liczbowe'''
        val_range = self.slider_right_pos - self.slider_left_pos # calokowity zakres
        button_val = self.button_rect.centerx - self.slider_left_pos # odleglosc od lewej, centerx pozycja w poziomie

        return (button_val/val_range) *(self.max - self.min) + self.min # wartiosc jako proporcja odleglosci

    def render(self,screen):
        '''Metoda ta odpowiada za renderowanie elementow suwaka'''
        pygame.draw.rect(screen, GRAY, self.container_rect)
        pygame.draw.rect(screen, RED, self.button_rect)


