import pygame

from src.entities.entity import Entity

from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.ui_utils import SpriteType


class Pacgum(Entity):
    def __init__(
            self,
            pos: tuple[int, int],
            size: float,
            points: int
    ) -> None:
        super().__init__(
            pos,
            size,
            0
        )
        sprite_sheet = SpriteLibrary.get('blue')
        self._surface = SpriteSheet.scaleSprite(
            sprite_sheet[SpriteType.PACGUM],
            size
        )


class SuperPacgum(Entity):
    def __init__(
        self,
        pos: tuple[int, int],
        size: float,
        points: int
    ) -> None:
        super().__init__(
            pos,
            size,
            0
        )
        sprite_sheet = SpriteLibrary.get('blue')
        scale = SpriteSheet.scaleSprite
        self.__sprite = scale(sprite_sheet[SpriteType.SUPER_PACGUMS], size)
        self.__animation = [
            self.__sprite,
            scale(sprite_sheet[SpriteType.EMPTY_WALL], size)
        ]
        self._surface = self.__sprite
        self.__animation_timer = 0.0
        self.__animation_delay = 0.1
        self.__frame_index = 0

    def update(self, dt: float) -> None:
        super().update(dt)

        self.__animation_timer += dt
        if self.__animation_timer >= self.__animation_delay:
            self.__animation_timer = 0.0
            self.__frame_index = \
                (self.__frame_index + 1) % len(self.__animation)

    def render(
            self,
            screen: pygame.Surface,
            screen_pos: tuple[float, float],
            dt: float,
            ) -> None:
        self._surface = self.__animation[self.__frame_index]
        super().render(screen, screen_pos, dt)
