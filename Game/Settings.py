import math
#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BROWN = (102, 51, 51)
CYAN = (0, 255, 255)
GRAY = (128,128,128)


#
WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2
HALF_WIDTH = WIDTH //2
VRESOLUTION = int(HALF_HEIGHT // 3) #Zakładam że wertykalna rozdzielczość to połowa wysokości, a to jest połowa tego
TILE_SIZE = 64
MAP_WIDTH = 20 * TILE_SIZE
MAP_HEIGHT = 20 * TILE_SIZE
FOV = math.pi / 3.5