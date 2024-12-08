import pygame
import argparse

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300
DEFAULT_SQUARE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GLOB_SNAKE = [(20*10, 5*20), (20*10, 6*20), (20*10, 7*20)]


def argu():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, default = DEFAULT_WIDTH, help="Screen Width")
    parser.add_argument('-H', '--height', type=int, default = DEFAULT_HEIGHT, help="Screen Height")
    parser.add_argument('-S', '--square', type=int, default = DEFAULT_SQUARE, help="Checkerboard square size")
    #parser.add_argument('-L', '--lines', type=int, default = DEFAULT_LINES, help="Number of lines")
    args = parser.parse_args()
    return args


def checkerboard(screen, square, height, width):

    noir = (0, 0, 0)
    cpt = 0

    for i in range(0, width, square):
        for j in range(0, height, 2*square):
            if cpt%2 == 0:
                rect = pygame.Rect(i, j, square, square)
            else:
                rect = pygame.Rect(i, j+square, square, square)
            pygame.draw.rect(screen, noir, rect)
        cpt += 1

def draw_snake(GLOB_SNAKE, square, screen):
    green = (0, 255, 0)
    for x in GLOB_SNAKE:
        (line, col) = x
        sn = pygame.Rect(col, line, square, square)
        pygame.draw.rect(screen, green, sn)

#coord taille couleur et appelle screen pour dessiner
#checkeboard : nb lignes, colonnes, taille tile, couleur

class Tile:
    def __init__(self, size, color, coord):
        self._size = size
        self._color = color
        self._coordleft, self._coordtop = coord
        self._tile = pygame.Rect(self._coordleft, self._coordtop, self._size, self._size)
    
    def __repr__(self):
        return f"Tile of size {self._size} on a screen on position x={self._coordx}, y={self._coordy}"

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self._tile)


class Checkerboard:
    def __init__(self, lines, columns, color1, color2, tile_size):
        self._lines = lines
        self._columns = columns
        self._color1  = color1
        self._color2  = color2
        self._tile_size = tile_size

    def __repr__(self):
        pass

    def draw(self, screen):
        for i_line in range(self._lines):
            for i_col in range(self._columns):
                if (i_line + i_col) %2 == 0:
                    tile = Tile(self._tile_size, self._color1, (i_col*self._tile_size, i_line*self._tile_size))
                else:
                    tile = Tile(self._tile_size, self._color2, (i_col*self._tile_size, i_line*self._tile_size))
                tile.draw(screen)

class Snake :
    def __init__(self, length, square, headleft, headtop):
        self._square = square #taille des carrés composant le snake 
        self._length = length #longueur du snake
        self._headleft = headleft #coordonnées gauche de la tête du snake
        self._headtop = headtop #coordonnées haut de la tête du snake
        self._snake = pygame.Rect(self._headleft, self._headtop, self._square*self._length, self._square)

    def __repr__(self):
        return f"The snake is {self._length} long and the size of the squares is {self._square}."

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self._snake)




def snake():
    
    args = argu()
    pygame.init()
    screen = pygame.display.set_mode( (args.width, args.height) )
    clock = pygame.time.Clock()
    flag = True
    LINES = args.height//args.square
    COL = args.width//args.square
    checkerboard = Checkerboard(LINES, COL, BLACK, WHITE, args.square)
    snake = Snake(3, args.square, 5*args.square, 10*args.square)

    while flag:

        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    flag = False
                    
        #screen.fill( (255, 255, 255) )
        #checkerboard(screen, args.square, args.height, args.width)
        #draw_snake(GLOB_SNAKE, args.square, screen)
        checkerboard.draw(screen)
        snake.draw(screen)
        pygame.display.update()

    pygame.quit()