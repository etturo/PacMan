"""Define the models module."""

from pydantic import BaseModel, Field, model_validator


class ParsingError(ValueError):
    """Represent the ParsingError component."""

    ...


class LevelConfig(BaseModel):
    """Represent the LevelConfig component."""

    width: int
    height: int


class LevelDifficulty(BaseModel):
    """Represent the LevelDifficulty component."""

    pacman_speed: int
    pacman_fright_speed: int
    ghost_speed: int
    ghost_fright_speed: int
    fright_time: float
    scatter_chase: list[float]


class GameSettings(BaseModel):
    """Represent the GameSettings component."""

    highscore_filename: str = Field(default="scores.json")
    levels: list[LevelConfig] = Field(
        default=[
            LevelConfig(width=5, height=5),
            LevelConfig(width=15, height=15),
            LevelConfig(width=28, height=36)
        ]
    )
    lives: int = Field(default=3, gt=0, le=99)
    pacgums: int = Field(default=42, ge=0)
    points_per_pacgum: int = Field(default=10, gt=0)
    points_per_super_pacgum: int = Field(default=50, gt=0)
    points_per_ghost: int = 200
    seed: int = Field(default=42, ge=0)
    level_max_time: int = Field(default=300, gt=0)
    max_level: int = Field(default=256, gt=0)
    difficulty: list[LevelDifficulty] = Field(
        default=[
            LevelDifficulty(
                pacman_speed=80,
                pacman_fright_speed=90,
                ghost_speed=75,
                ghost_fright_speed=50,
                fright_time=6,
                scatter_chase=[7, 20, 7, 20, 5, 20, 5]
            )
        ],
        min_length=1
    )
    # CUSTOM
    ghost_freezed: bool = False
    double_speeded: bool = False
    invincibility: bool = False
    fps: int = 60
    crt: bool = True
    glitch: bool = True
    glow: bool = True
    rolling: bool = True

    @model_validator(mode="after")
    def validate_scores(self) -> 'GameSettings':
        """Perform the validate_scores operation."""
        if self.points_per_super_pacgum <= self.points_per_pacgum:
            raise ValueError(
                "points_per_super_pacgums "
                "must be greater than points_per_pacgums"
            )
        return self
