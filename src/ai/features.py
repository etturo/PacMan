from src.ai.context import PacmanContext
from src.entities.ghost_movement import bfs_distances, GhostMode
from src.world.cell import Direction


def next_cell(ctx: PacmanContext, action: Direction) -> tuple[int, int]:
    """Returns the cell that results from taking action."""
    d_x, d_y = action.vector()
    return ctx.pacman_pos[0] + d_x, ctx.pacman_pos[1] + d_y


def ghosts_1_step(ctx: PacmanContext,
                  dist: dict[tuple[int, int], int]) -> float:
    """Count the dangerous ghosts one step away from the next cell.

    A ghost is dangerous in CHASE or SCATTER mode, and near when it
    stands on the next cell or on a cell next to it (dist <= 1).
    """
    count = 0.0
    for pos, mode in ctx.ghosts:
        is_dangerous = mode in (GhostMode.CHASE, GhostMode.SCATTER)
        is_near = pos in dist and dist[pos] <= 1
        if is_dangerous and is_near:
            count += 1
    return count


def closest_food(ctx: PacmanContext,
                 dist: dict[tuple[int, int], int]) -> float:
    """Calculates the distance to the closest food using the BFS algorithm."""
    steps = [dist[cell] for cell in ctx.food if cell in dist]
    if not steps:
        return 0.0
    width, height = ctx.maze.getSize()
    return min(steps) / (width * height)


def extract(ctx: PacmanContext, action: Direction) -> dict[str, float]:
    """Describe with numbers what happens if Pacman takes action.

    In features, the first number is the bias.
    The second is the number of dangerous ghosts (i.e. in CHASE or SCATTER
    mode) that are 1 step away.
    The third is 1 if the next cell is food AND there is no danger,
    0 otherwise.
    The fourth is the distance to the closest food divided by the total
    area, so the feature is always between 0 and 1."""
    nxt = next_cell(ctx, action)
    dist = bfs_distances(ctx.maze, nxt)

    features = {"bias": 1.0, "ghosts-1-step": ghosts_1_step(ctx, dist)}
    if features["ghosts-1-step"] == 0 and nxt in ctx.food:
        features["eats-food"] = 1.0
    else:
        features["eats-food"] = 0.0
    features["closest-food"] = closest_food(ctx, dist)

    for name in features:
        features[name] /= 10
    return features
