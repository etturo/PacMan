import pygame

from src.world.maze import Maze
from src.graphics.sprite_sheet import SpriteSheet, SpriteType


class Renderer:
    def __init__(self) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('PacMan')

        self.__sheet = SpriteSheet('data/assets/sprites/azure-sprite-sheet.png')

    def render(self, maze: Maze) -> None:
        self._render_maze(maze)

    def _render_maze(self, maze: Maze) -> None:
        self.__screen.fill((50, 50, 50))

        self.__screen.blit(self.__sheet[SpriteType.ONE], (100, 300))
        self.__screen.blit(self.__sheet[SpriteType.TWO], (116, 300))
        self.__screen.blit(self.__sheet[SpriteType.THREE], (100, 316))
        self.__screen.blit(self.__sheet[SpriteType.VERTICAL_WALL_RIGHT], (116, 316))
        self.__screen.blit(self.__sheet[SpriteType.PACMAN_VERTICAL_STEP_1], (100, 300))

        pygame.display.flip()
