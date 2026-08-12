import pygame

from src.graphics.sprite_sheet import SpriteSheet, SpriteType
from src.world.cell import Cell, Direction
from src.world.maze import Maze


class Renderer:
    def __init__(self) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.display.set_caption('PacMan')

        self.__screen_width = self.__screen.get_width()
        self.__screen_height = self.__screen.get_height()

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
        grid_columns, grid_rows = maze.getSize()
        grid_columns = grid_columns * 2 + 1
        grid_rows = grid_rows * 2 + 1

        self.__cell_size = min(
            self.__screen_width // grid_columns,
            self.__screen_height // grid_rows,
        ) - 1
        offset_x = (self.__screen_width - (self.__cell_size * grid_columns)) / 2
        offset_y = (self.__screen_height - (self.__cell_size * grid_rows)) / 2

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
        WALL_MAPPING: dict[int, SpriteType] = {
            0: SpriteType.EMPTY_WALL,
            1: SpriteType.UP_WALL,
            2: SpriteType.RIGHT_WALL,
            3: SpriteType.UP_RIGHT_WALL,
            4: SpriteType.DOWN_WALL,
            5: SpriteType.VERTICAL_WALL,
            6: SpriteType.DOWN_RIGHT_WALL,
            7: SpriteType.VERTICAL_RIGHT_WALL,
            8: SpriteType.LEFT_WALL,
            9: SpriteType.UP_LEFT_WALL,
            10: SpriteType.HORIZONTAL_WALL,
            11: SpriteType.HORIZONTAL_UP_WALL,
            12: SpriteType.DOWN_LEFT_WALL,
            13: SpriteType.VERTICAL_LEFT_WALL,
            14: SpriteType.HORIZONTAL_DOWN_WALL,
            15: SpriteType.FULL_WALL
        }

        def check_wall(walls: list[list[bool]], x: int, y: int) -> bool:
            h = len(walls)
            w = len(walls[0]) if h > 0 else 0
            return 0 <= x < w and 0 <= y < h and walls[y][x]

        def get_neighbour(walls: list[list[bool]], x: int, y: int) -> int:
            result: int = 0

            if not walls[y][x]:
                return 0

            result |= 1 if check_wall(walls, x, y-1) else 0
            result |= 2 if check_wall(walls, x+1, y) else 0
            result |= 4 if check_wall(walls, x, y+1) else 0
            result |= 8 if check_wall(walls, x-1, y) else 0

            return result

        maze_columns, maze_rows = maze.getSize()
        v_maze_height = maze_rows * 2 + 1
        v_maze_width = maze_columns * 2 + 1

        walls: list[list[bool]] = \
            [[False] * v_maze_width for _ in range(v_maze_height)]

        offset_x = (self.__screen_width - (self.__cell_size * v_maze_width)) / 2
        offset_y = (self.__screen_height - (self.__cell_size * v_maze_height)) / 2

        for y in range(maze_rows):
            for x in range(maze_columns):
                rx: int = x * 2 + 1
                ry: int = y * 2 + 1

                cell = maze[x, y]

                n = cell.hasWall(Direction.NORTH)
                w = cell.hasWall(Direction.WEST)
                e = cell.hasWall(Direction.EAST)
                s = cell.hasWall(Direction.SOUTH)

                walls[ry-1][rx] |= n
                walls[ry][rx-1] |= w
                walls[ry][rx+1] |= e
                walls[ry+1][rx] |= s

                walls[ry-1][rx-1] |= n or w
                walls[ry-1][rx+1] |= n or e
                walls[ry+1][rx-1] |= s or w
                walls[ry+1][rx+1] |= s or e


        for y in range(v_maze_height):
            for x in range(v_maze_width):
                cell_center_x = offset_x + (x + 0.5) * self.__cell_size
                cell_center_y = offset_y + (y + 0.5) * self.__cell_size

                wall_map = get_neighbour(walls, x, y)
                self.__screen.blit(self.__sheet[SpriteType.UP_WALL], (0, 0))

                if wall_map > 0:
                    sprite_type = WALL_MAPPING.get(wall_map)
                    sprite = self.__sheet[sprite_type]
                    scaled_sprite = pygame.transform.scale(sprite, (self.__cell_size, self.__cell_size))
                    rect = scaled_sprite.get_rect(center=(cell_center_x, cell_center_y))
                    self.__screen.blit(scaled_sprite, rect)
