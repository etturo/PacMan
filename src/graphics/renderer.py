import pygame

from src.graphics.sprite_sheet import SpriteSheet
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
        self.__screen.fill((50, 50, 50))
        self._render_grid(maze)
        # self._render_maze(maze)
        pygame.display.flip()

    def _render_grid(self, maze: Maze) -> None:
        screen_width, screen_height = pygame.display.get_window_size()
        grid_columns, grid_rows = maze.getSize()

        cell_size = min(
            screen_width / grid_columns,
            screen_height / grid_rows,
        )
        offset_x = (screen_width - (cell_size * grid_columns)) / 2
        offset_y = (screen_height - (cell_size * grid_rows)) / 2

        grid_color = (245, 245, 245)

        for column in range(grid_columns + 1):
            x = int(offset_x + column * cell_size)
            pygame.draw.line(
                self.__screen,
                grid_color,
                (x, int(offset_y)),
                (x, int(offset_y + cell_size * grid_rows)),
            )

        for row in range(grid_rows + 1):
            y = int(offset_y + row * cell_size)
            pygame.draw.line(
                self.__screen,
                grid_color,
                (int(offset_x), y),
                (int(offset_x + cell_size * grid_columns), y),
            )

    def _render_maze(self, maze: Maze) -> None:
        # width, height = maze.getSize()

        # for y in range(height):
        #     for x in range(width):
        ...
