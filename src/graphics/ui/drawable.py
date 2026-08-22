import pygame

from abc import ABC

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.ui_utils import SpriteType, CHAR_MAPPING


class Drawable(ABC):
    def __init__(
            self,
            position: tuple[int, int],
            sprite_sheet: SpriteSheet,
            centered: bool = True
        ) -> None:
        self._position = position
        self._sheet = sprite_sheet

        self._centered = centered

        self._surface: pygame.Surface

    def render(self, surface: pygame.Surface) -> None:
        if self._centered:
            rect = self._surface.get_rect(center=self._position)
            surface.blit(self._surface, rect)
            return

        surface.blit(self._surface, self._position)

    @staticmethod
    def _calculate_text_size(
        text: str,
        sprite_size: int = 0,
        offset: int = 0,
        include_padding: bool = False,
    ) -> tuple[int, int]:

        if not text:
            if include_padding:
                return (sprite_size * 2, sprite_size * 2)
            return (sprite_size, sprite_size)

        text_lines = text.split("\n") or [text]
        max_line_length = 0

        for line in text_lines:
            visible_chars = sum(
                1 for char in line
                if char.upper() in CHAR_MAPPING
            )
            max_line_length = max(max_line_length, visible_chars)

        box_width = max(1, max_line_length) * (sprite_size + offset)
        box_height = max(1, len(text_lines)) * (sprite_size + offset)

        if include_padding:
            box_width += sprite_size * 2
            box_height += sprite_size * 2

        return (box_width, box_height)
