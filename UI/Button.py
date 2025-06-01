import pygame
from Game.Settings import *

class Button:
    def __init__(self,rect,text,font_size = 40,color_if_ON = BLUE , color_if_not = RED,text_color = WHITE):

        self.rect = pygame.Rect(rect) #x,y,szer,wys
        self.text = text
        self.font = pygame.font.SysFont(None,int(font_size)) #None - domyslna czcionka sysretmu, mozna zmienic
        self.color_if_ON = color_if_ON #jezeli najedzie sie kursorem na guzik to zmienamny kolor
        self.color_if_not = color_if_not #staly kolor guzika
        self.text_color = text_color
        self.cursor_on_button = False # sprawdzam czy "falga" jset na guziku


        self.text_surface = self.font.render(self.text,True,self.text_color) #font.rect by zmienic tekst na obrazek by wstawic go w guzik
        self.text_rect = self.text_surface.get_rect(center=self.rect.center) #wywoluje get rect i ustawiam teskt na srodku

    def draw(self,surface):

        color = self.color_if_ON if self.cursor_on_button else self.color_if_not
        pygame.draw.rect(surface,color,self.rect)
        surface.blit(self.text_surface,self.text_rect)

    def update(self,mouse_positon): # do kordow
        self.cursor_on_button = self.rect.collidepoint(mouse_positon) #collidepotin - wywolujemy na rect metode ktora sprawdza czy wspolrzene miescza sie wewntarz self.rect jesli tak to zwraca True

    def is_clicked(self,mouse_posiiton, mouse_pressed):
        return self.cursor_on_button and mouse_pressed[0] #czy na guziku i lewy guzik wcisniety