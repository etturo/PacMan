import pygame
import random

from src.graphics.maze_render import MazeRender
from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.graphical_utils.ui_utils import CHAR_MAPPING
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.ui.button import Button
from src.graphics.ui.text import Text

from src.world.maze import Maze

from src.utils.settings import Settings

from src.utils.settings import GameMode

class ScreenManager:
    def __init__(self) -> None:
        # RENDER UTILS
        self.__screen_width = Settings.WINDOW_WIDTH
        self.__screen_height = Settings.WINDOW_HEIGHT
        self.__frame_count = 0

        # PYGAME VARIABLE INITIALIZED
        pygame.init()
        self.__screen = pygame.display.set_mode(
            (self.__screen_width, self.__screen_height),
            pygame.FULLSCREEN | pygame.SCALED
            )
        pygame.display.set_caption('PacMan')

        self.__crt_overlay = self._generate_crt_overlay()

        # The sprite sheet library loads all the sheets that are in the
        # 'data/assets/sprites' folder you can access to all the sprites
        # like a dictionary to the SpriteLibrary interface
        SpriteLibrary()
        # Is possible to add new key to access to the same value
        # so it's easier to access to the same value in different contexts
        SpriteLibrary.add_item('title', 'white_text')
        SpriteLibrary.add_item('wall_skins', 'blue')

        self.__crt_overlay = self._generate_crt_overlay()

    def _generate_crt_overlay(self) -> pygame.Surface:
        overlay = pygame.Surface(
            (self.__screen_width, self.__screen_height),
            pygame.SRCALPHA)

        for y in range(0, self.__screen_height, 3):
            pygame.draw.line(
                overlay,
                (0, 0, 0, 70),
                (0, y),
                (self.__screen_width, y))

        return overlay

    def getScreen(self) -> pygame.Surface:
        return self.__screen

    def render(self, surface: pygame.Surface, crt: bool = True) -> None:
        if crt:
            self._generate_crt_overlay()

        self.__screen.blit(surface)

        self.__screen.blit(self.__crt_overlay, (0, 0))

        pygame.display.flip()

    

    def _render_main_menu(self) -> None:
        self.__menu.render(self.__screen)

    

    def handle_menu_events(self, events: list[pygame.event.Event]) -> None:
        self.__menu.handle_events(events)
