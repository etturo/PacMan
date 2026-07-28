from typing import List, Tuple

from src.world.cell import Direction, Cell, ReadonlyCell


class Maze:
    """Represent the logical structure, dimensions, and grid of a maze."""

    def __getBorder(self, x: int, y: int) -> int:
        return ((Direction.WEST if x == 0 else 0) |
                (Direction.NORTH if y == 0 else 0) |
                (Direction.EAST if x == self.__width - 1 else 0) |
                (Direction.SOUTH if y == self.__height - 1 else 0))

    def __init__(self, size: tuple[int, int], seed: int):
        """Initialize the structural maze object with rows and columns."""
        self.__map: List[List[Cell]] = []
        self.__width: int = size[0]
        self.__height: int = size[1]

        for y in range(self.__height):
            row: List[Cell] = list()
            for x in range(self.__width):
                row.append(Cell(walls=0x0,
                                invicible_walls=self.__getBorder(x, y),))
            self.__map.append(row)

    def __str__(self) -> str:
        output: str = '\n'

        for row in self.__map:
            for cell in row:
                output += f"{cell} "
            output += '\n'

        return output + '\n'

    def setSpecificCell(self, x, y, walls) -> None:
        self.__map[y][x].setCell(walls)

    def __getitem__(self, pos: Tuple[int, int]) -> ReadonlyCell:
        """Read single node positional attributes safely."""
        x, y = pos
        return ReadonlyCell(self.__map[y][x])

    def addWall(self, x: int, y: int, wall: Direction) -> None:
        """Add a wall in a specific direction for the cell and its neighbor."""
        nx, ny = x + wall.vector[0], y + wall.vector[1]
        if (x >= 0 and x < self.__width and y >= 0 and y < self.__height and
                nx >= 0 and nx < self.__width and ny >= 0 and ny < self.__height):
            self.__map[y][x] += wall
            self.__map[ny][nx] += wall.opposite

    def removeWall(self, x: int, y: int, wall: Direction) -> None:
        """Remove a wall in a direction for the cell and its neighbor."""
        nx, ny = x + wall.vector[0], y + wall.vector[1]
        if (x >= 0 and x < self.__width and y >= 0 and y < self.__height and
                nx >= 0 and nx < self.__width and ny >= 0 and ny < self.__height):
            self.__map[y][x] -= wall
            self.__map[ny][nx] -= wall.opposite

    def setInvincibleWall(self, x: int, y: int, wall: Direction) -> None:
        """Set a wall as invincible for the given cell and its neighbor."""
        nx, ny = x + wall.vector[0], y + wall.vector[1]
        if (x >= 0 and x < self.__width and y >= 0 and y < self.__height and
                nx >= 0 and nx < self.__width and ny >= 0 and ny < self.__height):
            self.__map[y][x].SetInvincible(wall)
            self.__map[ny][nx].SetInvincible(wall.opposite)