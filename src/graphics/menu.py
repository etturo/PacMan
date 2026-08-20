import pygame

from src.graphics.ui.button import Button
from src.graphics.ui.text_wrapper import TextWrapper

from src.utils.sprite_sheet import SpriteSheet
from src.utils.sprite_library import SpriteLibrary


class Menu:
    def __init__(self) -> None:
        self.__buttons: list[Button]
        self.__texts: list[TextWrapper]

        screen_x, screen_y = pygame.display.get_window_size()

        # List of sprite sheets
        

        # List of buttons
        # List of text boxes
        title_txt = TextWrapper(
            "pacman",
            (screen_x / 2, screen_y / 2),
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