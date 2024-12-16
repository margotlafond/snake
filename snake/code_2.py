from __future__ import annotations  # noqa: D100

import abc
import argparse
import enum
import random as rd
from collections.abc import Iterator
from multiprocessing.dummy import Namespace
from typing import Any, NoReturn

import pygame

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300
DEFAULT_SQUARE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def argu() -> Namespace:  # noqa: D103
    parser = argparse.ArgumentParser(description="Some description.")
    parser.add_argument("-W", "--width", type=int, default = DEFAULT_WIDTH, help="Screen Width")  # noqa: E501
    parser.add_argument("-H", "--height", type=int, default = DEFAULT_HEIGHT, help="Screen Height")  # noqa: E501
    parser.add_argument('-S', '--square', type=int, default = DEFAULT_SQUARE, help="Checkerboard square size")  # noqa: E501
    args = parser.parse_args()
    return args

#coord taille couleur et appelle screen pour dessiner
#checkeboard : nb lignes, colonnes, taille tile, couleur

class Observer(abc.ABC):  # noqa: B024, D101

    def __init__(self) -> None:  # noqa: D107
        super().__init__()

    def notify_object_eaten(self, obj: "GameObject") -> None:  # noqa: B027, D102
        pass

    def notify_object_moved(self, obj: "GameObject") -> None:  # noqa: B027, D102
        pass

    def notify_collision(self, obj: "GameObject") -> None:  # noqa: B027, D102
        pass

class Subject(abc.ABC):  # noqa: B024, D101

    def __init__(self) -> None:  # noqa: D107
        super().__init__()
        self._observers: list[Observer] = []

    @property
    def observers(self) -> list[Observer]:  # noqa: D102
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        print(f"Attach {obs} as observer of {self}.")
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        print(f"Detach observer {obs} from {self}.")
        self._observers.remove(obs)

class Dir(enum.Enum) :  # noqa: D101
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

class Board(Subject, Observer):  # noqa: D101 #subject and observer bc prévient des collisions

    def __init__(self: Any, screen: pygame.Surface, tile_size: Any, nb_lines: int, nb_cols: int) -> None:  # noqa: ANN401, D107
        self._screen = screen
        self._tile_size = tile_size
        self._objects: list[object] = []
        self._nb_lines = nb_lines
        self._nb_cols = nb_cols

    def draw(self) -> None:  # noqa: D102
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    def add_object(self: Any, gameobject: Any) -> None:  # noqa: ANN401, D102
        self._objects.append(gameobject)
        gameobject.attach_obs(self) #becomes the observer of the object

    def remove_object(self, gameobject: "GameObject") -> None:
        gameobject.detach_obs(self)
        self._objects.remove(gameobject)

    def create_fruit(self) -> None:
        fruit = None
        while fruit is None or not self.detect_collision(fruit) is None:
            fruit = Fruit(color = pygame.Color("red"), col = rd.randint(0, self._nb_cols-1), line=rd.randint(0, self._nb_lines-1))

    def detect_collision(self, obj:GameObject) -> GameObject | None:
        for o in self._object:
            if o != obj and not(o.background) and o in obj:
                return o
        return None

    def notify_object_moved(self, obj: "GameObject") -> None:
        """Collision detection."""
        o = self.detect_collision(obj)
        if not o is None:
            obj.notify_collision(o)
    
    def notify_object_eaten(self, obj: "GameObject") -> None:  # noqa: D102
        self.remove_object(obj)
        self.create_fruit()

class GameObject(Subject, Observer):  # noqa: D101

    def __init__(self: Any) -> None:  # noqa: D107
        super().__init__()

    def __contains__(self, obj: object) -> bool:  # noqa: D105
        if isinstance(obj, GameObject):
            return any(t in obj.tiles for t in self.tiles)
        return False

    @property
    @abc.abstractmethod
    def tiles(self) -> NoReturn:  # noqa: D102
        raise NotImplementedError

    @property
    def backgroung(self) -> bool:  # noqa: D102
        return False #by default, GameObject isn't a background

class Tile:  # noqa: D101
    def __init__(self: Any, line: int, color: tuple, column: int) -> None:  # noqa: D107
        self._line = line
        self._color = color
        self._column = column

    def draw(self, screen: pygame.Surface, tile_size: int) -> None:
        tile = pygame.Rect(self._column*tile_size, self._line*tile_size, tile_size, tile_size)  # noqa: E501
        pygame.draw.rect(screen, self._color, tile)

    def __add__(self, other: Any) -> Tile:
        if not isinstance(other, Dir):
            msg = "The added element class is not Dir."
            raise ValueError(msg)  # noqa: TRY004
        return Tile(self._line + other.value[1], self._column + other.value[0], self._color)  # noqa: E501

#pas nécessaire de prendre size pour la taille : on peut le mettre soit
#dans la fonction draw soit dans attribut de classe
# left : col
# top : line

class Checkerboard(GameObject):  # noqa: D101
    def __init__(self, nb_lines: int, nb_col: int, color1: tuple, color2:tuple) -> None: # noqa: D107
        self._lines = nb_lines
        self._col = nb_col
        self._color1  = color1
        self._color2  = color2

    @property
    def tiles(self) -> Generator[Tile, Any, None]:  # noqa: D102
        for line in range(self._lines):
            for column in range(self._col):
                yield Tile(line=line, column=column, color=self._color1 if (line+column)%2==0 else self._color2)  # noqa: E501

    @property
    def background(self) -> bool:
        return True

class Snake(GameObject):
    """Snake class controled by the player."""

    def __init__(self, tiles: list[Tile], direction: Dir) -> None:  # noqa: D107
        self._tiles = tiles #list of the tiles that constitute the snake, head first
        self._direction = direction
        self._size = len(self._tiles)

    @classmethod
    def create_from_pos(cls, color: tuple, direction: Dir, line:int, column: int, size: int) -> Snake:  # noqa: D102, E501, F821
        """Creates a snake from the given position."""  # noqa: D401
        tiles = [Tile(line=line, column=column+p, color=color) for p in range(size)]
        return Snake(tiles, direction = direction)

    @property
    def dir(self) -> Dir:  # noqa: ANN201, D102
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir) -> None:  # noqa: ANN001
        self._direction = new_direction

    def __len__(self) -> int:  # noqa: D105
        return len(self._tiles)

    def __contains__(self, cell: list) -> bool:
        """Cell : cell of the checkerboard [headtop, headleft] wich are the numbers of the lines/columns."""
        return cell in self._snake 

    def move(self) -> None:  # noqa: D102
        """Move the snake."""
        #add a new head
        self._tiles.insert(0, self._tiles[0] + self._direction)
        self._tiles.pop()

        #notify observers
        for obs in self.observers:
            obs.notify_object_moved(self)

        #shrink the tail
        if self._size < len(self._tiles):
            self._tiles = self._tiles[:self._size]

    def notify_collision(self, obj: GameObject) -> None:  # noqa: D102
        if isinstance(obj, Fruit):
            self._size += 1
            for o in self._observers:
                o.notify_object_eaten(obj)

    @property
    def tiles(self) -> Iterator[Tile]:  # noqa: ANN201, F821
        return iter(self._tiles)

class Fruit:
    """Creates a fruit."""

    def __init__(self, col: int, line: int, color: tuple) -> None:  # noqa: D107
        self._tiles = [Tile(line=line, column=col, color=color)]
        self._line = line
        self._col = col
        self._color = color

    @property
    def col(self) -> int:
        return self._col
    
    @property
    def line(self) -> int:
        return self._line

    @property
    def tiles(self) ->  Iterator[Tile]:  # noqa: ANN201, D102
        return iter(self._tiles)

def snake() -> None:

    args = argu()
    #initialisations : valeurs
    flag = True
    DEFAULT_STARTING_SNAKE = [(10,7),(10,6),(10,5)]
    DEFAULT_DIRECTION = Dir.LEFT

    LINES = args.height//args.square #nb de lignes
    COL = args.width//args.square #nb de colonnes

    #initialisations : objets  # noqa: ERA001
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode( (args.width, args.height) )

    checkerboard = Checkerboard(nb_lines = LINES, nb_col = COL, color1 = BLACK, color2 = WHITE)
    snake = Snake(tiles = DEFAULT_STARTING_SNAKE, direction = DEFAULT_DIRECTION)
    fruit = Fruit(col=3, line = 3, color=RED)
    board = Board(screen = screen, tile_size = DEFAULT_SQUARE, nb_lines = LINES, nb_cols = COL)

    board.add_object(checkerboard)
    board.add_object(snake)
    board.add_object(fruit)


    while flag:

        clock.tick(5)

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

    pygame.quit()