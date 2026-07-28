from mazegenerator import MazeGenerator
from enum import IntEnum
from typing import Tuple
from src.world.maze import Maze
from src.world.cell import Cell



class MazeWrapper:
    def __init__(self) -> None:
        self._generator: MazeGenerator
        self._maze_list: list[list[int]] = list()
        self._maze: Maze

    def generate(self, size: tuple[int, int], seed: int) -> None:
        self._size: tuple[int, int] = size
        self._seed: int = seed

        try:
            self._generator = MazeGenerator(
                size=size,
                perfect=False,
                entry_cell=(0, 0),
                exit_cell=(1, 1),
                seed=seed
            )

            self._generator.generate()

            self._maze_list = self._generator.maze

            self._load_maze()

        except Exception as e:
            print(e)

    def __str__(self) -> str:
        output: str = '\n'

        for row in self._maze:
            for cell in row:
                output += f"{cell:X} "
            output += '\n'

        return output + '\n'

    @property
    def maze(self) -> Maze:
        return self._maze

    def _load_maze(self) -> Maze:
        self._maze  = Maze(self._size, self._seed)

        for y, row in enumerate(self._maze_list):
            for x, cell in enumerate(row):
                self._maze.setSpecificCell(x, y, cell)
