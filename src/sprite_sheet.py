from enum import Enum

import pygame

from src.settings import DEFAULT_SCALE

SPRITE_LENGHT = 8
SPRITE_WIDTH = 8

NUMBER_ZERO_COORDINATES = (1, 19)
NUMBER_ONE_COORDINATES = (10, 19)
NUMBER_TWO_COORDINATES = (19, 19)
NUMBER_THREE_COORDINATES = (28, 19)
NUMBER_FOUR_COORDINATES = (37, 19)
NUMBER_FIVE_COORDINATES = (46, 19)
NUMBER_SIX_COORDINATES = (55, 19)
NUMBER_SEVEN_COORDINATES = (64, 19)
NUMBER_EIGHT_COORDINATES = (73, 19)
NUMBER_NINE_COORDINATES = (82, 19)


class SpriteType(Enum):
    ZERO = "zero"
    ONE = "one"
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"
    SIX = "six"
    SEVEN = "seven"
    EIGHT = "eight"
    NINE = "nine"


class SpriteSheet:
    def __init__(self, filename: str,
                 color_key: tuple[int, int, int] = (255, 0, 255)
                 ) -> None:
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.sheet.set_colorkey(color_key)
        self.data: dict[SpriteType, pygame.Surface] = {}

        self._load_numbers()

    def __getitem__(self, key: SpriteType) -> pygame.Surface:
        return self.data[key]

    def _extract_and_scale(self,
                           coordinates: tuple[int, int]
                           ) -> pygame.Surface:
        rect = pygame.Rect(*coordinates, SPRITE_WIDTH, SPRITE_LENGHT)
        raw_surface = self.sheet.subsurface(rect)

        return pygame.transform.scale_by(raw_surface, DEFAULT_SCALE)

    def _load_numbers(self) -> None:
        self.data[SpriteType.ZERO] = self._extract_and_scale(
            NUMBER_ZERO_COORDINATES
        )
        self.data[SpriteType.ONE] = self._extract_and_scale(
            NUMBER_ONE_COORDINATES
        )
        self.data[SpriteType.TWO] = self._extract_and_scale(
            NUMBER_TWO_COORDINATES
        )
        self.data[SpriteType.THREE] = self._extract_and_scale(
            NUMBER_THREE_COORDINATES
        )
        self.data[SpriteType.FOUR] = self._extract_and_scale(
            NUMBER_FOUR_COORDINATES
        )
        self.data[SpriteType.FIVE] = self._extract_and_scale(
            NUMBER_FIVE_COORDINATES
        )
        self.data[SpriteType.SIX] = self._extract_and_scale(
            NUMBER_SIX_COORDINATES
        )
        self.data[SpriteType.SEVEN] = self._extract_and_scale(
            NUMBER_SEVEN_COORDINATES
        )
        self.data[SpriteType.EIGHT] = self._extract_and_scale(
            NUMBER_EIGHT_COORDINATES
        )
        self.data[SpriteType.NINE] = self._extract_and_scale(
            NUMBER_NINE_COORDINATES
        )
