class Entity:
    def __init__(self,sprite, x, y, size):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.size = size

    def distance_to_player(self, px, py):
        return ((self.x - px) ** 2 + (self.y - py) ** 2) ** 0.5