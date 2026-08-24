import pygame

from abc import ABC

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.ui_utils import SpriteType, CHAR_MAPPING


class Drawable(ABC):
    _VALID_ANCHORS = {
        "center",
        "topleft",
        "topright",
        "bottomleft",
        "bottomright",
        "midtop",
        "midbottom",
        "midleft",
        "midright",
    }

    def __init__(
            self,
            position: tuple[int, int],
            sprite_sheet: SpriteSheet,
            anchor: str = "center",
        ) -> None:
        self._position = position
        self._sheet = sprite_sheet

        self._anchor = self._normalize_anchor(anchor)
        self._surface: pygame.Surface

    @classmethod
    def _normalize_anchor(cls, anchor: str | None) -> str:
        if anchor is None:
            return "center"

        normalized = anchor.strip().lower().replace("-", "_")
        normalized = normalized.replace(" ", "_").replace('_', "")
        if normalized in cls._VALID_ANCHORS:
            return normalized
        print(f"WARINING: Unsupported anchor '{anchor}'.")

    def _get_rect(self) -> pygame.Rect:
        rect = self._surface.get_rect()

        if self._anchor == "center":
            rect.center = self._position
        elif self._anchor == "topleft":
            rect.topleft = self._position
        elif self._anchor == "topright":
            rect.topright = self._position
        elif self._anchor == "bottomleft":
            rect.bottomleft = self._position
        elif self._anchor == "bottomright":
            rect.bottomright = self._position
        elif self._anchor == "midtop":
            rect.midtop = self._position
        elif self._anchor == "midbottom":
            rect.midbottom = self._position
        elif self._anchor == "midleft":
            rect.midleft = self._position
        elif self._anchor == "midright":
            rect.midright = self._position
        else:
            raise ValueError(f"Unsupported anchor '{self._anchor}'.")

        return rect

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self._get_rect())

    @staticmethod
    def _calculate_text_size(
        text: str,
        sprite_size: int = 0,
        box_sprite_size: int = 0,
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
            box_width += box_sprite_size * 2
            box_height += box_sprite_size * 2

        return (box_width, box_height)
