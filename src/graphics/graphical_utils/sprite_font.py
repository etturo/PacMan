import pygame

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.ui_utils import SpriteType

from src.graphics.graphical_utils.ui_utils import CHAR_MAPPING


class SpriteFont:
    def __init__(self, sheet: SpriteSheet, size: float = 16) -> None:
        self.__size = size
        self.__sheet = sheet
        self.__characters: dict[SpriteType, pygame.Surface] = {}
        self.__original_char: dict[SpriteType, pygame.Surface]

        # Init of all the character in the sprite sheet
        # ALPHABET (first row)
        self.__characters[SpriteType.L_A] = self.__sheet.getSprite(8, 4, 1)
        self.__characters[SpriteType.L_B] = self.__sheet.getSprite(8, 4, 2)
        self.__characters[SpriteType.L_C] = self.__sheet.getSprite(8, 4, 3)
        self.__characters[SpriteType.L_D] = self.__sheet.getSprite(8, 4, 4)
        self.__characters[SpriteType.L_E] = self.__sheet.getSprite(8, 4, 5)
        self.__characters[SpriteType.L_F] = self.__sheet.getSprite(8, 4, 6)
        self.__characters[SpriteType.L_G] = self.__sheet.getSprite(8, 4, 7)
        self.__characters[SpriteType.L_H] = self.__sheet.getSprite(8, 4, 8)
        self.__characters[SpriteType.L_I] = self.__sheet.getSprite(8, 4, 9)
        self.__characters[SpriteType.L_J] = self.__sheet.getSprite(8, 4, 10)
        self.__characters[SpriteType.L_K] = self.__sheet.getSprite(8, 4, 11)
        self.__characters[SpriteType.L_L] = self.__sheet.getSprite(8, 4, 12)
        self.__characters[SpriteType.L_M] = self.__sheet.getSprite(8, 4, 13)

        # ALPHABET (second row)
        self.__characters[SpriteType.L_N] = self.__sheet.getSprite(8, 5, 1)
        self.__characters[SpriteType.L_O] = self.__sheet.getSprite(8, 5, 2)
        self.__characters[SpriteType.L_P] = self.__sheet.getSprite(8, 5, 3)
        self.__characters[SpriteType.L_Q] = self.__sheet.getSprite(8, 5, 4)
        self.__characters[SpriteType.L_R] = self.__sheet.getSprite(8, 5, 5)
        self.__characters[SpriteType.L_S] = self.__sheet.getSprite(8, 5, 6)
        self.__characters[SpriteType.L_T] = self.__sheet.getSprite(8, 5, 7)
        self.__characters[SpriteType.L_U] = self.__sheet.getSprite(8, 5, 8)
        self.__characters[SpriteType.L_V] = self.__sheet.getSprite(8, 5, 9)
        self.__characters[SpriteType.L_W] = self.__sheet.getSprite(8, 5, 10)
        self.__characters[SpriteType.L_X] = self.__sheet.getSprite(8, 5, 11)
        self.__characters[SpriteType.L_Y] = self.__sheet.getSprite(8, 5, 12)
        self.__characters[SpriteType.L_Z] = self.__sheet.getSprite(8, 5, 13)

        # NUMBERS
        self.__characters[SpriteType.NUM_0] = self.__sheet.getSprite(8, 3, 1)
        self.__characters[SpriteType.NUM_1] = self.__sheet.getSprite(8, 3, 2)
        self.__characters[SpriteType.NUM_2] = self.__sheet.getSprite(8, 3, 3)
        self.__characters[SpriteType.NUM_3] = self.__sheet.getSprite(8, 3, 4)
        self.__characters[SpriteType.NUM_4] = self.__sheet.getSprite(8, 3, 5)
        self.__characters[SpriteType.NUM_5] = self.__sheet.getSprite(8, 3, 6)
        self.__characters[SpriteType.NUM_6] = self.__sheet.getSprite(8, 3, 7)
        self.__characters[SpriteType.NUM_7] = self.__sheet.getSprite(8, 3, 8)
        self.__characters[SpriteType.NUM_8] = self.__sheet.getSprite(8, 3, 9)
        self.__characters[SpriteType.NUM_9] = self.__sheet.getSprite(8, 3, 10)

        # SPECIAL CHARACTERS
        self.__characters[SpriteType.CH_SLASH] = \
            self.__sheet.getSprite(8, 2, 11)
        self.__characters[SpriteType.CH_LINE] = \
            self.__sheet.getSprite(8, 2, 12)
        self.__characters[SpriteType.CH_DOT] = \
            self.__sheet.getSprite(8, 2, 13)
        self.__characters[SpriteType.CH_QUOTE] = \
            self.__sheet.getSprite(8, 3, 11)
        self.__characters[SpriteType.CH_CPR] = \
            self.__sheet.getSprite(8, 3, 12)
        self.__characters[SpriteType.CH_ESCL] = \
            self.__sheet.getSprite(8, 3, 13)
        self.__characters[SpriteType.CH_SPACE] = \
            self.__sheet.getSprite(8, 8, 11)
        sheet1 = self.__sheet.getSprite(8, 2, 13)
        sheet2 = self.__sheet.getSprite(8, 2, 21)
        self.__characters[SpriteType.CH_COLON] = \
            self.__sheet.combineSprite2x2(sheet2, sheet1, sheet2, sheet1)

        self.__characters[SpriteType.LEFT_ARROW] = \
            self.__sheet.getRotatedSprite(16, 5, 2, 90)
        self.__characters[SpriteType.RIGHT_ARROW] = \
            self.__sheet.getRotatedSprite(16, 5, 2, 270)

        self.__original_char = self.__characters.copy()
        self.setSize(size)

    def render(self,
               screen: pygame.Surface,
               position: tuple[float, float],
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

    def getSize(self) -> float:
        return self.__size

    def setSize(self, new_size: float) -> None:
        if new_size <= 0:
            new_size = 8
        self.__size = new_size

        size = (new_size, new_size)

        for sprite_type in CHAR_MAPPING.values():
            self.__characters[sprite_type] = pygame.transform.scale(
                self.__original_char[sprite_type],
                size
            )
