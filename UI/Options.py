import pygame


from Game.Settings import HALF_HEIGHT, HALF_WIDTH, WHITE, WIDTH
from UI.Button import Button
from UI.Slider import Slider
from Game import Settings

class Options:
    def __init__(self,screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont(None, 60)
        self.background = pygame.image.load("Assets/Textures/konwerterJSONnaYAML.png")
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))
        min_speed = 0.001 # rotacja
        max_speed = 0.01
        initial_val = max(min((player.rotationSpeed - min_speed) / (max_speed - min_speed), 1), 0)
        self.slider = Slider(HALF_WIDTH, HALF_HEIGHT, (500,30), initial_val, min_speed, max_speed)

        self.buttons = [ Button((WIDTH * 0.1,320,WIDTH * 0.15,50), "Creepy"),
                         Button( (WIDTH * 0.3,320,WIDTH * 0.15,50), "Friends"),
                         Button((WIDTH * 0.5,320,WIDTH * 0.15,50), "Femboys"),
                         Button((WIDTH * 0.7,320,WIDTH * 0.15,50), "ASD"),
                         Button((WIDTH * 0.4, 450, WIDTH * 0.2, 50), "How to Play")
                         ]

    #USELSS XDDDDDDDDDDDDDDDDDDDDDD
    def creepZursynowa(self):
        self.player.music = 1
    def maksPalkowskiMaPowiazaniaZFederacjaRosyjska(self):
        self.player.music = 2
    def NiktNieLubiKubyPawlika(self):
        self.player.music = 3



    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.slider.container_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            self.slider.move(mouse_pos)
            self.player.rotationSpeed = self.slider.get_val()
            print(self.player.rotationSpeed)

        for button in self.buttons:
            button.update(mouse_pos) #dla kazdej pozycji sprawdzane czy myszka ni jest na guziku


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #jednorazowo za kazda proba klikniecia
                for button in self.buttons:
                    if button.is_clicked(mouse_pos, mouse_pressed):
                        if button.text == "How to Play":
                            return "how_to_play"
                        print("fueah")
                        return button.text

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "Menu"

        self.draw()
        return "options" # jak nic sie nie zemin to zostjamy w options


    def draw(self):
        label = self.font.render("Czułość obrotu",True, WHITE)
        label2 = self.font.render("Muzyka w grze", True, WHITE)
        self.screen.fill((0, 0, 0))
        self.screen.blit(label,(250,80))
        self.screen.blit(label2, (250,250))

        self.slider.render(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()