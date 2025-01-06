import pygame  # noqa: D100

from .fruit import Fruit
from .game_object import GameObject
from .observer import Observer
from .subject import Subject


class Board(Subject, Observer):  # noqa: D101 #subject and observer bc prévient des collisions

    def __init__(self: Any, screen: pygame.Surface, tile_size: Any, nb_lines: int, nb_cols: int) -> None:  # noqa: ANN401, D107
        super().__init__()
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
        for o in self._objects:
            if o != obj and not(o.background) and o in obj:
                return o
        return None

    def notify_object_moved(self, obj: "GameObject") -> None:
        """Collision detection."""
        o = self.detect_collision(obj)
        if not o is None:
            obj.notify_collision(o)
        for tile in obj.tiles:
            if not (0 <= tile.x < self._nb_cols and
                    0 <= tile.y < self._nb_lines):
                obj.notify_out_of_board(width = self._nb_cols,
                                        height = self._nb_lines)

    def notify_object_eaten(self, obj: "GameObject") -> None:  # noqa: D102
        if isinstance(obj, Fruit):
            self.remove_object(obj)
            self.create_fruit()