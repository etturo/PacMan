import random
from collections import deque

from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple

from src.world.maze import Maze
from src.world.cell import Direction


UNREACHABLE = 1 << 30
# Original order
DIRECTIONS = (Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST)


class GhostMode(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()
    EATEN = auto()


class SchedulePhase(NamedTuple):
    mode: GhostMode
    duration: float


class GhostModeController:
    """Global timer for scatter/chase for all ghosts."""

    SCHEDULE: tuple[SchedulePhase, ...] = (
        SchedulePhase(GhostMode.SCATTER,  7.0),
        SchedulePhase(GhostMode.CHASE,   20.0),
        SchedulePhase(GhostMode.SCATTER,  7.0),
        SchedulePhase(GhostMode.CHASE,   20.0),
        SchedulePhase(GhostMode.SCATTER,  5.0),
        SchedulePhase(GhostMode.CHASE,   20.0),
        SchedulePhase(GhostMode.SCATTER,  5.0),
        SchedulePhase(GhostMode.CHASE,   float('inf')),
    )

    def __init__(self) -> None:
        self.__schedule = self.SCHEDULE
        self.__phase: int = 0
        self.__elapsed: float = 0.0
        self.__paused: bool = False

    def getMode(self) -> GhostMode:
        """Get the current ghost mode."""
        return self.__schedule[self.__phase].mode

    def setPaused(self, paused: bool) -> None:
        """Set the ghost mode to pause."""
        self.__paused = paused

    def update(self, dt: float) -> bool:
        """Update the ghost's timer.

        Returns: True if the mode changes, False otherwise."""
        if self.__paused or self.__phase >= len(self.__schedule) - 1:
            return False

        self.__elapsed += dt
        if self.__elapsed < self.__schedule[self.__phase].duration:
            return False
        self.__elapsed = 0.0
        self.__phase += 1
        return True

    def reset(self, level: int = 0) -> None:
        """Resets ghosts' states on PacMan's death or on a new level.

        Every level makes the scatter phases 3 seconds shorter."""
        self.__schedule = tuple(
            phase._replace(duration=max(0.0, phase.duration - 3 * level))
            if phase.mode == GhostMode.SCATTER else phase
            for phase in self.SCHEDULE)
        self.__elapsed = 0.0
        self.__phase = 0
        self.__paused = False


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
        direction for direction in DIRECTIONS
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
        for direction in DIRECTIONS:
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
    If distance is the same, the DIRECTIONS order wins.
    """
    distances = bfs_distances(maze, bound_target(maze, target))
    cell = maze[ghost_pos]
    banned = current_dir.opposite()

    candidates: list[tuple[int, Direction]] = []
    fallback: list[Direction] = []

    for direction in DIRECTIONS:
        if cell.hasWall(direction):
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


def _ahead_of_pacman(ctx: GhostContext, tiles: int) -> tuple[int, int]:
    """Cell `tiles` ahead of PacMan.

    Facing north it also goes `tiles` west: the overflow bug of the original
    is kept on purpose.
    """
    d_x, d_y = ctx.pacman_dir.vector()
    if ctx.pacman_dir == Direction.NORTH:
        d_x = -1
    return ctx.pacman_pos[0] + d_x * tiles, ctx.pacman_pos[1] + d_y * tiles


def blinky_strategy(ctx: GhostContext) -> tuple[int, int]:
    """Blinky's strategy: always follows PacMan"""
    return ctx.pacman_pos


def pinky_strategy(ctx: GhostContext) -> tuple[int, int]:
    """Pinky's strategy: 4 cells ahead of PacMan."""
    return _ahead_of_pacman(ctx, 4)


def inky_strategy(ctx: GhostContext) -> tuple[int, int]:
    """Inky's strategy: the vector from Blinky to 2 cells ahead of
    PacMan, doubled."""
    p_x, p_y = _ahead_of_pacman(ctx, 2)
    b_x, b_y = ctx.blinky_pos
    return (2 * p_x - b_x, 2 * p_y - b_y)


def clyde_strategy(ctx: GhostContext) -> tuple[int, int]:
    """Clyde's strategy: follows PacMan from afar, runs back to his
    corner once closer than 8 cells."""
    g_x, g_y = ctx.ghost_pos
    p_x, p_y = ctx.pacman_pos
    if (g_x - p_x) ** 2 + (g_y - p_y) ** 2 > 8 ** 2:
        return ctx.pacman_pos
    return ctx.scatter_corner
