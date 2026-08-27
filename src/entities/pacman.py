import pygame

from src.entities.entity import Entity, Direction

from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.ui_utils import SpriteType
from src.graphics.graphical_utils.sprite_sheet import SpriteSheet

from src.world.maze import Maze


class Pacman(Entity):
    def __init__(
        self,
        initial_position: tuple[float, float],
        size: int,
        speed: float,
        initial_lives: int = 3
        ) -> None:
        super().__init__(initial_position, size, speed)

        scale = SpriteSheet.scaleSprite

        self.__sheet = SpriteLibrary['yellow']

        self.__lives = initial_lives

        self.__sprite_full = scale(self.__sheet[SpriteType.PACMAN_FULL], size)
        self.__sprite_animation_up = [
            scale(self.__sheet[SpriteType.PACMAN_UP_1], size),
            scale(self.__sheet[SpriteType.PACMAN_UP_2], size),
            self.__sprite_full,
            scale(self.__sheet[SpriteType.PACMAN_UP_2], size),
        ]
        self.__sprite_animation_down = [
            scale(self.__sheet[SpriteType.PACMAN_DOWN_1], size),
            scale(self.__sheet[SpriteType.PACMAN_DOWN_2], size),
            self.__sprite_full,
            scale(self.__sheet[SpriteType.PACMAN_DOWN_2], size),
        ]
        self.__sprite_animation_left = [
            scale(self.__sheet[SpriteType.PACMAN_LEFT_1], size),
            scale(self.__sheet[SpriteType.PACMAN_LEFT_2], size),
            self.__sprite_full,
            scale(self.__sheet[SpriteType.PACMAN_LEFT_2], size)
        ]
        self.__sprite_animation_right = [
            scale(self.__sheet[SpriteType.PACMAN_RIGHT_1], size),
            scale(self.__sheet[SpriteType.PACMAN_RIGHT_2], size),
            self.__sprite_full,
            scale(self.__sheet[SpriteType.PACMAN_RIGHT_2], size)
        ]

        self.__death_animation = [
            scale(self.__sheet[SpriteType.PACMAN_DEATH_1], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_2], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_3], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_4], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_5], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_6], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_7], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_8], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_9], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_10], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_11], size),
            scale(self.__sheet[SpriteType.PACMAN_DEATH_12], size),
        ]

        self._surface = self.__sprite_full
        self._direction = Direction.STILL
        self.__animation_timer = 0
        self.__animation_delay = 0.1
        self.__frame_index = 0

    def update(self, dt: float) -> None:
        super().update(dt)

        self.__animation_timer += dt
        if self.__animation_timer >= self.__animation_delay:
            self.__animation_timer = 0.0
            self.__frame_index = (self.__frame_index + 1) % len(self.__sprite_animation_down)

    def takeDamage(self) -> None:
        self.__lives -= 1
        if self.lives <= 0:
            self._is_alive = False

    def getLives(self) -> None:
        return self.__lives

    def render(self,
               screen: pygame.Surface,
               screen_pos: tuple[float, float],
               dt: float,
               ) -> None:
        if self._current_direction == Direction.NORTH:
            self._surface = self.__sprite_animation_up[self.__frame_index]
        elif self._current_direction == Direction.SOUTH:
            self._surface = self.__sprite_animation_down[self.__frame_index]
        elif self._current_direction == Direction.WEST:
            self._surface = self.__sprite_animation_left[self.__frame_index]
        elif self._current_direction == Direction.EAST:
            self._surface = self.__sprite_animation_right[self.__frame_index]
        super().render(screen, screen_pos, dt)

