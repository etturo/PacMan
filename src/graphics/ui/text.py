import pygame

from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.ui.drawable import Drawable

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet

class Text(Drawable):
    def __init__(
            self,
            text: str,
            position: tuple[int, int],
            sprite_sheet: SpriteSheet,
            text_size: int,
            centered: bool = True
        ) -> None:
        super().__init__(position, sprite_sheet, centered)

        self.__text = text.upper()
        self.__font = SpriteFont(sprite_sheet, text_size)

        self.__lenght, self.__height = self._calculate_text_size(
            text=self.__text,
            sprite_size=self.__font.getSize(),
            include_padding=False,
        )

        self._surface = pygame.Surface((self.__lenght, self.__height))
        self.__font.render(self._surface, (0, 0), self.__text)
