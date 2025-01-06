from .dir import Dir  # noqa: D100


class Tile:  # noqa: D101
    def __init__(self: Any, line: int, color: tuple, column: int) -> None:  # noqa: D107
        self._line = line
        self._color = color
        self._column = column

    @property
    def x(self) -> int:
        """The x coordinate (i.e.: column index) of the tile."""
        return self._column

    @property
    def y(self) -> int:
        """The y coordinate (i.e.: line index) of the tile."""
        return self._line

    def draw(self, screen: pygame.Surface, tile_size: int) -> None:
        tile = pygame.Rect(self._column*tile_size, self._line*tile_size, tile_size, tile_size)  # noqa: E501
        pygame.draw.rect(screen, self._color, tile)

    def __add__(self, other: Any) -> Tile:
        if not isinstance(other, Dir):
            msg = "The added element class is not Dir."
            raise ValueError(msg)  # noqa: TRY004
        return Tile(self._line + other.value[1], self._column + other.value[0], self._color)  # noqa: E501
