import pygame

from typing import Callable, TYPE_CHECKING
from enum import Enum, auto

from src.entities.entity import Entity

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.ui_utils import SpriteType

from src.world.cell import Direction

# Only for the annotations: ghost_intelligence imports GhostMode from
# here, so importing it back at runtime would be a circular import.
if TYPE_CHECKING:
    from src.entities.ghost_intelligence import GhostContext


class GhostMode(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()


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
                'GhostContext'
            ],
            tuple[int, int]],
    ) -> None:

        super().__init__(init_pos, size, speed)

        scale = SpriteSheet.scaleSprite

        self.__sheet = sprite_sheet
        self.__strategy = strategy
        self.__mode = GhostMode.CHASE

        frightened_sheet_1 = SpriteLibrary.get('melon')
        frightened_sheet_2 = SpriteLibrary.get('green')

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

        self.__animation_timer = 0.0
        self.__animation_delay = 0.1
        self.__frame_index = 0
        self.__frightened_timer = 0.0
        self.__time_frightened = 6.0
        self._surface = self.__frightened_animation[0]

    def getMode(self) -> GhostMode:
        return self.__mode

    def setMode(self, new_mode: GhostMode) -> None:
        # Eating another super pacgum restarts the countdown
        if new_mode == GhostMode.FRIGHTENED:
            self.__frightened_timer = 0.0
        self.__mode = new_mode

    def decideNextMove(self, context: 'GhostContext') -> None:
        """Queue the direction that walks towards the strategy's target."""
        target = self.__strategy(context)

        # STEP 2: choose_direction() goes here, so that a target further
        # away than one cell can be reached too.
        d_x = target[0] - context.ghost_pos[0]
        d_y = target[1] - context.ghost_pos[1]
        next_dir = Direction.vecToDir((d_x, d_y))

        if next_dir == self._current_direction.opposite():
            # A queued u-turn is thrown away by the anti-reversal filter
            # in PlayingState.update(), so it has to be written straight
            # into the current direction. Only happens in a dead end,
            # where turning back is the one legal move.
            self._current_direction = next_dir
            self.setQueueDirection(Direction.STILL)
            return

        self.setQueueDirection(next_dir)

    def update(self, dt: float) -> None:
        super().update(dt)

        if self.__mode == GhostMode.FRIGHTENED:
            self.__frightened_timer += dt
            if self.__frightened_timer >= self.__time_frightened:
                self.__mode = GhostMode.CHASE
                self.__frightened_timer = 0.0

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
