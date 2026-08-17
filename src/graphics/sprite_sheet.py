from enum import Enum, auto

import pygame
from pygame.surface import Surface

from src.utils.settings import Settings


class SpriteType(Enum):
    # WALL SPRITES
    EMPTY_WALL = auto()
    UP_WALL = auto()
    RIGHT_WALL = auto()
    UP_RIGHT_WALL = auto()
    DOWN_WALL = auto()
    VERTICAL_WALL = auto()
    DOWN_RIGHT_WALL = auto()
    VERTICAL_RIGHT_WALL = auto()
    LEFT_WALL = auto()
    UP_LEFT_WALL = auto()
    HORIZONTAL_WALL = auto()
    HORIZONTAL_UP_WALL = auto()
    DOWN_LEFT_WALL = auto()
    VERTICAL_LEFT_WALL = auto()
    HORIZONTAL_DOWN_WALL = auto()
    CROSS_WALL = auto()
    FULL_WALL = auto()

    # FONT SPRITES
    L_A = auto()
    L_B = auto()
    L_C = auto()
    L_D = auto()
    L_E = auto()
    L_F = auto()
    L_G = auto()
    L_H = auto()
    L_I = auto()
    L_J = auto()
    L_K = auto()
    L_L = auto()
    L_M = auto()
    L_N = auto()
    L_O = auto()
    L_P = auto()
    L_Q = auto()
    L_R = auto()
    L_S = auto()
    L_T = auto()
    L_U = auto()
    L_V = auto()
    L_W = auto()
    L_X = auto()
    L_Y = auto()
    L_Z = auto()

    # NUMERIC SPRITES
    NUM_0 = auto()
    NUM_1 = auto()
    NUM_2 = auto()
    NUM_3 = auto()
    NUM_4 = auto()
    NUM_5 = auto()
    NUM_6 = auto()
    NUM_7 = auto()
    NUM_8 = auto()
    NUM_9 = auto()

    # SPECIAL CHARACTER SPRITE
    CH_SLASH = auto()
    CH_ESCL = auto()
    CH_LINE = auto()
    CH_CPRIGHT = auto()
    CH_DOT = auto()
    CH_QUOTE = auto()
    CH_SPACE = auto()


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
            color_key: tuple[int, int, int] = (0, 0, 0),
            ) -> None:

        self.__sheet = pygame.image.load(filename).convert_alpha()
        self.__sheet.set_colorkey(color_key)

        self.__data: dict[SpriteType, pygame.Surface] = {}

        self.__sprite_table: dict[int, dict[int, dict[int, pygame.Surface]]] = {
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
        self._load_font()

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

    def _load_font(self) -> None:
        # Font rendering is handled by `SpriteFont` when needed (e.g. in
        # `Renderer`). Avoid importing or instantiating `SpriteFont` here to
        # prevent circular imports.
        return None