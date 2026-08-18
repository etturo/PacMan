import pygame

from typing import Callable

from src.graphics.sprite_sheet import SpriteSheet, SpriteType
from src.graphics.graphical_utils.sprite_font import SpriteFont

class Button:
    def __init__(self,
                 x: int,
                 y: int,
                 text: str,
                 sprite_sheet: SpriteSheet,
                 on_click: Callable[[], None],
                 ) -> None:
        self.__sheet: SpriteSheet = sprite_sheet
        self.__text = text
        self.__on_click = on_click
        self.__is_hovered = False
        self.__font = SpriteFont(sprite_sheet)
        # Offset in pixel
        self.__offset = 5
        self.__sprite_size = self.__font.getSize()
        self.__surface: pygame.Surface

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.__is_hovered = self.__rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.__is_hovered:
                self.__on_click()

    def render(self, screen: pygame.Surface) -> None:
        self._create_textbox()

        screen.blit(self.__surface)

    def _create_textbox(self) -> None:
        x_padding: int = 10
        y_padding: int = 10

        box_lenght, box_height = self._calculate_text_size(
            self.__text,
            self.__sprite_size,
            self.__offset,
            self.__font.CHAR_MAPPING
            )

        border_width = max(1, box_lenght - self.__sprite_size)
        border_height = max(1, box_height - self.__sprite_size * 2)

        horizontal_sprites = pygame.transform.scale(
            self.__sheet[SpriteType.HORIZONTAL_EDGE],
            (border_width, self.__sprite_size * 2)
        )
        vertical_sprites = pygame.transform.scale(
            self.__sheet[SpriteType.VERTICAL_EDGE],
            (self.__sprite_size, border_height)
        )

        self.__surface = pygame.Surface((box_lenght, box_height))
        self.__surface.blit(horizontal_sprites, (0, self.__sprite_size))

    #TODO FIX IT
    @staticmethod
    def _calculate_text_size(text: str,
                             sprite_size: int,
                             offset: int,
                             CHAR_MAPPING: dict[str, SpriteType]
                             ) -> tuple[int, int]:
        if not text:
            return (sprite_size * 2, sprite_size * 2)

        text_lines = text.split("\n") or [""]
        max_line_length = 0

        for line in text_lines:
            visible_chars = sum(
                1 for char in line if char in CHAR_MAPPING
            )
            max_line_length = max(max_line_length, visible_chars)

        box_width = max(1, max_line_length) * (sprite_size + offset)
        box_height = max(1, len(text_lines)) * (sprite_size + offset)

        box_width += sprite_size * 2
        box_height += sprite_size * 2

        return (box_width, box_height)
