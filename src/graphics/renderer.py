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
        # Render BG
        self.__screen.fill((50, 50, 50))

        self._render_grid(maze)
        self._render_maze(maze)

        pygame.display.flip()

    def _render_grid(self, maze: Maze) -> None:
        screen_width, screen_height = pygame.display.get_window_size()
        grid_columns, grid_rows = maze.getSize()
        grid_columns = grid_columns * 2 + 1
        grid_rows = grid_rows * 2 + 1

        self.__cell_size = min(
            screen_width / grid_columns,
            screen_height / grid_rows,
        ) - 1
        offset_x = (screen_width - (self.__cell_size * grid_columns)) / 2
        offset_y = (screen_height - (self.__cell_size * grid_rows)) / 2

        grid_color = (245, 245, 245)

        for column in range(grid_columns + 1):
            x = int(offset_x + column * self.__cell_size)
            pygame.draw.line(
                self.__screen,
                grid_color,
                (x, int(offset_y)),
                (x, int(offset_y + self.__cell_size * grid_rows)),
            )

        for row in range(grid_rows + 1):
            y = int(offset_y + row * self.__cell_size)
            pygame.draw.line(
                self.__screen,
                grid_color,
                (int(offset_x), y),
                (int(offset_x + self.__cell_size * grid_columns), y),
            )

        font_size = max(1, int(self.__cell_size * 0.75))
        font = pygame.font.Font(None, font_size)
        text_color = (150, 150, 150)

        for row_index, row in enumerate(maze):
            for column_index, cell in enumerate(row):
                text = font.render(str(cell), True, text_color)
                center_x = offset_x + ((column_index * 2) + 1.5) * self.__cell_size
                center_y = offset_y + ((row_index * 2) + 1.5) * self.__cell_size
                text_rect = text.get_rect(center=(int(center_x), int(center_y)))
                self.__screen.blit(text, text_rect)

    def _render_maze(self, maze: Maze) -> None:
        screen_width, screen_height = pygame.display.get_window_size()
        grid_columns, grid_rows = maze.getSize()
        grid_columns = grid_columns * 2 + 1
        grid_rows = grid_rows * 2 + 1

        offset_x = (screen_width - (self.__cell_size * grid_columns)) / 2
        offset_y = (screen_height - (self.__cell_size * grid_rows)) / 2

        for row_index, row in enumerate(maze):
            for column_index, cell in enumerate(row):
                center_x = offset_x + ((column_index * 2) + 1.5) * self.__cell_size
                center_y = offset_y + ((row_index * 2) + 1.5) * self.__cell_size
                centered_rect = self.__sheet[SpriteType.VERTICAL_WALL]
                sprite_rect = centered_rect.get_rect(
                    center=(int(center_x), int(center_y))
                )
                self.__screen.blit(centered_rect, sprite_rect)
