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
        size: int,
        anchor: str = "topleft"
    ):
        super().__init__(position, sprite_sheet, anchor)

        self._surface = pygame.Surface((size, size))
        result = pygame.transform.scale(sprite_sheet[sprite_type], (size, size))
        self._surface.blit(result, (0, 0))


class LiveElement(Element, ABC):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: int,
        anchor: str = "topleft"
    ):
        super().__init__(
            position,
            sprite_sheet,
            sprite_type,
            size,
            anchor
            )

    @abstractmethod
    def update(self) -> None:
        pass

    def handle_events(self, events) -> None:
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
        self.__lives = -1
        self.__size = size
        self.__text_size = size / 1.3
        self._surface = pygame.Surface((size * 3, size * 2))
        self.__sprite_sheet = sprite_sheet
        self.__sprite = pygame.transform.scale(sprite_sheet[sprite_type], (size, size))

    def update(self, current_lives: int) -> None:
        if self.__lives == current_lives:
            return

        self.__lives = current_lives

        self._surface.fill((0, 0, 0))

        if self.__lives > 3:
            for i in range(3):
                self._surface.blit(self.__sprite, (i * self.__size, 0))

            text = Text(
                f"x{self.__lives}",
                (0, self.__size),
                self.__sprite_sheet,
                self.__text_size / 1.5,
                anchor='topleft'
                )

            text.render(self._surface)

        else:
            for i in range(self.__lives):
                self._surface.blit(self.__sprite, (i * self.__size, 0))

    def handle_events(self, events):
        return


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
        formatted_points = str(self.__points).center(5)
        self.__str = f"{'score'.center(5)}\n{formatted_points}"
        self.__text = Text(
            self.__str,
            (0, 0),
            self.__sprite_sheet,
            self.__size,
            anchor='topleft'
            )

        self._surface = pygame.Surface(self.__text.getSize())

    def update(self, points: int) -> None:
        self.__points = points

        self._surface.fill((0, 0, 0, 0))

        formatted_points = str(self.__points).center(5)
        self.__str = f"{'score'.center(5)}\n{formatted_points}"
        self.__text = Text(
            self.__str,
            (0, 0),
            self.__sprite_sheet,
            self.__size / 1.2,
            anchor='topleft'
            )

        self.__text.render(self._surface)

    def handle_events(self, events):
        return


class TextInput(LiveElement):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        size: int,
        max_length: int = 10
    ):
        super().__init__(
            position,
            sprite_sheet,
            SpriteType.EMPTY_WALL,
            size,
            anchor="center"
        )
        self.__text_buffer = ""
        self.__size = size
        self.__max_length = max_length
        self.__sprite_sheet = sprite_sheet
        self._surface = pygame.Surface((size * max_length, size * 1.5), pygame.SRCALPHA)
        self._render_text()
        self.__is_finished = False

    def _render_text(self) -> None:
        self._surface.fill((0, 0, 0, 0))
        display_text = self.__text_buffer if self.__text_buffer else " "

        center_x = self._surface.get_width() / 2
        center_y = self._surface.get_height() / 2

        text_element = Text(
            display_text,
            (center_x, center_y),
            self.__sprite_sheet,
            self.__size,
            anchor='center'
        )

        text_element.render(self._surface)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.__text_buffer = self.__text_buffer[:-1]
                    self._render_text()
                elif event.key != pygame.K_RETURN:
                    char = event.unicode.lower()
                    if len(self.__text_buffer) < self.__max_length and char.isalnum():
                        self.__text_buffer += char
                        self._render_text()
                elif event.key == pygame.K_RETURN:
                    self.__is_finished = True

    def get_text(self) -> str:
        return self.__text_buffer

    def isFinished(self) -> bool:
        return self.__is_finished

    def update(self) -> None:
        return
