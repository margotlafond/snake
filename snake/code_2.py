import pygame
import argparse

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300


def argu():
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-W', '--width', type=int, default = DEFAULT_WIDTH, help="Screen Width")
    parser.add_argument('-H', '--height', type=int, default = DEFAULT_HEIGHT, help="Screen Height")
    args = parser.parse_args()
    return args


def snake():
    
    args = argu()
    pygame.init()
    screen = pygame.display.set_mode( (args.width, args.height) )
    clock = pygame.time.Clock()
    var = True

    while var:

        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                var = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    var = False
                    
        screen.fill( (255, 255, 255) )

        pygame.display.update()

    pygame.quit()