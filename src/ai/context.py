from dataclasses import dataclass

from src.entities.ghost_movement import GhostMode
from src.world.maze import Maze


@dataclass(frozen=True)
class PacmanContext:
    """Everything the AI player is allowed to look at.

    Rebuilt from scratch on every decision, hence frozen.
    ghosts holds only the released ones, food the cells of every
    pacgum and super pacgum still alive.
    """
    maze: Maze
    pacman_pos: tuple[int, int]
    ghosts: list[tuple[tuple[int, int], GhostMode]]
    food: set[tuple[int, int]]
    points: int
