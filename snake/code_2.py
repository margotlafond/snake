from __future__ import annotations  # noqa: D100

import abc
import argparse
import enum
import random as rd
import typing
import re
from collections.abc import Iterator
from multiprocessing.dummy import Namespace

from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit
from .game_object import GameObject
from .tile import Tile

import pygame

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300
DEFAULT_SQUARE = 20
DEFAULT_FPS = 5
MAX_FPS = 25
MIN_FPS = 2
MIN_WIDTH = 200
MAX_WIDTH = 800
MIN_HEIGHT = 100
MAX_HEIGHT = 600
DEFAULT_FRUIT_COLOR = "#ff0000"
DEFAULT_SN_HEAD_COLOR = "#00ff00"
DEFAULT_SN_BODY_COLOR = "#00ff00"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)



def argu() -> argparse.Namespace:  # noqa: D103
    parser = argparse.ArgumentParser(description="Some description.")
    parser.add_argument("-W", "--width", type=int, default = DEFAULT_WIDTH, help="Screen Width")  # noqa: E501
    parser.add_argument("-H", "--height", type=int, default = DEFAULT_HEIGHT, help="Screen Height")  # noqa: E501
    parser.add_argument("-S", "--square", type=int, default = DEFAULT_SQUARE, help="Checkerboard square size")  # noqa: E501
    parser.add_argument("--fps", type=int, default = DEFAULT_FPS, help="Frames per second")  # noqa: E501
    parser.add_argument("--fruitcolor", default = DEFAULT_FRUIT_COLOR, help="Fruit color")
    parser.add_argument("--snakeheadcolor", default = DEFAULT_SN_HEAD_COLOR, help="Snake head color")  # noqa: E501
    parser.add_argument("--snakebodycolor", default = DEFAULT_SN_BODY_COLOR, help="Snake body color")  # noqa: E501
    parser.add_argument("--gameoveronexit", default = False, help="GameOver when the snake exists")  # noqa: E501
    args = parser.parse_args()

    #Check arguments
    if not(MIN_FPS <= args.fps <= MAX_FPS):
        raise IntRangeError("FPS", args.fps, MIN_FPS, MAX_FPS)

    if not(MIN_WIDTH <= args.width <= MAX_WIDTH):
        raise IntRangeError("Width", args.width, MIN_WIDTH, MAX_WIDTH)

    if not(MIN_HEIGHT <= args.height <= MAX_HEIGHT):
        raise IntRangeError("Height", args.height, MIN_HEIGHT, MAX_HEIGHT)

    if not re.match(r"#[0-9A-Fa-f]{6}$", args.fruitcolor):
        raise ColorError(args.fruitcolor, "--fruitcolor")

    if not re.match(r"#[0-9A-Fa-f]{6}$", args.snakeheadcolor):
        raise ColorError(args.snakeheadcolor, "--snakeheadcolor")

    if not re.match(r"#[0-9A-Fa-f]{6}$", args.snakebodycolor):
        raise ColorError(args.snakebodycolor, "--snakebodycolor")


    return args

#coord taille couleur et appelle screen pour dessiner
#checkeboard : nb lignes, colonnes, taille tile, couleur

#pas nécessaire de prendre size pour la taille : on peut le mettre soit
#dans la fonction draw soit dans attribut de classe
# left : col
# top : line

def snake() -> None:

    args = argu()
    #initialisations : valeurs  # noqa: ERA001
    flag = True
    DEFAULT_STARTING_SNAKE = [(10,7),(10,6),(10,5)]  # noqa: N806
    LINE_INI = 10
    COL_INI = 5
    SIZE_INI = 3
    DEFAULT_DIRECTION = Dir.LEFT  # noqa: N806

    LINES = args.height//args.square #nb de lignes
    COL = args.width//args.square #nb de colonnes

    #initialisations : objets  # noqa: ERA001
    pygame.init()
    try:
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode( (args.width, args.height) )

        checkerboard = Checkerboard(nb_lines = LINES, nb_col = COL, color1 = BLACK, color2 = WHITE)
        # /!\ passer par from pos... pour créer le snake
        snake = Snake.create_from_pos(colorbody=args.snakecolorbody, colorhead = args.snakecolorhead, direction=DEFAULT_DIRECTION, line=LINE_INI, column=COL_INI, size=SIZE_INI, gameover_on_exit = args.gameoveronexit)  # noqa: E501
        #snake = Snake(tiles = DEFAULT_STARTING_SNAKE, direction = DEFAULT_DIRECTION)  # noqa: ERA001
        fruit = Fruit(col=3, line = 3, color=args.fuitcolor)
        board = Board(screen = screen, tile_size = DEFAULT_SQUARE, nb_lines = LINES, nb_cols = COL)

        board.add_object(checkerboard)
        board.add_object(snake)
        board.add_object(fruit)


        while flag:

            clock.tick(args.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    flag = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        flag = False
                    if event.key == pygame.K_RIGHT:
                        snake.dir = Dir.RIGHT
                    elif event.key == pygame.K_LEFT:
                        snake.dir = Dir.LEFT
                    elif event.key == pygame.K_UP:
                        snake.dir = Dir.UP
                    elif event.key == pygame.K_DOWN:
                        snake.dir = Dir.DOWN

            #actualisation of the elements
            snake.move()
            board.draw()

            pygame.display.set_caption(f"Snake - Score: {len(snake)-3}")

            pygame.display.update()

    except GameOver:
        print("You lose !")

    pygame.quit()