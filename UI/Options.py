import pygame


class Options:
    def __init__(self,screen):
        self.screen = screen
        self.background = pygame.image.load("Assets/Textures/konwerterJSONnaYAML.png")
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))



    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        self.draw()
        return "options" # jak nic sie nie zemin to zostjamy w options


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()