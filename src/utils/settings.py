from enum import Enum, auto


class Settings:
    DEFAULT_SCALE = 2.0

    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080

    SMALL_SPRITE_LENGHT = 8
    SMALL_SPRITE_WIDTH = 8

    SPRITE_LENGHT = 16
    SPRITE_WIDTH = 16


class GameMode(Enum):
    STARTING = auto()
    MAIN_MENU = auto()
    SETTINGS_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
