import pygame
import argparse

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300
DEFAULT_SQUARE = 20


def argu():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, default = DEFAULT_WIDTH, help="Screen Width")
    parser.add_argument('-H', '--height', type=int, default = DEFAULT_HEIGHT, help="Screen Height")
    parser.add_argument('-S', '--square', type=int, default = DEFAULT_SQUARE, help="Checkerboard square size")
    args = parser.parse_args()
    return args

def checkerboard(screen, square, height, width):

    i = 0
    noir = (0, 0, 0)
    cpt = 0

    for j in range(0, height, square):
        for i in range(0, width, square):
            if cpt == 0:
                rect = pygame.Rect(i, j, square, square)
            else:
                rect = pygame.Rect(i+square, j, square, square)
            cpt += 1
            pygame.draw.rect(screen, noir, rect)



def snake():
    
    args = argu()
    pygame.init()
    screen = pygame.display.set_mode( (args.width, args.height) )
    clock = pygame.time.Clock()
    flag = True

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

        pygame.display.update()

    pygame.quit()