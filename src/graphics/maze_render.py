import pygame

from src.utils.sprite_sheet import SpriteSheet, SpriteType
from src.world.cell import Direction
from src.world.maze import Maze


class MazeRender:
    def __init__(self) -> None:
        self.WALL_MAPPING: dict[int, SpriteType] = {
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
            15: SpriteType.CROSS_WALL,
        }

    def init_maze(self,
             maze: Maze,
             cell_size: int,
             sprite_sheet: SpriteSheet
              ) -> None:
        self.__sheet = sprite_sheet
        self.__screen_width, self.__screen_height = \
            pygame.display.get_window_size()

        self.__maze = maze
        self.__maze_columns, self.__maze_rows = maze.getSize()

        self._create_expanded_maze()

        self.__cell_size = cell_size

        self.__offset_x = (
            self.__screen_width - (self.__cell_size * self.__v_maze_width)
        ) / 2
        self.__offset_y = (
            self.__screen_height - (self.__cell_size * self.__v_maze_height)
        ) / 2

    def _check_wall(self, x: int, y: int) -> bool:
        h = len(self.__walls)
        w = len(self.__walls[0]) if h > 0 else 0
        return 0 <= x < w and 0 <= y < h and self.__walls[y][x]

    def _get_neighbour(self, x: int, y: int) -> int:
        result: int = 0

        if not self.__walls[y][x]:
            return 0

        result |= 1 if self._check_wall(x, y - 1) else 0
        result |= 2 if self._check_wall(x + 1, y) else 0
        result |= 4 if self._check_wall(x, y + 1) else 0
        result |= 8 if self._check_wall(x - 1, y) else 0

        return result

    def is_initialized(self) -> bool:
        try:
            return isinstance(self.__maze, Maze)
        except AttributeError:
            return False

    def _create_expanded_maze(self) -> None:
        self.__v_maze_height = self.__maze_rows * 2 + 1
        self.__v_maze_width = self.__maze_columns * 2 + 1

        self.__walls = \
            [[False] * self.__v_maze_width for _ in range(self.__v_maze_height)]

        for y in range(self.__maze_rows):
            for x in range(self.__maze_columns):
                rx: int = x * 2 + 1
                ry: int = y * 2 + 1

                cell = self.__maze[x, y]

                n = cell.hasWall(Direction.NORTH)
                w = cell.hasWall(Direction.WEST)
                e = cell.hasWall(Direction.EAST)
                s = cell.hasWall(Direction.SOUTH)

                self.__walls[ry - 1][rx] |= n
                self.__walls[ry][rx - 1] |= w
                self.__walls[ry][rx + 1] |= e
                self.__walls[ry + 1][rx] |= s

                self.__walls[ry - 1][rx - 1] |= n or w
                self.__walls[ry - 1][rx + 1] |= n or e
                self.__walls[ry + 1][rx - 1] |= s or w
                self.__walls[ry + 1][rx + 1] |= s or e

    def render(self,
               screen: pygame.Surface,
               maze: Maze,
               cell_size: int,
               screen_width: int,
               screen_height: int
               ) -> None:
        for y in range(self.__v_maze_height):
            for x in range(self.__v_maze_width):
                cell_center_x = self.__offset_x + (x + 0.5) * self.__cell_size
                cell_center_y = self.__offset_y + (y + 0.5) * self.__cell_size

                wall_map = self._get_neighbour(x, y)

                if wall_map > 0:
                    sprite_type = self.WALL_MAPPING.get(
                        wall_map,
                        SpriteType.EMPTY_WALL,
                    )
                    sprite = self.__sheet[sprite_type]

                    scaled_sprite = pygame.transform.scale(
                        sprite,
                        (self.__cell_size, self.__cell_size),
                    )
                    rect = scaled_sprite.get_rect(
                        center=(cell_center_x, cell_center_y),
                    )

                    screen.blit(scaled_sprite, rect)
