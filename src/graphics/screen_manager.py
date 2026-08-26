import pygame

from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.utils.settings import Settings

class ScreenManager:
    def __init__(self) -> None:
        pygame.init()

        self.__virtual_screen_width = Settings.VIRTUAL_WINDOW_WIDTH
        self.__virtual_screen_height = Settings.VIRTUAL_WINDOW_HEIGHT

        self.__screen = pygame.display.set_mode(
            (self.__virtual_screen_width, self.__virtual_screen_height),
            pygame.FULLSCREEN | pygame.SCALED | pygame.RESIZABLE
        )
        pygame.display.set_caption('PacMan')

        self.__crt_overlay = self._generate_crt_overlay()

        self.__is_fullscreen = True

        SpriteLibrary.load()
        SpriteLibrary.add_item('title', 'white_text')
        SpriteLibrary.add_item('wall_skins', 'blue')

    def _generate_crt_overlay(self) -> pygame.Surface:
        overlay = pygame.Surface(
            (self.__virtual_screen_width, self.__virtual_screen_height),
            pygame.SRCALPHA
        )

        for y in range(0, self.__virtual_screen_height, 3):
            pygame.draw.line(
                overlay,
                (0, 0, 0, 70),
                (0, y),
                (self.__virtual_screen_width, y)
            )

        return overlay

    def getScreen(self) -> pygame.Surface:
        return self.__screen

    def render(self, surface: pygame.Surface, crt: bool = True) -> None:
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(surface, (0, 0))

        if crt:
            self.__screen.blit(self.__crt_overlay, (0, 0))

        pygame.display.flip()