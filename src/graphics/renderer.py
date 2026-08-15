import pygame

from src.graphics.maze_render import MazeRender
from src.graphics.sprite_sheet import SpriteSheet
from src.world.maze import Maze


class Renderer:
    def __init__(self) -> None:
        # PYGAME VARIABLE INITIALIZED
        pygame.init()
        self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('PacMan')

        # RENDER UTILS
        self.__screen_width = self.__screen.get_width()
        self.__screen_height = self.__screen.get_height()

        # The maze renderer is an interface that render the maze,
        # the steps to make it work are first init, so it can initialize
        # every attribute that it need, and then the render method itself
        self.__maze_renderer: MazeRender = MazeRender()

        # The sprite sheet represent a sheet with a color palette associeted,
        # we can load different sheets with different palette but the usage is
        # equivalent
        self.__walls_sheet = SpriteSheet(
            'data/assets/sprites/blue-sprite-sheet.png'
        )
        self.__sheet = SpriteSheet(
            'data/assets/sprites/orange-sprite-sheet.png'
        )

    def render(
            self,
            maze: Maze
            ) -> None:
        # Render BG
        self.__screen.fill((0, 0, 0))

        self._render_maze(maze)

        # Update the screen
        pygame.display.flip()

    def _render_maze(self, maze: Maze) -> None:
        # Calculation to make the tiles of the maze proportional to the size
        # of the screen
        cell_size = min(
            self.__screen_width // maze.getSize()[0],
            self.__screen_height // maze.getSize()[1]
        ) // 2 - 1

        self.__maze_renderer.render(
            self.__screen,
            self.__walls_sheet,
            maze,
            cell_size,
            self.__screen_width,
            self.__screen_height
            )

    def _render_main_menu(self) -> None:
        ...
