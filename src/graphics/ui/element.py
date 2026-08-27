import pygame

from abc import ABC, abstractmethod

from src.graphics.ui.drawable import Drawable
from src.graphics.graphical_utils.sprite_sheet import SpriteSheet, SpriteType
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.ui.text import Text

from src.utils.settings import Settings


class Element(Drawable):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: int
    ):
        super().__init__(position, sprite_sheet, anchor="topleft")

        self._surface = pygame.Surface((size, size))
        result = pygame.transform.scale(sprite_sheet[sprite_type], (size, size))
        self._surface.blit(result, (0, 0))


class LiveElement(Element, ABC):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: int
    ):
        super().__init__(
            position,
            sprite_sheet,
            sprite_type,
            size
            )

        self._surface = pygame.Surface((size, size))
        result = pygame.transform.scale(sprite_sheet[sprite_type], (size, size))
        self._surface.blit(result, (0, 0))

    @abstractmethod
    def update(self) -> None:
        pass


class Lives(LiveElement):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: int,
        initial_lives: int = 3
    ):
        super().__init__(position, sprite_sheet, sprite_type, size)
        self.__lives = initial_lives
        self.__size = size
        self.__text_size = size / 1.3
        self._surface = pygame.Surface(((size * 8), size))
        self.__sprite_sheet = sprite_sheet
        self.__sprite = pygame.transform.scale(sprite_sheet[sprite_type], (size, size))

    def update(self, current_lives: int) -> None:
        self.__lives = current_lives

        if self.__lives > 3:
            for i in range(3):
                self._surface.blit(self.__sprite, (i * self.__size, 0))

            text = Text(
                f" x{self.__lives}",
                (3 * self.__size, 1),
                self.__sprite_sheet,
                self.__text_size,
                anchor='topleft'
                )

            text.render(self._surface)

        else:
            for i in range(self.__lives):
                self._surface.blit(self.__sprite, (i * self.__size, 0))


class Points(LiveElement):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        size: int,
        initial_points: int = 3
        ):
        super().__init__(
            position,
            sprite_sheet,
            SpriteType.EMPTY_WALL,
            size
            )
        self.__points = initial_points
        self.__size = size
        self.__sprite_sheet = sprite_sheet
        formatted_points = str(self.__points).center(10)
        self.__text = Text(
            f"high score\n{formatted_points}",
            (0, 0),
            self.__sprite_sheet,
            self.__size,
            anchor='topleft'
            )

        self._surface = pygame.Surface(self.__text.getSize())

    def update(self, points: int) -> None:
        self.__points = points

        self.__text.render(self._surface)
