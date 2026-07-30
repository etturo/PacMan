from enum import Enum

import pygame

from src.utils.settings import Settings


class SpriteColumn(str, Enum):
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
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"


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
        self.sheets: dict[int, dict[int, dict[SpriteColumn, pygame.Surface]]] = {
            sprite_size: self._load_grid(section_start, section_end, sprite_size)
            for sprite_size, (section_start, section_end) in self._GRID_LAYOUTS.items()
        }
        self.composites: dict[str, pygame.Surface] = {
            "vertical_wall": self._combine_sprites_2x2(
                self.sheets[8][2][SpriteColumn.U],
                self.sheets[8][2][SpriteColumn.T],
                self.sheets[8][2][SpriteColumn.U],
                self.sheets[8][2][SpriteColumn.T],
            )
        }

    def __getitem__(
        self,
        coordinates: tuple[int, int, SpriteColumn | str],
    ) -> pygame.Surface:
        sprite_size, row, column = coordinates
        return self.sheets[sprite_size][row][self._normalize_column(column)]

    def sprite(
        self,
        sprite_size: int,
        row: int,
        column: SpriteColumn | str,
    ) -> pygame.Surface:
        return self.sheets[sprite_size][row][self._normalize_column(column)]

    def _load_grid(
        self,
        top_left: tuple[int, int],
        bottom_right: tuple[int, int],
        sprite_size: int,
    ) -> dict[int, dict[SpriteColumn, pygame.Surface]]:
        rows: dict[int, dict[SpriteColumn, pygame.Surface]] = {}
        row_number = 1

        for y in range(
            top_left[1] + 1,
            bottom_right[1] - sprite_size + 1,
            sprite_size + 1,
        ):
            columns: dict[SpriteColumn, pygame.Surface] = {}
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
    def _column_from_index(index: int) -> SpriteColumn:
        return SpriteColumn(chr(ord("A") + index))

    @staticmethod
    def _normalize_column(column: SpriteColumn | str) -> SpriteColumn:
        if isinstance(column, SpriteColumn):
            return column

        return SpriteColumn(column.upper())

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
