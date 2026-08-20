import pygame

from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.drawable import Drawable

from src.utils.sprite_sheet import SpriteSheet

class Text(Drawable):
    def __init__(
            self,
            text: str,
            position: tuple[int, int],
            sprite_sheet: SpriteSheet,
            text_size: int
        ) -> None:
        super().__init__(position, sprite_sheet)

        self.__text = text
        self.__font = SpriteFont(sprite_sheet, text_size)

    def render(self, surface: pygame.Surface) -> None:
        self.__font.render(surface, self._position, self.__text)
