import pygame
import argparse

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300
DEFAULT_SQUARE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
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
        self._headleft = headleft #n°colonne gauche de la tête du snake
        self._headtop = headtop #n°ligne haut de la tête du snake
        self._snake = [[headtop, headleft + length -1 - i] for i in range(length)] #tête à la fin


    def __repr__(self):
        pass
    
    def __contains__(self, cell):
        """
        cell : cell of the checkerboard [headtop, headleft] wich are the numbers of the lines/columns
        """
        return cell in self._snake 

    def draw(self, screen):
        for coord in self._snake:
            sq_snake = pygame.Rect(coord[1]*self._square, coord[0]*self._square, self._square, self._square)
            pygame.draw.rect(screen, GREEN, sq_snake)
    
    def move(self, COL, LINES, direction):
        l, c = self._snake[-1]

        if direction == 'left':
            if c-1 < 0:
                self._snake.append([l, COL-1])
            else :
                self._snake.append([l, c-1])
            self._snake.pop(0)

        elif direction == 'right':
            if c+1 > COL-1:
                self._snake.append([l, 0])
            else:
                self._snake.append([l, c+1])
            self._snake.pop(0)

        elif direction == 'up':
            if l < 1 :
                self._snake.append([LINES-1, c]) 
            else:   
                self._snake.append([l-1, c])
            self._snake.pop(0)

        elif direction == 'down':
            if l+1 > LINES-1:
                self._snake.append([0, c])
            else:
                self._snake.append([l+1, c])
            self._snake.pop(0)
    
    def grow(self, direction, COL, LINES):
        l, c = self._snake[-1]

        if direction == 'left':
            if c-1 < 0:
                self._snake.append([l, COL-1])
            else :
                self._snake.append([l, c-1])

        elif direction == 'right':
            if c+1 > COL-1:
                self._snake.append([l, 0])
            else:
                self._snake.append([l, c+1])

        elif direction == 'up':
            if l < 1 :
                self._snake.append([LINES-1, c]) 
            else:   
                self._snake.append([l-1, c])

        elif direction == 'down':
            if l+1 > LINES-1:
                self._snake.append([0, c])
            else:
                self._snake.append([l+1, c])


    
class Fruit:
    def __init__(self, square, line, col, score):
        self._square = square
        self._line = line
        self._col = col
        self._score = score

    def position(self):
        return [self._line, self._col]
    
    def draw(self, screen):  
        fruit = pygame.Rect(self._col*self._square, self._line*self._square, self._square, self._square)
        pygame.draw.rect(screen, RED, fruit)








def snake():
    
    args = argu()
    direction = 'left'
    sn_lenght = 3
    sn_line = 10
    sn_col = 5
    pygame.init()
    screen = pygame.display.set_mode( (args.width, args.height) )
    clock = pygame.time.Clock()
    flag = True
    LINES = args.height//args.square
    COL = args.width//args.square
    checkerboard = Checkerboard(LINES, COL, BLACK, WHITE, args.square)
    snake = Snake(sn_lenght, args.square, sn_col, sn_line)
    score = 0
    fruit = Fruit(args.square, 3, 3, score)

    while flag:

        clock.tick(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    flag = False
                if event.key == pygame.K_RIGHT:
                    direction = 'right'
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    
        #screen.fill( (255, 255, 255) )
        #checkerboard(screen, args.square, args.height, args.width)
        #draw_snake(GLOB_SNAKE, args.square, screen)
        checkerboard.draw(screen)
        
        fruit.draw(screen)
        snake.draw(screen)
        snake.move(COL, LINES, direction)

        if fruit.position() in snake:
            snake.grow(direction, COL, LINES)
            score += 1
            if score%2 != 0:
                fruit = Fruit(args.square, 10, 15, score)
            else:
                fruit = Fruit(args.square, 3, 3, score)

        pygame.display.set_caption(f"Snake - Score: {score}")


        pygame.display.update()

    pygame.quit()