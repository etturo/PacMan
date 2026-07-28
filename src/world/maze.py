from src.world.cell import Direction, Cell, InvalidCellOperation, ReadonlyCell


class Maze:
    """Represent the logical structure, dimensions, and grid of a maze."""

    def __getBorder(self, x: int, y: int) -> int:
        return ((Direction.WEST if x == 0 else 0) |
                (Direction.NORTH if y == 0 else 0) |
                (Direction.EAST if x == self.width - 1 else 0) |
                (Direction.SOUTH if y == self.height - 1 else 0))

    def __init__(self, size: tuple[int, int], seed: int):
        """Initialize the structural maze object with rows and columns."""
        self.__map: List[List[Cell]] = []
        self.width: int = size[0]
        self.height: int = size[1]

        for y in range(self.height):
            row: List[Cell] = list()
            for x in range(self.width):
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

    def serialize(self) -> None:
        """Save the maze configuration and solution to the output file."""
        with open(self.__settings['OUTPUT_FILE'], 'w') as file:
            for line in self.__map:
                for cell in line:
                    file.write(cell.Serialize()[2:].upper())
                file.write("\n")

            file.write('\n' + str(self.__settings['ENTRY']))
            file.write('\n' + str(self.__settings['EXIT']) + '\n')

            for direction in self.solution:
                file.write(str(direction))

    def __getitem__(self, pos: Tuple[int, int]) -> ReadonlyCell:
        """Read single node positional attributes safely."""
        x, y = pos
        return ReadonlyCell(self.__map[y][x])

    def addWall(self, x: int, y: int, wall: Direction) -> None:
        """Add a wall in a specific direction for the cell and its neighbor."""
        nx, ny = x + wall.vector[0], y + wall.vector[1]
        if (x >= 0 and x < self.width and y >= 0 and y < self.height and
                nx >= 0 and nx < self.width and ny >= 0 and ny < self.height):
            self.__map[y][x] += wall
            self.__map[ny][nx] += wall.opposite

    def removeWall(self, x: int, y: int, wall: Direction) -> None:
        """Remove a wall in a direction for the cell and its neighbor."""
        nx, ny = x + wall.vector[0], y + wall.vector[1]
        if (x >= 0 and x < self.width and y >= 0 and y < self.height and
                nx >= 0 and nx < self.width and ny >= 0 and ny < self.height):
            self.__map[y][x] -= wall
            self.__map[ny][nx] -= wall.opposite

    def setInvincibleWall(self, x: int, y: int, wall: Direction) -> None:
        """Set a wall as invincible for the given cell and its neighbor."""
        nx, ny = x + wall.vector[0], y + wall.vector[1]
        if (x >= 0 and x < self.width and y >= 0 and y < self.height and
                nx >= 0 and nx < self.width and ny >= 0 and ny < self.height):
            self.__map[y][x].SetInvincible(wall)
            self.__map[ny][nx].SetInvincible(wall.opposite)