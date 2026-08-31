import pygame

from typing import Callable
from enum import Enum, auto

from src.entities.entity import Entity

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.ui_utils import SpriteType

from src.world.maze import Maze, Direction

class GhostMode(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()


class Ghost(Entity):
    def __init__(
        self,
        init_pos: tuple[int, int],
        size: int,
        speed: float,
        sprite_sheet: SpriteSheet,
        # The strategy is a function prototyped like:
        # '''
        # def strategy(maze: Maze, ghost_pos: tuple[int, int], pacman_pos: tuple[int, int])
        # '''
        # and returns the Direction the ghost should take next turn
        strategy: Callable[[Maze, tuple[int, int], tuple[int, int]], Direction],
        ) -> None:

        #TOREMOVE
        speed = 0

        super().__init__(init_pos, size, speed)

        scale = SpriteSheet.scaleSprite

        self.__sheet = sprite_sheet
        self.__strategy = strategy
        self.__mode = GhostMode.CHASE

        frightened_sheet_1 = SpriteLibrary['melon']
        frightened_sheet_2 = SpriteLibrary['green']

        self.__sprite_animation_up = [
            scale(self.__sheet[SpriteType.GHOST_EYE_UP_1], size),
            scale(self.__sheet[SpriteType.GHOST_EYE_UP_2], size)
        ]
        self.__sprite_animation_down = [
            scale(self.__sheet[SpriteType.GHOST_EYE_DOWN_1], size),
            scale(self.__sheet[SpriteType.GHOST_EYE_DOWN_2], size),
        ]
        self.__sprite_animation_left = [
            scale(self.__sheet[SpriteType.GHOST_EYE_LEFT_1], size),
            scale(self.__sheet[SpriteType.GHOST_EYE_LEFT_2], size),
        ]
        self.__sprite_animation_right = [
            scale(self.__sheet[SpriteType.GHOST_EYE_RIGHT_1], size),
            scale(self.__sheet[SpriteType.GHOST_EYE_RIGHT_2], size),
        ]

        self.__frightened_animation = [
            scale(frightened_sheet_1[SpriteType.FRIGHTENED_GHOST_1], size),
            scale(frightened_sheet_1[SpriteType.FRIGHTENED_GHOST_2], size),
            scale(frightened_sheet_1[SpriteType.FRIGHTENED_GHOST_1], size),
            scale(frightened_sheet_1[SpriteType.FRIGHTENED_GHOST_2], size),
            scale(frightened_sheet_2[SpriteType.FRIGHTENED_GHOST_1], size),
            scale(frightened_sheet_2[SpriteType.FRIGHTENED_GHOST_2], size),
            scale(frightened_sheet_2[SpriteType.FRIGHTENED_GHOST_1], size),
            scale(frightened_sheet_2[SpriteType.FRIGHTENED_GHOST_2], size),
        ]

        self.__animation_timer = 0
        self.__animation_delay = 0.1
        self.__frame_index = 0
        self._surface = self.__frightened_animation[0]

    def getMode(self) -> GhostMode:
        return self.__mode

    def update(self, dt: float) -> None:
        super().update(dt)

        self.__animation_timer += dt
        if self.__animation_timer >= self.__animation_delay:
            self.__animation_timer = 0.0
            self.__frame_index += 1

    def render(self,
               screen: pygame.Surface,
               screen_pos: tuple[float, float],
               dt: float,
               ) -> None:

        if self.__mode == GhostMode.CHASE:
            if self._current_direction == Direction.NORTH:
                self._surface = \
                    self.__sprite_animation_up[self.__frame_index % len(self.__sprite_animation_up)]
            elif self._current_direction == Direction.SOUTH:
                self._surface = \
                    self.__sprite_animation_down[self.__frame_index % len(self.__sprite_animation_down)]
            elif self._current_direction == Direction.WEST:
                self._surface = \
                    self.__sprite_animation_left[self.__frame_index % len(self.__sprite_animation_left)]
            elif self._current_direction == Direction.EAST:
                self._surface = \
                    self.__sprite_animation_right[self.__frame_index % len(self.__sprite_animation_right)]
            else:
                self._surface = \
                    self.__sprite_animation_right[self.__frame_index % len(self.__sprite_animation_right)]

        elif self.__mode == GhostMode.FRIGHTENED:
            self._surface = \
                self.__frightened_animation[self.__frame_index % len(self.__frightened_animation)]
        # elif:
        #     self.__mode == GhostMode.SCATTER:
        #     ...
        super().render(screen, screen_pos, dt)
