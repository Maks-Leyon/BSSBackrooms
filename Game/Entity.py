class Entity:
    '''Ta klasa reprezentuje obiekt w grze, który posiada pozycję (x, y), graficzną reprezentację (sprite) oraz rozmiar (size).'''
    def __init__(self,sprite, x, y, size):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.size = size

    def distance_to_player(self, px, py):
        '''Metoda ta zwraca dystans do podanych koordynatów px, py za pomocą wzoru Euklidesowego'''
        return ((self.x - px) ** 2 + (self.y - py) ** 2) ** 0.5