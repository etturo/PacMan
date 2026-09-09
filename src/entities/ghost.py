import pygame

from typing import Callable

from src.entities.entity import Entity
from src.entities.ghost_intelligence import (
    GhostContext,
    GhostMode,
    choose_direction,
)

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.ui_utils import SpriteType

from src.world.cell import Direction

__all__ = ['Ghost', 'GhostMode']


class Ghost(Entity):
    def __init__(
        self,
        init_pos: tuple[int, int],
        size: float,
        speed: float,
        sprite_sheet: SpriteSheet,
        # The strategy is a function prototyped like:
        # '''
        # def strategy(context: GhostContext)
        # '''
        # and returns the cell the ghost wants to reach, not the
        # Direction to get there: picking the direction is the same job
        # for the four of them, so decideNextMove() does it once.
        strategy: Callable[
            [
                GhostContext
            ],
            tuple[int, int]],
    ) -> None:

        super().__init__(init_pos, size, speed)
        self.__initial_speed = speed

        scale = SpriteSheet.scaleSprite

        self.__sheet = sprite_sheet
        self.__strategy = strategy
        self.__mode = GhostMode.CHASE

        frightened_sheet_1 = SpriteLibrary.get('melon')
        frightened_sheet_2 = SpriteLibrary.get('green')
        point_sheet = SpriteLibrary.get('red')

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

        self.__death_animation_200 = [
            scale(point_sheet[SpriteType.TWO_HUND_POINTS], size),
            scale(point_sheet[SpriteType.TWO_HUND_POINTS], size),
            scale(point_sheet[SpriteType.TWO_HUND_POINTS], size),
            scale(point_sheet[SpriteType.TWO_HUND_POINTS], size),
            scale(point_sheet[SpriteType.TWO_HUND_POINTS], size),
            scale(point_sheet[SpriteType.TWO_HUND_POINTS], size),
            scale(point_sheet[SpriteType.TWO_HUND_POINTS], size),
            scale(point_sheet[SpriteType.TWO_HUND_POINTS], size),
        ]
        self.__death_animation_400 = [
            scale(point_sheet[SpriteType.FOUR_HUND_POINTS], size),
            scale(point_sheet[SpriteType.FOUR_HUND_POINTS], size),
            scale(point_sheet[SpriteType.FOUR_HUND_POINTS], size),
            scale(point_sheet[SpriteType.FOUR_HUND_POINTS], size),
            scale(point_sheet[SpriteType.FOUR_HUND_POINTS], size),
            scale(point_sheet[SpriteType.FOUR_HUND_POINTS], size),
            scale(point_sheet[SpriteType.FOUR_HUND_POINTS], size),
            scale(point_sheet[SpriteType.FOUR_HUND_POINTS], size),
        ]
        self.__death_animation_800 = [
            scale(point_sheet[SpriteType.EIGHT_HUND_POINTS], size),
            scale(point_sheet[SpriteType.EIGHT_HUND_POINTS], size),
            scale(point_sheet[SpriteType.EIGHT_HUND_POINTS], size),
            scale(point_sheet[SpriteType.EIGHT_HUND_POINTS], size),
            scale(point_sheet[SpriteType.EIGHT_HUND_POINTS], size),
            scale(point_sheet[SpriteType.EIGHT_HUND_POINTS], size),
            scale(point_sheet[SpriteType.EIGHT_HUND_POINTS], size),
            scale(point_sheet[SpriteType.EIGHT_HUND_POINTS], size),
        ]
        self.__death_animation_1600 = [
            scale(point_sheet[SpriteType.SIXTEEN_HUND_POINTS], size),
            scale(point_sheet[SpriteType.SIXTEEN_HUND_POINTS], size),
            scale(point_sheet[SpriteType.SIXTEEN_HUND_POINTS], size),
            scale(point_sheet[SpriteType.SIXTEEN_HUND_POINTS], size),
            scale(point_sheet[SpriteType.SIXTEEN_HUND_POINTS], size),
            scale(point_sheet[SpriteType.SIXTEEN_HUND_POINTS], size),
            scale(point_sheet[SpriteType.SIXTEEN_HUND_POINTS], size),
            scale(point_sheet[SpriteType.SIXTEEN_HUND_POINTS], size),
        ]

        self.__animation_timer = 0.0
        self.__animation_delay = 0.1
        self.__frame_index = 0
        self.__frightened_timer = 0.0
        self.__time_frightened = 6.0
        self.__current_points = 0
        self.__death_animation_length = 0
        self._surface = self.__frightened_animation[0]

    def getMode(self) -> GhostMode:
        return self.__mode

    def setMode(self, new_mode: GhostMode) -> None:
        if new_mode == GhostMode.FRIGHTENED:
            # Eating another super pacgum restarts the countdown
            self.__frightened_timer = 0.0
            # and slows the ghosts
            self._speed = self.__initial_speed / 1.5
        else:
            self._speed = self.__initial_speed

        self.__mode = new_mode

    def decideNextMove(self, context: GhostContext) -> None:
        """Queue the direction that walks towards the strategy's target."""
        target = self.__strategy(context)

        # The target can be any cell of the maze, not just a neighbour,
        # so choose_direction() is the one that turns it into the single
        # step to take next.
        next_dir = choose_direction(
            context.maze,
            context.ghost_pos,
            self._current_direction,
            target,
        )

        if next_dir == self._current_direction.opposite():
            # A queued u-turn is thrown away by the anti-reversal filter
            # in PlayingState.update(), so it has to be written straight
            # into the current direction. Only happens in a dead end,
            # where turning back is the one legal move.
            self._current_direction = next_dir
            self.setQueueDirection(Direction.STILL)
            return

        self.setQueueDirection(next_dir)

    def die(self, current_points: int) -> None:
        # Based on the streak of ghost eaten the count of points
        # increases exponentially
        if current_points in [400, 800, 1600]:
            self.__current_points = current_points
        else:
            self.__current_points = 200

        self.__death_animation_length = {
            200: len(self.__death_animation_200),
            400: len(self.__death_animation_400),
            800: len(self.__death_animation_800),
            1600: len(self.__death_animation_1600),
        }[self.__current_points]
        self.__frame_index = 0
        self._is_alive = False
        self._speed = self.__initial_speed

    def update(self, dt: float) -> None:
        super().update(dt)

        if not self._is_alive:
            self.__animation_timer += dt
            if self.__animation_timer >= self.__animation_delay:
                self.__animation_timer = 0.0
                self.__frame_index += 1

                if self.__frame_index >= self.__death_animation_length:
                    self.resetPosition()
                    self._is_alive = True
                    self._queued_direction = Direction.STILL
                    self._current_direction = Direction.STILL
                    self.__mode = GhostMode.CHASE
                    self.__frame_index = 0
            return

        self.__animation_timer += dt

        if self.__mode == GhostMode.FRIGHTENED:
            self.__frightened_timer += dt
            if self.__frightened_timer >= self.__time_frightened:
                self.__mode = GhostMode.CHASE
                self.__frightened_timer = 0.0

        if self.__animation_timer >= self.__animation_delay:
            self.__animation_timer = 0.0
            self.__frame_index += 1

    def render(self,
               screen: pygame.Surface,
               screen_pos: tuple[float, float],
               dt: float,
               ) -> None:

        if not self._is_alive:
            match self.__current_points:
                case 200:
                    self._surface = \
                        self.__death_animation_200[
                            self.__frame_index % len(
                                self.__death_animation_200
                            )
                        ]
                case 400:
                    self._surface = \
                        self.__death_animation_400[
                            self.__frame_index % len(
                                self.__death_animation_400
                            )
                        ]
                case 800:
                    self._surface = \
                        self.__death_animation_800[
                            self.__frame_index % len(
                                self.__death_animation_800
                            )
                        ]
                case 1600:
                    self._surface = \
                        self.__death_animation_1600[
                            self.__frame_index % len(
                                self.__death_animation_1600
                            )
                        ]

        elif self.__mode == GhostMode.CHASE:
            if self._current_direction == Direction.NORTH:
                self._surface = \
                    self.__sprite_animation_up[
                        self.__frame_index % len(
                            self.__sprite_animation_up
                            )
                            ]
            elif self._current_direction == Direction.SOUTH:
                self._surface = \
                    self.__sprite_animation_down[
                        self.__frame_index % len(
                            self.__sprite_animation_down
                            )
                            ]
            elif self._current_direction == Direction.WEST:
                self._surface = \
                    self.__sprite_animation_left[
                        self.__frame_index % len(
                            self.__sprite_animation_left
                            )
                            ]
            elif self._current_direction == Direction.EAST:
                self._surface = \
                    self.__sprite_animation_right[
                        self.__frame_index % len(
                            self.__sprite_animation_right
                            )
                            ]
            else:
                self._surface = \
                    self.__sprite_animation_right[
                        self.__frame_index % len(
                            self.__sprite_animation_right
                            )
                            ]

        elif self.__mode == GhostMode.FRIGHTENED:
            self._surface = \
                self.__frightened_animation[
                    self.__frame_index % len(
                        self.__frightened_animation
                        )
                        ]
        # elif:
        #     self.__mode == GhostMode.SCATTER:
        #     ...
        super().render(screen, screen_pos, dt)
