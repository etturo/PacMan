import pygame

from src.graphics.ui.button import Button
from src.graphics.ui.text import Text

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.sprite_library import SpriteLibrary


class Menu:
    def __init__(self) -> None:
        self.__buttons: list[Button]
        self.__texts: list[TextWrapper]

        screen = pygame.display.get_surface()

        # List of buttons
        # List of text boxes
        title_txt = Text(
            "pacman",
            screen.get_rect().center,
            SpriteLibrary['azure'],
            100
        )

        self.__buttons = [

        ]
        self.__texts = [
            title_txt
        ]

    def render(self, surface: pygame.Surface) -> None:
        try:
            for element in self.__buttons + self.__texts:
                element.render(surface)
        except AttributeError:
            return