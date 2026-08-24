import pygame

from src import __version__, __authors__

from src.graphics.ui.button import Button
from src.graphics.ui.text import Text

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.sprite_library import SpriteLibrary

from src.utils.settings import GameMode, Settings


class Menu:
    def __init__(self) -> None:
        self.__buttons: list[Button]
        self.__texts: list[TextWrapper]

        screen_width = Settings.WINDOW_WIDTH
        screen_height = Settings.WINDOW_HEIGHT

        button_size = 60
        first_y_button = screen_height / 3.5
        # List of buttons
        start_button = Button(
            (screen_width / 2, first_y_button),
            SpriteLibrary['yellow'],
            lambda: self._set_game_mode(GameMode.PLAYING),
            text='play',
            anchor='center',
            sprite_size=button_size
        )
        settings_button = Button(
            (screen_width / 2, first_y_button + 2 * button_size + 10),
            SpriteLibrary['yellow'],
            lambda: ...,
            text='settings',
            anchor='center',
            sprite_size=button_size
        )
        scores_button = Button(
            (screen_width / 2, first_y_button + 4 * button_size + 20),
            SpriteLibrary['yellow'],
            lambda: ...,
            text='scores',
            anchor='center',
            sprite_size=button_size
        )
        exit_button = Button(
            (screen_width / 2, first_y_button + 6 * button_size + 30),
            SpriteLibrary['yellow'],
            lambda: self._quit(),
            text='exit',
            anchor='center',
            sprite_size=button_size
        )
        # List of text boxes
        title_txt = Text(
            "pacman",
            (screen_width / 2, 100),
            SpriteLibrary['yellow'],
            100,
            anchor='center'
        )
        credits_text = Text(
            f"authors - {__authors__}",
            (0, screen_height),
            SpriteLibrary['white_text'],
            20,
            anchor='bottom left'
        )
        version_text = Text(
            f"version - {__version__}",
            (screen_width, screen_height),
            SpriteLibrary['white_text'],
            20,
            anchor='bottom right'
        )

        self.__buttons = [
            start_button,
            settings_button,
            scores_button,
            exit_button
        ]
        self.__texts = [
            title_txt,
            credits_text,
            version_text,
        ]

    @staticmethod
    def _set_game_mode(mode: GameMode) -> None:
        from src.core.game import Game
        Game.setGameMode(mode)

    @staticmethod
    def _quit() -> None:
        from src.core.game import Game
        Game.quit()

    def render(self, surface: pygame.Surface) -> None:
        try:
            for element in self.__buttons + self.__texts:
                element.render(surface)
        except AttributeError:
            return

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.__buttons:
                button.handle_event(event)
