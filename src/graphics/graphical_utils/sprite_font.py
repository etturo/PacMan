import pygame

from src.graphics.graphical_utils.sprite_sheet import SpriteType, SpriteSheet

from src.graphics.graphical_utils.ui_utils import CHAR_MAPPING


class SpriteFont:
    def __init__(self, sheet: SpriteSheet, size: int = 16) -> None:
        # note: the default size of the font is 8 because is the pixel
        #       size of the characters sprites, so if scaling is applied
        #       the value that is passed should be that value

        self.__size = size
        self.__sheet = sheet
        self.__characters: dict[SpriteType, pygame.Surface] = {}
        self.__original_char: dict[SpriteType, pygame.Surface]

        # Init of all the character in the sprite sheet
        # ALPHABET (first row)
        self.__characters[SpriteType.L_A] = self.__sheet._sprite(8, 4, 1)
        self.__characters[SpriteType.L_B] = self.__sheet._sprite(8, 4, 2)
        self.__characters[SpriteType.L_C] = self.__sheet._sprite(8, 4, 3)
        self.__characters[SpriteType.L_D] = self.__sheet._sprite(8, 4, 4)
        self.__characters[SpriteType.L_E] = self.__sheet._sprite(8, 4, 5)
        self.__characters[SpriteType.L_F] = self.__sheet._sprite(8, 4, 6)
        self.__characters[SpriteType.L_G] = self.__sheet._sprite(8, 4, 7)
        self.__characters[SpriteType.L_H] = self.__sheet._sprite(8, 4, 8)
        self.__characters[SpriteType.L_I] = self.__sheet._sprite(8, 4, 9)
        self.__characters[SpriteType.L_J] = self.__sheet._sprite(8, 4, 10)
        self.__characters[SpriteType.L_K] = self.__sheet._sprite(8, 4, 11)
        self.__characters[SpriteType.L_L] = self.__sheet._sprite(8, 4, 12)
        self.__characters[SpriteType.L_M] = self.__sheet._sprite(8, 4, 13)

        # ALPHABET (second row)
        self.__characters[SpriteType.L_N] = self.__sheet._sprite(8, 5, 1)
        self.__characters[SpriteType.L_O] = self.__sheet._sprite(8, 5, 2)
        self.__characters[SpriteType.L_P] = self.__sheet._sprite(8, 5, 3)
        self.__characters[SpriteType.L_Q] = self.__sheet._sprite(8, 5, 4)
        self.__characters[SpriteType.L_R] = self.__sheet._sprite(8, 5, 5)
        self.__characters[SpriteType.L_S] = self.__sheet._sprite(8, 5, 6)
        self.__characters[SpriteType.L_T] = self.__sheet._sprite(8, 5, 7)
        self.__characters[SpriteType.L_U] = self.__sheet._sprite(8, 5, 8)
        self.__characters[SpriteType.L_V] = self.__sheet._sprite(8, 5, 9)
        self.__characters[SpriteType.L_W] = self.__sheet._sprite(8, 5, 10)
        self.__characters[SpriteType.L_X] = self.__sheet._sprite(8, 5, 11)
        self.__characters[SpriteType.L_Y] = self.__sheet._sprite(8, 5, 12)
        self.__characters[SpriteType.L_Z] = self.__sheet._sprite(8, 5, 13)

        # NUMBERS
        self.__characters[SpriteType.NUM_0] = self.__sheet._sprite(8, 1, 1)
        self.__characters[SpriteType.NUM_1] = self.__sheet._sprite(8, 1, 2)
        self.__characters[SpriteType.NUM_2] = self.__sheet._sprite(8, 1, 3)
        self.__characters[SpriteType.NUM_3] = self.__sheet._sprite(8, 1, 4)
        self.__characters[SpriteType.NUM_4] = self.__sheet._sprite(8, 1, 5)
        self.__characters[SpriteType.NUM_5] = self.__sheet._sprite(8, 1, 6)
        self.__characters[SpriteType.NUM_6] = self.__sheet._sprite(8, 1, 7)
        self.__characters[SpriteType.NUM_7] = self.__sheet._sprite(8, 1, 8)
        self.__characters[SpriteType.NUM_8] = self.__sheet._sprite(8, 1, 9)
        self.__characters[SpriteType.NUM_9] = self.__sheet._sprite(8, 1, 10)

        # SPECIAL CHARACTERS
        self.__characters[SpriteType.CH_SLASH] = self.__sheet._sprite(8, 2, 11)
        self.__characters[SpriteType.CH_LINE] = self.__sheet._sprite(8, 2, 12)
        self.__characters[SpriteType.CH_DOT] = self.__sheet._sprite(8, 2, 13)
        self.__characters[SpriteType.CH_QUOTE] = self.__sheet._sprite(8, 3, 11)
        self.__characters[SpriteType.CH_CPR] = self.__sheet._sprite(8, 3, 12)
        self.__characters[SpriteType.CH_ESCL] = self.__sheet._sprite(8, 3, 13)
        self.__characters[SpriteType.CH_SPACE] = self.__sheet._sprite(8, 8, 11)

        self.__original_char = self.__characters.copy()
        self.setSize(size)

    def render(self,
               screen: pygame.Surface,
               position: tuple[int, int],
               text: str
               ) -> None:

        pos_x, pos_y = position

        initial_x = pos_x
        current_x = pos_x
        current_y = pos_y
        text = text.upper()

        for char in text:
            if char in CHAR_MAPPING:
                sprite_type = CHAR_MAPPING[char]
                sprite = self.__characters[sprite_type]

                screen.blit(sprite, (current_x, current_y))
                current_x += self.__size

            if char == "\n":
                current_x = initial_x
                current_y += self.__size

    def getSize(self) -> int:
        return self.__size

    def setSize(self, new_size: int) -> None:
        if new_size <= 0:
            new_size = 8
        self.__size = new_size

        size = (new_size, new_size)

        for sprite_type in CHAR_MAPPING.values():
            self.__characters[sprite_type] = pygame.transform.scale(
                self.__original_char[sprite_type],
                size
            )
