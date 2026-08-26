from pydantic import BaseModel, Field, model_validator


class ParsingError(ValueError):
    ...


class LevelConfig(BaseModel):
    width: int
    height: int


class GameSettings(BaseModel):
    highscore_filename: str = Field(default="config.json")
    levels: list[LevelConfig]
    lives: int = Field(default=3, gt=0, le=99)
    pacgums: int = Field(default=42, ge=0)
    points_per_pacgums: int = Field(default=10, gt=0)
    points_per_super_pacgums: int = Field(default=50, gt=0)
    points_per_ghost: int = Field(default=200, gt=0)
    seed: int = Field(default=42, ge=0)
    level_max_time: int = Field(default=90, gt=0)

    @model_validator(mode="after")
    def validate_scores(self) -> 'BaseSettings':
        if self.points_per_super_pacgums <= self.points_per_pacgums:
            raise ValueError(
                "points_per_super_pacgums "
                "must be greater than points_per_pacgums"
            )
        return self
