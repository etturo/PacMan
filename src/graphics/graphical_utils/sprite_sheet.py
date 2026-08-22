from enum import Enum, auto

import pygame
from pygame.surface import Surface

from src.utils.settings import Settings

from src.graphics.graphical_utils.ui_utils import SpriteType


class SpriteSheet:
    """Load the atlas as three indexed grids of equally sized sprites."""

    _GRID_LAYOUTS: dict[int, tuple[tuple[int, int], tuple[int, int]]] = {
        8: ((0, 0), (199, 82)),
        16: ((0, 82), (171, 185)),
        25: ((171, 82), (199, 185)),
    }

    def __init__(
            self,
            filename: str,
            ) -> None:

        self.__sheet = pygame.image.load(filename)

        self.__data: dict[SpriteType, pygame.Surface] = {}

        self.__sprite_table: (dict[int,
                                   dict[int,
                                        dict[int,
                                             pygame.Surface
                                             ]
                                        ]
                                   ]
                              ) = {
            sprite_size: self._load_grid(
                section_start,
                section_end,
                sprite_size
                )
            for sprite_size, (
                section_start,
                section_end
                ) in self._GRID_LAYOUTS.items()
        }

        self._load_maze()

    def __getitem__(
            self,
            sprite: SpriteType,
            ) -> pygame.Surface:
        try:
            return_value = self.__data[sprite]
        except KeyError:
            return_value = self.__data[SpriteType.EMPTY_WALL]

        return return_value

    def _sprite(
            self,
            sprite_size: int,
            row: int,
            column: int,
            ) -> pygame.Surface:
        return self.__sprite_table[sprite_size][row][column]

    def _load_grid(
            self,
            top_left: tuple[int, int],
            bottom_right: tuple[int, int],
            sprite_size: int,
            ) -> dict[int, dict[int, pygame.Surface]]:

        rows: dict[int, dict[int, pygame.Surface]] = {}
        row_number = 1

        for y in range(
            top_left[1] + 1,
            bottom_right[1] - sprite_size + 1,
            sprite_size + 1,
        ):
            columns: dict[int, pygame.Surface] = {}
            column_index = 1

            for x in range(
                top_left[0] + 1,
                bottom_right[0] - sprite_size + 1,
                sprite_size + 1,
            ):
                rect = pygame.Rect(x, y, sprite_size, sprite_size)
                columns[column_index] = self._scale_surface(
                    self.__sheet.subsurface(rect)
                )
                column_index += 1

            if columns:
                rows[row_number] = columns
                row_number += 1

        return rows

    @staticmethod
    def _scale_surface(surface: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale_by(surface, Settings.DEFAULT_SCALE)

    def _load_maze(self) -> None:
        self.__data[SpriteType.EMPTY_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 8, 3),
            self._sprite(8, 8, 3),
            self._sprite(8, 8, 3),
            self._sprite(8, 8, 3)
        )
        self.__data[SpriteType.UP_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 2, 17),
            self._sprite(8, 2, 19),
            self._sprite(8, 3, 17),
            self._sprite(8, 3, 19)
        )
        self.__data[SpriteType.RIGHT_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 1, 17),
            self._sprite(8, 1, 18),
            self._sprite(8, 3, 17),
            self._sprite(8, 3, 18)
        )
        self.__data[SpriteType.UP_RIGHT_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 2, 17),
            self._sprite(8, 5, 19),
            self._sprite(8, 3, 17),
            self._sprite(8, 3, 18)
        )
        self.__data[SpriteType.DOWN_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 1, 17),
            self._sprite(8, 1, 19),
            self._sprite(8, 2, 17),
            self._sprite(8, 2, 19)
        )
        self.__data[SpriteType.VERTICAL_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 2, 17),
            self._sprite(8, 2, 19),
            self._sprite(8, 2, 17),
            self._sprite(8, 2, 19)
        )
        self.__data[SpriteType.DOWN_RIGHT_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 1, 17),
            self._sprite(8, 1, 18),
            self._sprite(8, 2, 17),
            self._sprite(8, 6, 19)
        )
        self.__data[SpriteType.VERTICAL_RIGHT_WALL] = \
            self._combine_sprites_2x2(
                self._sprite(8, 2, 17),
                self._sprite(8, 5, 19),
                self._sprite(8, 2, 17),
                self._sprite(8, 6, 19)
        )
        self.__data[SpriteType.LEFT_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 1, 18),
            self._sprite(8, 1, 19),
            self._sprite(8, 3, 18),
            self._sprite(8, 3, 19)
        )
        self.__data[SpriteType.UP_LEFT_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 5, 18),
            self._sprite(8, 2, 19),
            self._sprite(8, 3, 18),
            self._sprite(8, 3, 19)
        )
        self.__data[SpriteType.HORIZONTAL_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 1, 18),
            self._sprite(8, 1, 18),
            self._sprite(8, 3, 18),
            self._sprite(8, 3, 18)
        )
        self.__data[SpriteType.HORIZONTAL_UP_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 5, 18),
            self._sprite(8, 5, 19),
            self._sprite(8, 3, 18),
            self._sprite(8, 3, 18)
        )
        self.__data[SpriteType.DOWN_LEFT_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 1, 18),
            self._sprite(8, 1, 19),
            self._sprite(8, 6, 18),
            self._sprite(8, 2, 19)
        )
        self.__data[SpriteType.VERTICAL_LEFT_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 5, 18),
            self._sprite(8, 2, 19),
            self._sprite(8, 6, 18),
            self._sprite(8, 2, 19)
        )
        self.__data[SpriteType.HORIZONTAL_DOWN_WALL] = \
            self._combine_sprites_2x2(
                self._sprite(8, 1, 18),
                self._sprite(8, 1, 18),
                self._sprite(8, 6, 18),
                self._sprite(8, 6, 19)
        )
        self.__data[SpriteType.CROSS_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 5, 18),
            self._sprite(8, 5, 19),
            self._sprite(8, 6, 18),
            self._sprite(8, 6, 19)
        )
        self.__data[SpriteType.FULL_WALL] = self._combine_sprites_2x2(
            self._sprite(8, 4, 17),
            self._sprite(8, 4, 20),
            self._sprite(8, 7, 17),
            self._sprite(8, 7, 20)
        )

    def getMazeWalls(self) -> dict[SpriteType, Surface]:
        return self.__data

    @staticmethod
    def _combine_sprites_2x2(
            top_left: pygame.Surface,
            top_right: pygame.Surface,
            bottom_left: pygame.Surface,
            bottom_right: pygame.Surface,
            ) -> pygame.Surface:

        single_width = top_left.get_width()
        single_height = top_left.get_height()

        combined_surface = pygame.Surface(
            (single_width * 2, single_height * 2),
            pygame.SRCALPHA,
        )

        combined_surface.blit(top_left, (0, 0))
        combined_surface.blit(top_right, (single_width, 0))
        combined_surface.blit(bottom_left, (0, single_height))
        combined_surface.blit(bottom_right, (single_width, single_height))

        return combined_surface
