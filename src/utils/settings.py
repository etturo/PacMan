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
    MODE_TO_GAME_OVER = pygame.USEREVENT + 4
    MODE_TO_SETTINGS = pygame.USEREVENT + 5

    EXIT = pygame.USEREVENT + 6

    RESET_POSITIONS = pygame.USEREVENT + 7

    TOGGLE_FREEZE = pygame.USEREVENT + 8
    TOGGLE_DOUBLE_SPEED = pygame.USEREVENT + 9
    ADD_A_LIFE = pygame.USEREVENT + 10
    SUB_A_LIFE = pygame.USEREVENT + 11
    TOGGLE_INVINCIBILITY = pygame.USEREVENT + 12

    TOGGLE_FULLSCREEN = pygame.USEREVENT + 13
    ADD_10_FPS = pygame.USEREVENT + 14
    SUB_10_FPS = pygame.USEREVENT + 15
    TOGGLE_CRT_EFFECT = pygame.USEREVENT + 16
    TOGGLE_FLICKER_EFFECT = pygame.USEREVENT + 17
    TOGGLE_GLOW_EFFECT = pygame.USEREVENT + 18
    TOGGLE_GLITCH_EFFECT = pygame.USEREVENT + 19
    TOGGLE_ROLLING_EFFECT = pygame.USEREVENT + 20

    @staticmethod
    def post(mode: 'GameEvent') -> None:
        pygame.event.post(pygame.event.Event(mode))
