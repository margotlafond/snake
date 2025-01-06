

class Observer(abc.ABC):  # noqa: B024, D101

    def __init__(self) -> None:  # noqa: D107
        super().__init__()

    def notify_object_eaten(self, obj: "GameObject") -> None:  # noqa: B027, D102
        pass

    def notify_object_moved(self, obj: "GameObject") -> None:  # noqa: B027, D102
        pass

    def notify_collision(self, obj: "GameObject") -> None:  # noqa: B027, D102
        pass
