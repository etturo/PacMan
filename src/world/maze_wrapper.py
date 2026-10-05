import sys
import os

from functools import wraps
from typing import Callable, Any

from mazegenerator import MazeGenerator  # type: ignore

from src.world.maze import Maze


def suppress_prints(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if sys.stdout is None or sys.stderr is None:
            return func(*args, **kwargs)

        sys.stdout.flush()
        sys.stderr.flush()

        original_stdout_fd = os.dup(1)
        original_stderr_fd = os.dup(2)

        devnull_fd = os.open(os.devnull, os.O_WRONLY)

        os.dup2(devnull_fd, 1)
        os.dup2(devnull_fd, 2)

        try:
            return func(*args, **kwargs)
        finally:
            sys.stdout.flush()
            sys.stderr.flush()

            os.dup2(original_stdout_fd, 1)
            os.dup2(original_stderr_fd, 2)

            os.close(original_stdout_fd)
            os.close(original_stderr_fd)
            os.close(devnull_fd)

    return wrapper


class MazeWrapper:
    def __init__(self) -> None:
        self.__generator: MazeGenerator
        self.__maze_list: list[list[int]] = list()
        self.__maze: Maze

    @suppress_prints
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
            ...

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

    def __load_maze(self) -> None:
        self.__maze = Maze(self._size, self._seed)

        for y, row in enumerate(self.__maze_list):
            for x, cell in enumerate(row):
                self.__maze.setSpecificCell(x, y, cell)
