from mazegenerator.mazegenerator import Iterator  # type: ignore

from src.world.cell import Direction, Cell


class Maze:
    """Represent the logical structure, dimensions, and grid of a maze."""

    def __getBorder(self, x: int, y: int) -> int:
        return ((Direction.WEST if x == 0 else 0) |
                (Direction.NORTH if y == 0 else 0) |
                (Direction.EAST if x == self.__width - 1 else 0) |
                (Direction.SOUTH if y == self.__height - 1 else 0))

    def __init__(self, size: tuple[int, int], seed: int):
        """Initialize the structural maze object with rows and columns."""
        self.__map: list[list[Cell]] = []
        self.__width: int = size[0]
        self.__height: int = size[1]

        for y in range(self.__height):
            row: list[Cell] = list()
            for x in range(self.__width):
                row.append(Cell(walls=0x0,
                                invicible_walls=self.__getBorder(x, y),))
            self.__map.append(row)

    def getSize(self) -> tuple[int, int]:
        """Returns a tuple containing the width and the height of the maze"""
        return (self.__width, self.__height)

    def __str__(self) -> str:
        output: str = '\n'

        for row in self.__map:
            for cell in row:
                output += f"{cell} "
            output += '\n'

        return output + '\n'

    def setSpecificCell(self, x: int,
                        y: int,
                        walls: int) -> None:
        self.__map[y][x].setCell(walls)

    def __getitem__(self, pos: tuple[int, int]) -> Cell:
        """Read single node positional attributes safely."""
        return self.__map[pos[1]][pos[0]]

    def __iter__(self) -> Iterator:
        return iter(self.__map)

    def getNeighbour(self, x: int, y: int) -> dict[Direction, Cell]:
        """Return neighbouring cells for the cell at (x, y).

        Uses row-major storage `self.__map[y][x]`. Only include neighbours
        that are inside the maze bounds.
        """
        result: dict[Direction, Cell] = {}

        if y > 0:
            result[Direction.NORTH] = self.__map[y - 1][x]

        if y < self.__height - 1:
            result[Direction.SOUTH] = self.__map[y + 1][x]

        if x > 0:
            result[Direction.WEST] = self.__map[y][x - 1]

        if x < self.__width - 1:
            result[Direction.EAST] = self.__map[y][x + 1]

        return result
