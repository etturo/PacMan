import pygame

from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.ui.drawable import Drawable

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet


class Text(Drawable):
    def __init__(
            self,
            text: str,
            position: tuple[float, float],
            sprite_sheet: SpriteSheet,
            text_size: int,
            anchor: str = "center",
            ) -> None:
        super().__init__(position, sprite_sheet, anchor)

        self.__text = text.upper()
        self.__font = SpriteFont(sprite_sheet, text_size)

        self.__width, self.__height = self._calculate_text_size(
            text=self.__text,
            sprite_size=self.__font.getSize(),
            include_padding=False,
        )

        self._surface = pygame.Surface((self.__width, self.__height))
        # import random
        # self._surface.fill((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
        self.__font.render(self._surface, (0, 0), self.__text)

    def getSize(self) -> tuple[float, float]:
        return (self.__width, self.__height)


