from dataclasses import dataclass

from src.entities.ghost_movement import GhostMode
from src.world.maze import Maze


@dataclass(frozen=True)
class PacmanContext:
    """Everything the AI player is allowed to look at.

    Rebuilt from scratch on every decision, hence frozen.
    ghosts hold only the released ones, food the cells of every
    pacgum and super pacgum still alive.
    fright_left is the seconds of blue left, shared by every
    frightened ghost; 0 when none is.
    pacman_speed in cells per second
    ghost_speed is the speed of the dangerous ghosts, cells per second.
    """
    maze: Maze
    pacman_pos: tuple[int, int]
    ghosts: list[tuple[tuple[int, int], GhostMode]]
    fright_left: float
    pacman_speed: float
    ghost_speed: float
    food: set[tuple[int, int]]
    points: int
