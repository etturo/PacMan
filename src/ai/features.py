"""Define the features module."""

from src.ai.context import PacmanContext
from src.entities.ghost_movement import bfs_distances, GhostMode
from src.world.cell import Direction


def next_cell(ctx: PacmanContext, action: Direction) -> tuple[int, int]:
    """Return the cell that results from taking action."""
    d_x, d_y = action.vector()
    return ctx.pacman_pos[0] + d_x, ctx.pacman_pos[1] + d_y


def is_dangerous(ctx: PacmanContext, mode: GhostMode, steps: int) -> bool:
    """Determine whether a ghost n_steps away can kill Pacman."""
    return (mode in (GhostMode.CHASE, GhostMode.SCATTER)
            or (mode == GhostMode.FRIGHTENED
                and not is_reachable(ctx, steps)))


# def danger(ctx: PacmanContext, dist: dict[tuple[int, int], int]) -> float:
#     """Add up how close the dangerous ghosts within DANGER_RADIUS steps
#     of the next cell are: each counts 1 on the next cell, falling
#     to 0 at DANGER_RADIUS steps."""
#     total = 0.0
#     danger_radius = 5
#     for pos, mode in ctx.ghosts:
#         if pos not in dist:
#             continue
#         d = dist[pos]
#         if d < danger_radius and is_dangerous(ctx, mode, d):
#             total += (danger_radius - d) / danger_radius
#     return total


def ghosts_1_step(ctx: PacmanContext,
                  dist: dict[tuple[int, int], int]) -> float:
    """Count the dangerous ghosts one step away from the next cell.

    Dangerous as in is_dangerous, near when the ghost stands on the
    next cell or on a cell next to it (dist <= 1).
    """
    count = 0.0
    for pos, mode in ctx.ghosts:
        is_near = pos in dist and dist[pos] <= 1
        if is_near and is_dangerous(ctx, mode, dist[pos]):
            count += 1
    return count


def closest_food(ctx: PacmanContext,
                 dist: dict[tuple[int, int], int]) -> float:
    """Calculate the distance to the closest food using BFS."""
    steps = [dist[cell] for cell in ctx.food if cell in dist]
    if not steps:
        return 0.0
    width, height = ctx.maze.getSize()
    return min(steps) / (width * height)


def is_reachable(ctx: PacmanContext, steps: int) -> bool:
    """Determine whether Pacman reaches the target before frightened ends.

    Pacman goes to the next cell and then takes the given number of steps.
    gets there before the frightened mode is over.
    """
    return (steps + 1) / ctx.pacman_speed < ctx.fright_left


def scared_steps(ctx: PacmanContext,
                 dist: dict[tuple[int, int], int]) -> list[int]:
    """Count steps from the next cell to every reachable blue ghost."""
    return [dist[pos] for pos, mode in ctx.ghosts
            if mode == GhostMode.FRIGHTENED and pos in dist
            and is_reachable(ctx, dist[pos])]


def eat_ghost(ctx: PacmanContext, dist: dict[tuple[int, int], int]) -> float:
    """Count the blue ghosts in reach one step away from the next cell."""
    return float(sum(1 for steps in scared_steps(ctx, dist) if steps <= 1))


def closest_scared(ctx: PacmanContext,
                   dist: dict[tuple[int, int], int]) -> float:
    """Calculate how close the nearest reachable blue ghost is.

    The value is near 1 next to it,
    near 0 when it is barely in reach, 0 when there is none.
    """
    steps = scared_steps(ctx, dist)
    if not steps:
        return 0.0
    reach = ctx.fright_left * ctx.pacman_speed
    return 1 - min(steps) / reach


def extract(ctx: PacmanContext, action: Direction) -> dict[str, float]:
    """Describe with numbers what happens if Pacman takes action.

    In features, the first number is the bias.
    The second is the number of dangerous ghosts (see is_dangerous)
    that are 1 step away.
    The third is 1 if the next cell is food AND there is no danger,
    0 otherwise.
    The fourth is the distance to the closest food divided by the total
    area, so the feature is always between 0 and 1.
    The fifth is the number of blue ghosts in reach one step away.
    The sixth is how close the nearest blue ghost in reach is: near 1
    next to it, 0 when there is none.
    """
    nxt = next_cell(ctx, action)
    dist = bfs_distances(ctx.maze, nxt)

    features = {"bias": 1.0, "ghosts-1-step": ghosts_1_step(ctx, dist)}
    if features["ghosts-1-step"] == 0 and nxt in ctx.food:
        features["eats-food"] = 1.0
    else:
        features["eats-food"] = 0.0
    features["closest-food"] = closest_food(ctx, dist)
    features["eats-ghost"] = eat_ghost(ctx, dist)
    features["closest-scared"] = closest_scared(ctx, dist)

    for name in features:
        features[name] /= 10
    return features
