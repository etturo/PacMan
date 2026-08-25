import pygame

from enum import Enum, auto, IntEnum

class GameMode(Enum):
    STARTING = auto()
    MAIN_MENU = auto()
    SETTINGS_MENU = auto()
    SCORES_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

class Settings:
    DEFAULT_SCALE = 2.0

    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080

    SMALL_SPRITE_LENGHT = 8
    SMALL_SPRITE_WIDTH = 8

    SPRITE_LENGHT = 16
    SPRITE_WIDTH = 16

class GameEvent(IntEnum):
    MODE_TO_STARTING = pygame.USEREVENT + 1
    MODE_TO_MENU = pygame.USEREVENT + 2
    MODE_TO_PLAYING = pygame.USEREVENT + 3
    MODE_TO_SETTINGS = pygame.USEREVENT + 4
    MODE_TO_SCORES = pygame.USEREVENT + 5
    EXIT = pygame.USEREVENT + 6

    def post(mode: 'GameEvent') -> None:
        pygame.event.post(pygame.event.Event(mode))
