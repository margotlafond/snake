from collections.abc import Iterator

from .game_object import GameObject
from .tile import Tile

class Fruit(GameObject):
    """Creates a fruit."""

    def __init__(self, col: int, line: int, color: tuple) -> None:  # noqa: D107
        super().__init__()
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

    @property
    def background(self) -> bool:  # noqa: D102
        return False
