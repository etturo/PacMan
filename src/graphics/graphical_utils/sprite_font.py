import pygame

from src.graphics.sprite_sheet import SpriteSheet, SpriteType


class SpriteFont(SpriteSheet):
    def __init__(
        self,
        sprite_table: dict[int, dict[int, dict[int, pygame.Surface]]],
        font_size: int
        ) -> None:

        self.__size = font_size
        self.__sheet = sprite_sheet
        self.__GRID_LAYOUT = grid_layout
        self.__characters = dict[SpriteType, pygame.Surface] = {}

        # Init of all the character in the sprite sheet
        self.__characters[SpriteType.L_A] = self._sprite(8, 4, 1)
        self.__characters[SpriteType.L_B] = self._sprite(8, 4, 2)
        self.__characters[SpriteType.L_C] = self._sprite(8, 4, 3)
        self.__characters[SpriteType.L_D] = self._sprite(8, 4, 4)
        self.__characters[SpriteType.L_E] = self._sprite(8, 4, 5)
        self.__characters[SpriteType.L_F] = self._sprite(8, 4, 6)
        self.__characters[SpriteType.L_G] = self._sprite(8, 4, 7)
        self.__characters[SpriteType.L_H] = self._sprite(8, 4, 8)
        self.__characters[SpriteType.L_I] = self._sprite(8, 4, 9)
        self.__characters[SpriteType.L_J] = self._sprite(8, 4, 10)
        self.__characters[SpriteType.L_K] = self._sprite(8, 4, 11)
        self.__characters[SpriteType.L_L] = self._sprite(8, 4, 12)
        self.__characters[SpriteType.L_M] = self._sprite(8, 4, 13)

        self.__characters[SpriteType.L_N] = self._sprite(8, 5, 1)
        self.__characters[SpriteType.L_O] = self._sprite(8, 5, 2)
        self.__characters[SpriteType.L_P] = self._sprite(8, 5, 3)
        self.__characters[SpriteType.L_Q] = self._sprite(8, 5, 4)
        self.__characters[SpriteType.L_R] = self._sprite(8, 5, 5)
        self.__characters[SpriteType.L_S] = self._sprite(8, 5, 6)
        self.__characters[SpriteType.L_T] = self._sprite(8, 5, 7)
        self.__characters[SpriteType.L_U] = self._sprite(8, 5, 8)
        self.__characters[SpriteType.L_V] = self._sprite(8, 5, 9)
        self.__characters[SpriteType.L_W] = self._sprite(8, 5, 10)
        self.__characters[SpriteType.L_X] = self._sprite(8, 5, 11)
        self.__characters[SpriteType.L_Y] = self._sprite(8, 5, 12)
        self.__characters[SpriteType.L_Z] = self._sprite(8, 5, 13)

        self.__characters[SpriteType.NUM_0] = self._sprite(8, 1, 1)
        self.__characters[SpriteType.NUM_1] = self._sprite(8, 1, 2)
        self.__characters[SpriteType.NUM_2] = self._sprite(8, 1, 3)
        self.__characters[SpriteType.NUM_3] = self._sprite(8, 1, 4)
        self.__characters[SpriteType.NUM_4] = self._sprite(8, 1, 5)
        self.__characters[SpriteType.NUM_5] = self._sprite(8, 1, 6)
        self.__characters[SpriteType.NUM_6] = self._sprite(8, 1, 7)
        self.__characters[SpriteType.NUM_7] = self._sprite(8, 1, 8)
        self.__characters[SpriteType.NUM_8] = self._sprite(8, 1, 9)
        self.__characters[SpriteType.NUM_9] = self._sprite(8, 1, 10)

    def render(self) -> pygame.Surface:
        ...

    def setSize(self, new_size: int) -> None:
        self.__size = new_size
