import pygame

from abc import ABC

from src.utils.sprite_sheet import SpriteSheet


class Drawable(ABC):
    def __init__(
            self,
            position: tuple[int, int],
            sprite_sheet: SpriteSheet
        ) -> None:
        self._position = position
        self._sheet = sprite_sheet
        self._surface: pygame.Surface

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self._position)
