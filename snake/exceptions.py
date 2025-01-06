class SnakeException(Exception):  # noqa: D101, N818
    def __init__(self, message: str) -> None:  # noqa: D107
        super().__init__(message)

class SnakeError(SnakeException):  # noqa: D101
    def __init__(self, message: str) -> None:  # noqa: D107
        super().__init__(message)

class IntRangeError(SnakeError):  # noqa: D101
    def __init__(self, name: str, value: int, val_min: int, val_max: int) -> None:  # noqa: D107
        super().__init__(f"Value {value} of {name} is out of the allowed range [{val_min}, {val_max}].")  # noqa: E501

class ColorError(SnakeError):  # noqa: D101
    def __init__(self, color: str, name: str) -> None:  # noqa: D107
        super().__init__(f"Wrong color {color} for argument {name}.")

class GameOver(SnakeException):  # noqa: D101
    def __init__(self) -> None:
        super().__init__("GAME OVER")
