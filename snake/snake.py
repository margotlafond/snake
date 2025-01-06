from collections.abc import Iterator


class Snake(GameObject):
    """Snake class controled by the player."""

    def __init__(self, tiles: list[Tile], direction: Dir, gameover_on_exit: bool) -> None:  # noqa: D107
        super().__init__()
        self._tiles = tiles #list of the tiles that constitute the snake, head first
        self._direction = direction
        self._size = len(self._tiles)
        self._gameover_on_exit = gameover_on_exit

    @classmethod
    def create_from_pos(cls, colorbody: tuple or str, colorhead: tuple or str, direction: Dir, line:int, column: int, size: int) -> Snake:  # noqa: ARG003, D102, E501, F821
        """Creates a snake from the given position."""  # noqa: D401
        tiles = [Tile(line=line, column=column, color=colorhead)]
        for p in range(1, size):
            tiles.append(Tile(line=line, column=column+p, color=colorbody))
        return Snake(tiles, direction = direction)

    @property
    def dir(self) -> Dir:  # noqa: ANN201, D102
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir) -> None:  # noqa: ANN001
        self._direction = new_direction

    def notify_out_of_board(self) -> None:
        """Snake has exited the board."""
        if self._gameover_on_exit:
            raise GameOver

    def __len__(self) -> int:  # noqa: D105
        return len(self._tiles)
    
    #def __contains__(self, cell: list) -> bool:
        """Cell : cell of the checkerboard [headtop, headleft] wich are the numbers of the lines/columns."""
        #return cell in self._snake 

    def move(self) -> None:  # noqa: D102
        """Move the snake."""
        #add a new head
        new_head = self._tiles[0] + self._direction
        if new_head in self._tiles:
            raise GameOver
        self._tiles.insert(0, new_head)
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
