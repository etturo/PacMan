import pygame

from src.graphics.ui.drawable import Drawable
from src.graphics.graphical_utils.sprite_sheet import SpriteSheet, SpriteType


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
