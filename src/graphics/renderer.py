import pygame

from src.graphics.sprite_sheet import SpriteSheet, SpriteType
from src.world.maze import Maze


class Renderer:
    def __init__(self) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('PacMan')

        self.__sheet = SpriteSheet(
            'data/assets/sprites/orange-sprite-sheet.png'
        )

    def render(self, maze: Maze) -> None:
        self._render_maze(maze)

    def _render_maze(self, maze: Maze) -> None:
        self.__screen.fill((50, 50, 50))

        self.__screen.blit(
            self.__sheet[SpriteType.UP_RIGHT_WALL],
            (100, 300)
            )

        pygame.display.flip()
