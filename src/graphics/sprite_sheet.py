from enum import Enum, auto

import pygame

from src.utils.settings import Settings


class SpriteCoord(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"


class SpriteType(Enum):
    VERTICAL_WALL = auto()


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

        self.sheet = pygame.image.load(filename).convert_alpha()
        self.sheet.set_colorkey(color_key)

        self.sheets: dict[int, dict[int, dict[SpriteCoord, pygame.Surface]]] = {
            sprite_size: self._load_grid(section_start, section_end, sprite_size)
            for sprite_size, (section_start, section_end) in self._GRID_LAYOUTS.items()
        }

        

    def __getitem__(
            self,
            coordinates: tuple[int, int, SpriteCoord | str],
        ) -> pygame.Surface:

        sprite_size, row, column = coordinates
        return self.sheets[sprite_size][row][self._normalize_column(column)]

    def sprite(
            self,
            sprite_size: int,
            row: int,
            column: SpriteCoord | str,
        ) -> pygame.Surface:
        return self.sheets[sprite_size][row][self._normalize_column(column)]

    def _load_grid(
            self,
            top_left: tuple[int, int],
            bottom_right: tuple[int, int],
            sprite_size: int,
        ) -> dict[int, dict[SpriteCoord, pygame.Surface]]:

        rows: dict[int, dict[SpriteCoord, pygame.Surface]] = {}
        row_number = 1

        for y in range(
            top_left[1] + 1,
            bottom_right[1] - sprite_size + 1,
            sprite_size + 1,
        ):
            columns: dict[SpriteCoord, pygame.Surface] = {}
            column_index = 0

            for x in range(
                top_left[0] + 1,
                bottom_right[0] - sprite_size + 1,
                sprite_size + 1,
            ):
                rect = pygame.Rect(x, y, sprite_size, sprite_size)
                columns[self._column_from_index(column_index)] = self._scale_surface(
                    self.sheet.subsurface(rect)
                )
                column_index += 1

            if columns:
                rows[row_number] = columns
                row_number += 1

        return rows

    @staticmethod
    def _column_from_index(index: int) -> SpriteCoord:
        return SpriteCoord(chr(ord("A") + index))

    @staticmethod
    def _normalize_column(column: SpriteCoord | str) -> SpriteCoord:
        if isinstance(column, SpriteCoord):
            return column

        return SpriteCoord(column.upper())

    @staticmethod
    def _scale_surface(surface: pygame.Surface) -> pygame.Surface:
        return pygame.transform.scale_by(surface, Settings.DEFAULT_SCALE)

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
