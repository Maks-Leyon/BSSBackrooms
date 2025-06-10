import pygame
from Game.Settings import *

class Button:
    '''Ta klasa reprezentuje Guzik, który jest używany do klikania w guzik, pobiera ona prostokat(rect),teskt guzika(text), ustawia wielkosc czcionki domyslnie(font_size=40),kolor guzika gdy jest na nim myszka ustawiony na niebieski(color_if_ON = BLUE), kolor guzika gdy nie ma na nim myszki ustawiony na czerwony(color_if_not = RED) oraz kolor tekstu widocznego na guziku ustawiony na bialy(text_color = WHITE) jako argumenty inicjalizacyjne'''
    def __init__(self,rect,text,font_size = 40,color_if_ON = BLUE , color_if_not = RED,text_color = WHITE):

        self.rect = pygame.Rect(rect) #x,y,szer,wys
        self.text = text
        self.font = pygame.font.SysFont(None,int(font_size)) #None - domyslna czcionka sysretmu, mozna zmienic
        self.color_if_ON = color_if_ON #jezeli najedzie sie kursorem na guzik to zmienamny kolor
        self.color_if_not = color_if_not #staly kolor guzika
        self.text_color = text_color
        self.cursor_on_button = False # sprawdzam czy "falga" jset na guziku


        #bez bg
        self.color = BLACK
        self.text_color1 = BLACK
        self.font1 = pygame.font.Font("Assets/Fonts/messy.ttf", 40)
        self.text_surface = self.font1.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.text_surface1 = self.font1.render(self.text, True,
                                             self.text_color1)
        self.text_rect1 = self.text_surface1.get_rect(center=self.rect.center)



        self.text_surface = self.font.render(self.text,True,self.text_color) #font.rect by zmienic tekst na obrazek by wstawic go w guzik

        self.text_rect = self.text_surface.get_rect(center=self.rect.center) #wywoluje get rect i ustawiam teskt na srodku






    def update(self,mouse_positon): # do kordow
        '''Metoda ta odpowiada za sorawdzenie czy mouse_position znajduje sie na przycisku, jest to potrzebne do pozniejszego wywolywania akcji guzika, rowniez sluzy do zmiany koloru guzika gdy myszka jest na nim'''
        self.cursor_on_button = self.rect.collidepoint(mouse_positon) #collidepotin - wywolujemy na rect metode ktora sprawdza czy wspolrzene miescza sie wewntarz self.rect jesli tak to zwraca True

    def is_clicked(self,mouse_posiiton, mouse_pressed):
        '''Metoda ta zwraca wartosc boolean - czy guzik ( a dokladniej czy w jego wymiarach) zostal klikniety guzik'''
        return self.cursor_on_button and mouse_pressed[0] #czy na guziku i lewy guzik wcisniety

    def drawWithouBG(self,screen):
        '''Metoda ta odpowaida za rysowanie jednego guzika ale bez tła Sam napis, ktory dziala jak guzik'''
        screen.blit(self.text_surface1, self.text_rect1)

    def draw(self,surface):
        '''Metoda ta odpowiada za rysowanie jednego guzika, Prostokata wokol niego oraz tesktu na prostokacie'''

        color = self.color_if_ON if self.cursor_on_button else self.color_if_not
        pygame.draw.rect(surface,color,self.rect)
        surface.blit(self.text_surface,self.text_rect)