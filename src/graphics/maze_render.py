import pygame

from src.graphics.sprite_sheet import SpriteSheet, SpriteType
from src.world.cell import Direction
from src.world.maze import Maze


class MazeRender:
    __screen: pygame.Surface
    __sheet: SpriteSheet
    __screen_width: int
    __screen_height: int
    __maze: Maze
    __maze_columns: int
    __maze_rows: int
    __cell_size: int
    __offset_x: float
    __offset_y: float
    __v_maze_width: int
    __v_maze_height: int
    __walls: list[list[bool]]

    __WALL_MAPPING: dict[int, SpriteType] = {
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

    @classmethod
    def _init(cls,
               screen: pygame.Surface,
               sheet: SpriteSheet,
               maze: Maze,
               cell_size: int,
               screen_width: int,
               screen_height: int
               ) -> None:
        cls.__screen = screen
        cls.__sheet = sheet
        cls.__screen_width = screen_width
        cls.__screen_height = screen_height

        cls.__maze = maze
        cls.__maze_columns = maze.getSize()[0]
        cls.__maze_rows = maze.getSize()[1]

        cls._create_expanded_maze()

        cls.__cell_size = cell_size
        cls.__offset_x = (
            cls.__screen_width - (cls.__cell_size * cls.__v_maze_width)
        ) / 2
        cls.__offset_y = (
            cls.__screen_height - (cls.__cell_size * cls.__v_maze_height)
        ) / 2

    @classmethod
    def _check_wall(cls, x: int, y: int) -> bool:
        h = len(cls.__walls)
        w = len(cls.__walls[0]) if h > 0 else 0
        return 0 <= x < w and 0 <= y < h and cls.__walls[y][x]

    @classmethod
    def _get_neighbour(cls, x: int, y: int) -> int:
        result: int = 0

        if not cls.__walls[y][x]:
            return 0

        result |= 1 if cls._check_wall(x, y - 1) else 0
        result |= 2 if cls._check_wall(x + 1, y) else 0
        result |= 4 if cls._check_wall(x, y + 1) else 0
        result |= 8 if cls._check_wall(x - 1, y) else 0

        return result

    @classmethod
    def _create_expanded_maze(cls) -> None:
        cls.__v_maze_height = cls.__maze_rows * 2 + 1
        cls.__v_maze_width = cls.__maze_columns * 2 + 1

        cls.__walls = [[False] * cls.__v_maze_width for _ in range(cls.__v_maze_height)]

        for y in range(cls.__maze_rows):
            for x in range(cls.__maze_columns):
                rx: int = x * 2 + 1
                ry: int = y * 2 + 1

                cell = cls.__maze[x, y]

                n = cell.hasWall(Direction.NORTH)
                w = cell.hasWall(Direction.WEST)
                e = cell.hasWall(Direction.EAST)
                s = cell.hasWall(Direction.SOUTH)

                cls.__walls[ry - 1][rx] |= n
                cls.__walls[ry][rx - 1] |= w
                cls.__walls[ry][rx + 1] |= e
                cls.__walls[ry + 1][rx] |= s

                cls.__walls[ry - 1][rx - 1] |= n or w
                cls.__walls[ry - 1][rx + 1] |= n or e
                cls.__walls[ry + 1][rx - 1] |= s or w
                cls.__walls[ry + 1][rx + 1] |= s or e

    @classmethod
    def render(cls,
               screen: pygame.Surface,
               sheet: SpriteSheet,
               maze: Maze,
               cell_size: int,
               screen_width: int,
               screen_height: int
               ) -> None:

        cls._init(
            screen=screen,
            sheet=sheet,
            maze=maze,
            cell_size=cell_size,
            screen_width=screen_width,
            screen_height=screen_height
            )

        for y in range(cls.__v_maze_height):
            for x in range(cls.__v_maze_width):
                cell_center_x = cls.__offset_x + (x + 0.5) * cls.__cell_size
                cell_center_y = cls.__offset_y + (y + 0.5) * cls.__cell_size

                wall_map = cls._get_neighbour(x, y)

                if wall_map > 0:
                    sprite_type = cls.__WALL_MAPPING.get(
                        wall_map,
                        SpriteType.EMPTY_WALL,
                    )
                    sprite = cls.__sheet[sprite_type]

                    scaled_sprite = pygame.transform.scale(
                        sprite,
                        (cls.__cell_size, cls.__cell_size),
                    )
                    rect = scaled_sprite.get_rect(
                        center=(cell_center_x, cell_center_y),
                    )

                    cls.__screen.blit(scaled_sprite, rect)
