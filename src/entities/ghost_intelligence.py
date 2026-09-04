import random

from dataclasses import dataclass

from src.entities.ghost import GhostMode

from src.world.maze import Maze
from src.world.cell import Direction


@dataclass(frozen=True)
class GhostContext:
    """Everything a ghost strategy is allowed to look at.

    Rebuilt from scratch on every decision, hence frozen.
    """
    maze: Maze
    ghost_pos: tuple[int, int]
    ghost_dir: Direction
    pacman_pos: tuple[int, int]
    pacman_dir: Direction
    blinky_pos: tuple[int, int]
    scatter_corner: tuple[int, int]
    mode: GhostMode


def random_target(ctx: GhostContext) -> tuple[int, int]:
    """Aim at a random open neighbour."""
    open_dirs = [
        direction
        for direction in (Direction.NORTH,
                          Direction.EAST,
                          Direction.SOUTH,
                          Direction.WEST)
        if not ctx.maze[ctx.ghost_pos].hasWall(direction)
    ]

    if not open_dirs:
        return ctx.ghost_pos

    forward_dirs = [direction for direction in open_dirs
                    if direction != ctx.ghost_dir.opposite()]

    # Turning back is only allowed when it is the one way out, that is
    # in a dead end: the same rule choose_direction() will follow.
    d_x, d_y = random.choice(forward_dirs or open_dirs).vector()

    return (ctx.ghost_pos[0] + d_x, ctx.ghost_pos[1] + d_y)
