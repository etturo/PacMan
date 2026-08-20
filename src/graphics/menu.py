import pygame

from src.graphics.ui.button import Button
from src.graphics.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.text_wrapper import TextWrapper


class Menu:
    def __init__(self) -> None:
        self.__buttons: list[Button]
        self.__texts: list[TextWrapper]

        screen_x, screen_y = pygame.display.get_window_size()

        # List of sprite sheets
        azure_sheet = SpriteSheet("data/assets/sprites/azure-sprite-sheet.png")

        # List of buttons
        # List of text boxes
        title_txt = TextWrapper(
            "pacman",
            (screen_x / 2, screen_y / 2),
            azure_sheet,
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