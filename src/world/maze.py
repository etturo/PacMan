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
        x, y = pos
        return self.__map[y][x]

    def __iter__(self) -> Iterator:
        return iter(self.__map)
