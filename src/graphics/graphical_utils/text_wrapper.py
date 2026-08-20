import pygame

from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.sprite_sheet import SpriteSheet

class TextWrapper:
    def __init__(
        self,
        text: str,
        pos: tuple[int, int],
        sprite_sheet: SpriteSheet,
        text_size: int
        ) -> None:
        self.text = text
        self.position = pos
        self.font = SpriteFont(sprite_sheet, text_size)

    def render(self, surface: pygame.Surface, centered: bool = True) -> None:
        position = self.position

        if centered == True:
            ...

        self.font.render(surface, position[0], position[1], self.text)
