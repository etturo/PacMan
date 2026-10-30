"""Define the maze wrapper module."""

import sys
import os

import pygame

from functools import wraps
from typing import Callable, Any

from mazegenerator import MazeGenerator

from src.world.maze import Maze


def suppress_prints(func: Callable[..., Any]) -> Callable[..., Any]:
    """Suppress output written while calling the wrapped function."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Perform the wrapper operation."""
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
    """Represent the MazeWrapper component."""

    def __init__(self) -> None:
        """Initialize the component."""
        self.__generator: MazeGenerator
        self.__maze_list: list[list[int]] = list()
        self.__maze: Maze

    @suppress_prints
    def generate(self, size: tuple[int, int], seed: int) -> None:
        """Perform the generate operation."""
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

            self.__generator.generate(seed)

            self.__maze_list = self.__generator.maze

            self.__load_maze()

        except Exception:
            print("Maze Generator failed.")
            pygame.quit()

    def __str__(self) -> str:
        """Implement the __str__ operation."""
        output: str = '\n'

        for row in self.__maze:
            for cell in row:
                output += f"{cell:X} "
            output += '\n'

        return output + '\n'

    @property
    def maze(self) -> Maze:
        """Perform the maze operation."""
        return self.__maze

    def __load_maze(self) -> None:
        """Perform the __load_maze operation."""
        self.__maze = Maze(self._size, self._seed)

        for y, row in enumerate(self.__maze_list):
            for x, cell in enumerate(row):
                self.__maze.setSpecificCell(x, y, cell)
