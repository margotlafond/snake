import pygame
import argparse

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300
DEFAULT_SQUARE = 20
SNAKE = [(20*10, 5*20), (20*10, 6*20), (20*10, 7*20)]


def argu():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, default = DEFAULT_WIDTH, help="Screen Width")
    parser.add_argument('-H', '--height', type=int, default = DEFAULT_HEIGHT, help="Screen Height")
    parser.add_argument('-S', '--square', type=int, default = DEFAULT_SQUARE, help="Checkerboard square size")
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


def draw_snake1(square, size, head, line, screen):
    green = (0, 255, 0)
    sn = pygame.Rect(head*square, line*square, size*square, square)
    pygame.draw.rect(screen, green, sn)


def draw_snake(SNAKE, square, screen):
    green = (0, 255, 0)
    for x in SNAKE:
        (line, col) = x
        sn = pygame.Rect(col, line, square, square)
        pygame.draw.rect(screen, green, sn)


def snake():
    
    args = argu()
    pygame.init()
    screen = pygame.display.set_mode( (args.width, args.height) )
    clock = pygame.time.Clock()
    flag = True
    size = 3
    head = 5
    line = 10

    while flag:

        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    flag = False
                    
        screen.fill( (255, 255, 255) )

        checkerboard(screen, args.square, args.height, args.width)

        draw_snake(SNAKE, args.square, screen)

        pygame.display.update()

    pygame.quit()