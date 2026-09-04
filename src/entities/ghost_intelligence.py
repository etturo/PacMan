import random
from collections import deque

from dataclasses import dataclass
from enum import Enum, auto

from src.world.maze import Maze
from src.world.cell import Direction


UNREACHABLE = 1 << 30
# DIRECTIONS = (Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST)


class GhostMode(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()


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


def bfs_distances(maze: Maze,
                  source: tuple[int, int]) -> dict[tuple[int, int], int]:
    """BFS to get distance from source to target.

    It will be run from the target to get all the distances in one
    pass.
    """
    width, height = maze.getSize()
    distances: dict[tuple[int, int], int] = {source: 0}
    queue: deque[tuple[int, int]] = deque([source])

    while queue:
        x, y = queue.popleft()
        cell = maze[(x, y)]
        for direction in Direction:
            if cell.hasWall(direction):
                continue

            dx, dy = direction.vector()
            neighbour = (x + dx, y + dy)

            if not (0 <= neighbour[0] < width and 0 <= neighbour[1] < height):
                continue
            if neighbour in distances:
                continue

            distances[neighbour] = distances[(x, y)] + 1
            queue.append(neighbour)
    return distances


def bound_target(maze: Maze, cell: tuple[int, int]) -> tuple[int, int]:
    """If the target is outside of the maze, bound it inside."""
    width, height = maze.getSize()
    return (max(0, min(width - 1, cell[0])),
            max(0, min(height - 1, cell[1])))


def choose_direction(maze: Maze,
                     ghost_pos: tuple[int, int],
                     current_dir: Direction,
                     target: tuple[int, int]) -> Direction:
    """Closest direction to target.

    U-turn is permitted only if it's only legal move.
    If distance is the same, the original order is preserved.
    """
    # TODO: verificare che si voglia lascaire l'ordine delle celle come
    #  specificato in cell/Direction, perché non è quello originale
    distances = bfs_distances(maze, bound_target(maze, target))
    cell = maze[ghost_pos]
    banned = current_dir.opposite()

    candidates: list[tuple[int, Direction]] = []
    fallback: list[Direction] = []

    for direction in Direction:
        # STILL never has a wall, so without this it would always be a
        # candidate and would win every tie against the real u-turn.
        if direction == Direction.STILL or cell.hasWall(direction):
            continue

        d_x, d_y = direction.vector()
        neighbour = (ghost_pos[0] + d_x, ghost_pos[1] + d_y)

        if direction == banned:
            fallback.append(direction)
            continue

        candidates.append((distances.get(neighbour, UNREACHABLE), direction))

    if not candidates:
        return fallback[0] if fallback else Direction.STILL

    return min(candidates, key=lambda pair: pair[0])[1]


def blinky_strategy(ctx: GhostContext) -> tuple[int, int]:
    """Blinky's strategy: always follows PacMan"""
    return ctx.pacman_pos
