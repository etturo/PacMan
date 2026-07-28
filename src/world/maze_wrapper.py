from mazegenerator import MazeGenerator
from src.world.maze import Maze


class MazeWrapper:
    def __init__(self) -> None:
        self.__generator: MazeGenerator
        self.__maze_list: list[list[int]] = list()
        self.__maze: Maze

    def generate(self, size: tuple[int, int], seed: int) -> None:
        self._size: tuple[int, int] = size
        self._seed: int = seed

        try:
            self.__generator = MazeGenerator(
                size=size,
                perfect=False,
                entry_cell=(0, 0),
                exit_cell=(1, 1),
                seed=seed
            )

            self.__generator.generate()

            self.__maze_list = self.__generator.maze

            self.__load_maze()

        except Exception as e:
            print(e)

    def __str__(self) -> str:
        output: str = '\n'

        for row in self.__maze:
            for cell in row:
                output += f"{cell:X} "
            output += '\n'

        return output + '\n'

    @property
    def maze(self) -> Maze:
        return self.__maze

    def __load_maze(self) -> Maze:
        self.__maze  = Maze(self._size, self._seed)

        for y, row in enumerate(self.__maze_list):
            for x, cell in enumerate(row):
                self.__maze.setSpecificCell(x, y, cell)
