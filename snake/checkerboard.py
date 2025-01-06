from __future__ import annotations  # noqa: D100

from .game_object import GameObject
from .tile import Tile


class Checkerboard(GameObject):  # noqa: D101
    def __init__(self, nb_lines: int, nb_col: int, color1: tuple, color2:tuple) -> None: # noqa: D107
        super().__init__()
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
