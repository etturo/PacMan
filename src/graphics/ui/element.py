import pygame
import json
from typing import cast, Any

from abc import ABC, abstractmethod

from src.graphics.ui.drawable import Drawable
from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.ui_utils import SpriteType
from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.ui.text import Text


class Element(Drawable):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: float,
        anchor: str = "topleft"
    ):
        super().__init__(position, sprite_sheet, anchor)

        self._surface = pygame.Surface((size, size))
        result = pygame.transform.scale(
            sprite_sheet[sprite_type],
            (size, size)
            )
        self._surface.blit(result, (0, 0))


class LiveElement(Element, ABC):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: float,
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
    def update(self, value: int = 0) -> None:
        pass

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pass


class Lives(LiveElement):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: float,
        initial_lives: int = 3
    ):
        super().__init__(position, sprite_sheet, sprite_type, size)
        self.__lives = -1
        self.__size = size
        self.__text_size = size / 1.3
        self._surface = pygame.Surface((size * 3, size * 2), pygame.SRCALPHA)
        self.__sprite_sheet = sprite_sheet
        self.__sprite = pygame.transform.scale(
            sprite_sheet[sprite_type],
            (size, size)
            )

    def update(self, value: int = 0) -> None:
        if self.__lives == value:
            return

        self.__lives = value
        self._surface.fill((0, 0, 0, 0))

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

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        return


class Points(LiveElement):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        size: float,
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

        self._surface = pygame.Surface(self.__text.getSize(), pygame.SRCALPHA)

    def update(self, value: int = 0) -> None:
        self.__points = value
        self._surface.fill((0, 0, 0, 0))

        formatted_points = str(self.__points).center(5)
        self.__str = f"{'score'.center(5)}\n{formatted_points}"
        self.__text = Text(
            self.__str,
            (0, 0),
            self.__sprite_sheet,
            self.__size,
            anchor='topleft'
            )

        self.__text.render(self._surface)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        return


class TextInput(LiveElement):
    def __init__(
        self,
        position: tuple[float, float],
        sprite_sheet: SpriteSheet,
        size: float,
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
        self._surface = pygame.Surface(
            (size * max_length, size * 1.5),
            pygame.SRCALPHA
            )
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
                    if (len(self.__text_buffer) < self.__max_length
                            and char.isalnum()):
                        self.__text_buffer += char
                        self._render_text()
                elif event.key == pygame.K_RETURN:
                    if len(self.__text_buffer) > 0:
                        self.__is_finished = True

    def get_text(self) -> str:
        return self.__text_buffer

    def isFinished(self) -> bool:
        return self.__is_finished

    def update(self, value: int = 0) -> None:
        return


class Leadboard(Element):
    def __init__(
        self,
        position: tuple[float, float],
        width: float,
        height: float,
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: float,
        anchor: str = "topleft"
    ):
        super().__init__(position, sprite_sheet, sprite_type, size, anchor)
        self.__font: SpriteFont = SpriteFont(sprite_sheet, size)
        self.__offset = 5
        self.__width = width
        self.__height = height
        self.__sprite_size = size

        self._create_textbox()

        title = Text(
            "LEADBOARD",
            (self._surface.get_width() / 2, size),
            SpriteLibrary.get('white'),
            size / 1.5,
            anchor="mid top"
        )
        title.render(self._surface)

        leadboard: list[list[Any]] = []
        try:
            with open("data/leadboard/scores.json", "r") as f:
                leadboard = cast(list[list[Any]], json.load(f))
        except (json.decoder.JSONDecodeError,
                FileNotFoundError,
                FileExistsError):
            print("WARNING! Failed to load the leadboard file, "
                  "check json correctness.")

        leadboard.sort(key=lambda x: int(x[1]), reverse=True)

        for i in range(min(10, len(leadboard))):
            player = leadboard[i][0]
            score = leadboard[i][1]
            text = Text(
                f"{i + 1}.{player}-{score}",
                (self._surface.get_width() / 15, size * i + size * 2.5),
                SpriteLibrary.get('white'),
                size / 3,
                anchor="topleft"
            )
            text.render(self._surface)

    def _create_textbox(self) -> None:
        text_size = self.__sprite_size
        box_sprite_size = text_size / 2

        box_width = self.__width
        box_height = self.__height

        v_border_length = max(1, box_height - (box_sprite_size * 2))
        h_border_length = max(1, box_width - (box_sprite_size * 2))

        horizontal_sprites = pygame.transform.scale(
            self._sheet[SpriteType.HORIZONTAL_EDGE],
            (h_border_length, box_sprite_size)
        )
        vertical_sprites = pygame.transform.scale(
            self._sheet[SpriteType.VERTICAL_EDGE],
            (box_sprite_size, v_border_length)
        )
        top_left_sprite = pygame.transform.scale(
            self._sheet[SpriteType.TOP_LEFT],
            (box_sprite_size, box_sprite_size)
        )
        top_right_sprite = pygame.transform.scale(
            self._sheet[SpriteType.TOP_RIGHT],
            (box_sprite_size, box_sprite_size)
        )
        bottom_left_sprite = pygame.transform.scale(
            self._sheet[SpriteType.BOTTOM_LEFT],
            (box_sprite_size, box_sprite_size)
        )
        bottom_right_sprite = pygame.transform.scale(
            self._sheet[SpriteType.BOTTOM_RIGHT],
            (box_sprite_size, box_sprite_size)
        )

        self._surface = pygame.Surface((box_width, box_height))
        self.__secondary_surface = pygame.Surface((box_width, box_height))
        self.__rect = self._get_rect()

        # top horizontal border
        self._surface.blit(
            horizontal_sprites,
            (box_sprite_size, 0))

        # bottom horizontal border
        self._surface.blit(
            horizontal_sprites,
            (box_sprite_size, box_height - box_sprite_size))

        # left vertical border
        self._surface.blit(
            vertical_sprites,
            (0, box_sprite_size))

        # right vertical blit
        self._surface.blit(
            vertical_sprites,
            (box_width - box_sprite_size, box_sprite_size))

        self._surface.blit(
            top_left_sprite,
            (0, 0))
        self._surface.blit(
            top_right_sprite,
            (box_width - box_sprite_size, 0))
        self._surface.blit(
            bottom_left_sprite,
            (0, box_height - box_sprite_size))
        self._surface.blit(
            bottom_right_sprite,
            (box_width - box_sprite_size, box_height - box_sprite_size))


class Box(Element):
    def __init__(
        self,
        position: tuple[float, float],
        width: float,
        height: float,
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: float,
        title: str = "",
        anchor: str = "topleft",
    ):
        super().__init__(position, sprite_sheet, sprite_type, size, anchor)
        self.__offset = 5
        self.__width = width
        self.__height = height
        self.__sprite_size = size

        self._surface = pygame.Surface(
            (self.__width, self.__height), pygame.SRCALPHA
        )
        self.__title = title

        self._create_textbox()

        title_box = Text(
            self.__title,
            (self._surface.get_width() / 2, size),
            SpriteLibrary.get('white'),
            size / 1.5,
            anchor="mid top"
        )
        title_box.render(self._surface)

    def _create_textbox(self) -> None:
        text_size = self.__sprite_size
        box_sprite_size = text_size / 2

        box_width = self.__width
        box_height = self.__height

        v_border_length = max(1, box_height - (box_sprite_size * 2))
        h_border_length = max(1, box_width - (box_sprite_size * 2))

        horizontal_sprites = pygame.transform.scale(
            self._sheet[SpriteType.HORIZONTAL_EDGE],
            (h_border_length, box_sprite_size)
        )
        vertical_sprites = pygame.transform.scale(
            self._sheet[SpriteType.VERTICAL_EDGE],
            (box_sprite_size, v_border_length)
        )
        top_left_sprite = pygame.transform.scale(
            self._sheet[SpriteType.TOP_LEFT],
            (box_sprite_size, box_sprite_size)
        )
        top_right_sprite = pygame.transform.scale(
            self._sheet[SpriteType.TOP_RIGHT],
            (box_sprite_size, box_sprite_size)
        )
        bottom_left_sprite = pygame.transform.scale(
            self._sheet[SpriteType.BOTTOM_LEFT],
            (box_sprite_size, box_sprite_size)
        )
        bottom_right_sprite = pygame.transform.scale(
            self._sheet[SpriteType.BOTTOM_RIGHT],
            (box_sprite_size, box_sprite_size)
        )

        self._surface = pygame.Surface((box_width, box_height))
        self.__secondary_surface = pygame.Surface((box_width, box_height))
        self.__rect = self._get_rect()

        # top horizontal border
        self._surface.blit(
            horizontal_sprites,
            (box_sprite_size, 0))

        # bottom horizontal border
        self._surface.blit(
            horizontal_sprites,
            (box_sprite_size, box_height - box_sprite_size))

        # left vertical border
        self._surface.blit(
            vertical_sprites,
            (0, box_sprite_size))

        # right vertical blit
        self._surface.blit(
            vertical_sprites,
            (box_width - box_sprite_size, box_sprite_size))

        self._surface.blit(
            top_left_sprite,
            (0, 0))
        self._surface.blit(
            top_right_sprite,
            (box_width - box_sprite_size, 0))
        self._surface.blit(
            bottom_left_sprite,
            (0, box_height - box_sprite_size))
        self._surface.blit(
            bottom_right_sprite,
            (box_width - box_sprite_size, box_height - box_sprite_size))


class Timer(LiveElement):
    def __init__(
        self,
        position: tuple[float, float],
        width: float,
        height: float,
        sprite_sheet: SpriteSheet,
        sprite_type: SpriteType,
        size: float,
        time: float,
        max_time_seconds: int,
        anchor: str = "topleft",
    ):
        super().__init__(position, sprite_sheet, sprite_type, size, anchor)
        self.__offset = 5
        self.__width = width
        self.__height = height
        self.__sprite_size = size
        self._surface = pygame.Surface(
            (self.__width, self.__height), pygame.SRCALPHA
        )

        self.__max_time_seconds = max_time_seconds

        self.__is_going = False

        self.__font = SpriteFont(sprite_sheet, size)


        self.__start_time: float = time
        self.__time_elapsed: float = time
        self.__time_to_show: float = time

        
        minutes = int(self.__time_elapsed // 60)
        seconds = int(self.__time_elapsed % 60)
        minutes_total = int(self.__max_time_seconds // 60)
        seconds_total = int(self.__max_time_seconds % 60)
        minutes_result = minutes_total - minutes
        seconds_result = seconds_total - seconds
        first_line = "time".center(5)
        second_line = "left".center(5)
        third_line = "-----"
        fourth_line = f"{minutes_result:02d}:{seconds_result:02d}".center(5)
        self.__text = \
            f"{first_line}\n{second_line}\n{third_line}\n{fourth_line}"
        self._surface.fill((0, 0, 0))
        self.__font.render(self._surface, (0, 0), self.__text)

    def update(self, dt: float) -> None:
        if self.__is_going:
            self.__time_elapsed += dt
            self.__time_to_show = self.__time_elapsed - self.__start_time
            minutes = int(self.__time_elapsed // 60)
            seconds = int(self.__time_elapsed % 60)
            minutes_total = int(self.__max_time_seconds // 60)
            seconds_total = int(self.__max_time_seconds % 60)
            minutes_result = minutes_total - minutes
            seconds_result = seconds_total - seconds
            first_line = "time".center(5)
            second_line = "left".center(5)
            third_line = "-----"
            fourth_line = f"{minutes_result:02d}:{seconds_result:02d}".center(5)
            self.__text = \
                f"{first_line}\n{second_line}\n{third_line}\n{fourth_line}"
        self._surface.fill((0, 0, 0))
        self.__font.render(self._surface, (0, 0), self.__text)

    def start(self) -> None:
        self.__is_going = True

    def pause(self) -> None:
        self.__is_going = False

    def getIsGoing(self) -> bool:
        return self.__is_going

