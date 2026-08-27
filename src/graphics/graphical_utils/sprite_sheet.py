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

        self.__sheet = pygame.image.load(filename).convert()
        self.__sheet.set_colorkey((0, 0, 0))

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

        self._load_skins()

    def __getitem__(
            self,
            sprite: SpriteType,
            ) -> pygame.Surface:
        try:
            return_value = self.__data[sprite]
        except KeyError:
            return_value = self.__data[SpriteType.EMPTY_WALL]

        return return_value

    def getSprite(
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

    def _load_skins(self) -> None:
        self.__data[SpriteType.EMPTY_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 8, 3),
            self.getSprite(8, 8, 3),
            self.getSprite(8, 8, 3),
            self.getSprite(8, 8, 3)
        )
        self.__data[SpriteType.UP_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 2, 17),
            self.getSprite(8, 2, 19),
            self.getSprite(8, 3, 17),
            self.getSprite(8, 3, 19)
        )
        self.__data[SpriteType.RIGHT_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 1, 17),
            self.getSprite(8, 1, 18),
            self.getSprite(8, 3, 17),
            self.getSprite(8, 3, 18)
        )
        self.__data[SpriteType.UP_RIGHT_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 2, 17),
            self.getSprite(8, 5, 19),
            self.getSprite(8, 3, 17),
            self.getSprite(8, 3, 18)
        )
        self.__data[SpriteType.DOWN_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 1, 17),
            self.getSprite(8, 1, 19),
            self.getSprite(8, 2, 17),
            self.getSprite(8, 2, 19)
        )
        self.__data[SpriteType.VERTICAL_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 2, 17),
            self.getSprite(8, 2, 19),
            self.getSprite(8, 2, 17),
            self.getSprite(8, 2, 19)
        )
        self.__data[SpriteType.DOWN_RIGHT_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 1, 17),
            self.getSprite(8, 1, 18),
            self.getSprite(8, 2, 17),
            self.getSprite(8, 6, 19)
        )
        self.__data[SpriteType.VERTICAL_RIGHT_WALL] = \
            self._combine_sprites_2x2(
                self.getSprite(8, 2, 17),
                self.getSprite(8, 5, 19),
                self.getSprite(8, 2, 17),
                self.getSprite(8, 6, 19)
        )
        self.__data[SpriteType.LEFT_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 1, 18),
            self.getSprite(8, 1, 19),
            self.getSprite(8, 3, 18),
            self.getSprite(8, 3, 19)
        )
        self.__data[SpriteType.UP_LEFT_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 5, 18),
            self.getSprite(8, 2, 19),
            self.getSprite(8, 3, 18),
            self.getSprite(8, 3, 19)
        )
        self.__data[SpriteType.HORIZONTAL_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 1, 18),
            self.getSprite(8, 1, 18),
            self.getSprite(8, 3, 18),
            self.getSprite(8, 3, 18)
        )
        self.__data[SpriteType.HORIZONTAL_UP_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 5, 18),
            self.getSprite(8, 5, 19),
            self.getSprite(8, 3, 18),
            self.getSprite(8, 3, 18)
        )
        self.__data[SpriteType.DOWN_LEFT_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 1, 18),
            self.getSprite(8, 1, 19),
            self.getSprite(8, 6, 18),
            self.getSprite(8, 2, 19)
        )
        self.__data[SpriteType.VERTICAL_LEFT_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 5, 18),
            self.getSprite(8, 2, 19),
            self.getSprite(8, 6, 18),
            self.getSprite(8, 2, 19)
        )
        self.__data[SpriteType.HORIZONTAL_DOWN_WALL] = \
            self._combine_sprites_2x2(
                self.getSprite(8, 1, 18),
                self.getSprite(8, 1, 18),
                self.getSprite(8, 6, 18),
                self.getSprite(8, 6, 19)
        )
        self.__data[SpriteType.CROSS_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 5, 18),
            self.getSprite(8, 5, 19),
            self.getSprite(8, 6, 18),
            self.getSprite(8, 6, 19)
        )
        self.__data[SpriteType.FULL_WALL] = self._combine_sprites_2x2(
            self.getSprite(8, 4, 17),
            self.getSprite(8, 4, 20),
            self.getSprite(8, 7, 17),
            self.getSprite(8, 7, 20)
        )
        self.__data[SpriteType.GHOST_EYE_RIGHT_1] = self.getSprite(16, 1, 1)
        self.__data[SpriteType.GHOST_EYE_RIGHT_2] = self.getSprite(16, 1, 2)
        self.__data[SpriteType.GHOST_EYE_LEFT_1] = self.getSprite(16, 1, 5)
        self.__data[SpriteType.GHOST_EYE_LEFT_2] = self.getSprite(16, 1, 6)
        self.__data[SpriteType.GHOST_EYE_DOWN_1] = self.getSprite(16, 1, 3)
        self.__data[SpriteType.GHOST_EYE_DOWN_2] = self.getSprite(16, 1, 4)
        self.__data[SpriteType.GHOST_EYE_UP_1] = self.getSprite(16, 1, 7)
        self.__data[SpriteType.GHOST_EYE_UP_2] = self.getSprite(16, 1, 8)

        self.__data[SpriteType.PACMAN_DOWN_1] = self.getSprite(16, 5, 8)
        self.__data[SpriteType.PACMAN_DOWN_2] = self.getSprite(16, 4, 8)
        self.__data[SpriteType.PACMAN_RIGHT_1] = self.getSprite(16, 5, 7)
        self.__data[SpriteType.PACMAN_RIGHT_2] = self.getSprite(16, 4, 7)
        self.__data[SpriteType.PACMAN_UP_1] = self.getRotatedSprite(16, 5, 8, 180)
        self.__data[SpriteType.PACMAN_UP_2] = self.getRotatedSprite(16, 4, 8, 180)
        self.__data[SpriteType.PACMAN_LEFT_1] = self.getRotatedSprite(16, 5, 7, 180)
        self.__data[SpriteType.PACMAN_LEFT_2] = self.getRotatedSprite(16, 4, 7, 180)
        self.__data[SpriteType.PACMAN_FULL] = self.getSprite(16, 6, 7)

        self.__data[SpriteType.PACMAN_DEATH_1] = self.getSprite(16, 4, 1)
        self.__data[SpriteType.PACMAN_DEATH_2] = self.getSprite(16, 4, 2)
        self.__data[SpriteType.PACMAN_DEATH_3] = self.getSprite(16, 4, 3)
        self.__data[SpriteType.PACMAN_DEATH_4] = self.getSprite(16, 4, 4)
        self.__data[SpriteType.PACMAN_DEATH_5] = self.getSprite(16, 4, 5)
        self.__data[SpriteType.PACMAN_DEATH_6] = self.getSprite(16, 4, 6)

        self.__data[SpriteType.PACMAN_DEATH_7] = self.getSprite(16, 5, 1)
        self.__data[SpriteType.PACMAN_DEATH_8] = self.getSprite(16, 5, 2)
        self.__data[SpriteType.PACMAN_DEATH_9] = self.getSprite(16, 5, 3)
        self.__data[SpriteType.PACMAN_DEATH_10] = self.getSprite(16, 5, 4)
        self.__data[SpriteType.PACMAN_DEATH_11] = self.getSprite(16, 5, 5)
        self.__data[SpriteType.PACMAN_DEATH_12] = self.getSprite(16, 5, 6)

        self.__data[SpriteType.LIVES_SPRITE] = self._combine_sprites_2x2(
            self.getSprite(8, 8, 1),
            self.getSprite(8, 8, 2),
            self.getSprite(8, 9, 1),
            self.getSprite(8, 9, 2)
        )

        self.__data[SpriteType.PACGUM] = self.getSprite(8, 2, 16)
        self.__data[SpriteType.SUPER_PACGUMS] = self.getSprite(8, 4, 16)


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

    def getRotatedSprite(
            self,
            sprite_size: int,
            row: int,
            column: int,
            degree: int
            ) -> pygame.Surface:
        
        base_surface = self.getSprite(sprite_size, row, column)
        return pygame.transform.rotate(base_surface, degree)

    @staticmethod
    def scaleSprite(sprite: pygame.Surface, size: int) -> pygame.Surface:
        return pygame.transform.scale(sprite, (size, size))