import abc  # noqa: D100
import typing

from .observer import Observer
from .subject import Subject
from .tile import Tile


class GameObject(Subject, Observer):  # noqa: D101

    def __init__(self: Any) -> None:  # noqa: D107
        super().__init__()

    def __contains__(self, obj: object) -> bool:  # noqa: D105
        if isinstance(obj, GameObject):
            return any(t in obj.tiles for t in self.tiles)
        return False

    @property
    @abc.abstractmethod
    def tiles(self) -> typing.Iterator[Tile]:  # noqa: D102
        raise NotImplementedError

    @property
    def backgroung(self) -> bool:  # noqa: D102
        return False #by default, GameObject isn't a background
