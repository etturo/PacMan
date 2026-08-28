import pygame

from enum import IntEnum


class Settings:
    DEFAULT_SCALE = 2.0

    # VIRTUAL_WINDOW_WIDTH = 640
    # VIRTUAL_WINDOW_HEIGHT = 360

    VIRTUAL_WINDOW_WIDTH = 1280
    VIRTUAL_WINDOW_HEIGHT = 720

    SMALL_SPRITE_LENGHT = 8
    SMALL_SPRITE_WIDTH = 8

    SPRITE_LENGHT = 16
    SPRITE_WIDTH = 16


class GameEvent(IntEnum):
    MODE_TO_STARTING = pygame.USEREVENT + 1
    MODE_TO_MENU = pygame.USEREVENT + 2
    MODE_TO_PLAYING = pygame.USEREVENT + 3
    EXIT = pygame.USEREVENT + 4
    RESET_POSITIONS = pygame.USEREVENT + 5

    @staticmethod
    def post(mode: 'GameEvent') -> None:
        pygame.event.post(pygame.event.Event(mode))
