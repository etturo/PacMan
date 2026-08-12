from pydantic import BaseModel


class ParsingError(BaseException):
    def __init__(self) -> None:
        ...


class LevelConfig(BaseModel):
    width: int
    height: int


class BaseSettings(BaseModel):
    highscore_filename: str = "config.json"
    levels: list[LevelConfig] = []
    lives: int = 3
    pacgums: int = 42
    points_per_pacgums: int = 10
    points_per_super_pacgums: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
