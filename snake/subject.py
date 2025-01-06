from .observer import Observer

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
