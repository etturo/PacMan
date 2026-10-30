"""Define the agent module."""

import json
import random

from src.ai.context import PacmanContext
from src.ai.features import extract
from src.entities.ghost_movement import DIRECTIONS
from src.world.cell import Direction


class QAgent:
    """Represent the QAgent component."""

    def __init__(self, weights: dict[str, float] | None = None,
                 training: bool = False) -> None:
        """Initialize the component."""
        self.__weights = weights or {}
        self.__training = training
        self.__epsilon = 0.05
        self.__alpha = 0.2
        self.__gamma = 0.8
        self.__last: tuple[PacmanContext, Direction] | None = None
        self.__last_points = 0
        self.__episodes = 1

    def _is_legal(self, ctx: PacmanContext) -> list[Direction]:
        """Perform the _is_legal operation."""
        return [d for d in DIRECTIONS
                if not ctx.maze[ctx.pacman_pos].hasWall(d)]

    def q(self, ctx: PacmanContext, action: Direction) -> float:
        """Return Q(s, a): the sum of each feature times its weight.

        The higher it is, the better the agent thinks action is in ctx.
        """
        return sum(self.__weights.get(name, 0.0) * value
                   for name, value in extract(ctx, action).items())

    def getAction(self, ctx: PacmanContext) -> Direction:
        """Pick the move with the highest Q, and sometimes a random one.

        While training, first learn from the previous move, then
        remember this one: its reward is known only at the next call.
        """
        if self.__training and self.__last is not None:
            self._update(ctx.points - self.__last_points - 1, ctx)

        legal = self._is_legal(ctx)
        if self.__training and random.random() < self.__epsilon:
            action = random.choice(legal)
        else:
            action = max(legal, key=lambda a: self.q(ctx, a))

        if self.__training:
            self.__last = (ctx, action)
            self.__last_points = ctx.points
        return action

    def _update(self, reward: float, ctx: PacmanContext | None) -> None:
        """Perform the _update operation."""
        if self.__last is None:
            return
        last_ctx, last_action = self.__last
        target = reward
        if ctx is not None:
            target += self.__gamma * max(
                self.q(ctx, a) for a in self._is_legal(ctx))
        delta = target - self.q(last_ctx, last_action)
        for name, value in extract(last_ctx, last_action).items():
            self.__weights[name] = (self.__weights.get(name, 0.0)
                                    + self.__alpha * delta * value)

    def final(self, ctx: PacmanContext, died: bool) -> None:
        """Update the weights for the last state.

        Alpha is decayed over time so that Q-learning converges.
        """
        self._update(ctx.points - self.__last_points - (500 if died else 0),
                     None)
        self.__last = None
        self.__last_points = 0
        self.__episodes += 1
        self.__alpha = 0.2 / (1 + self.__episodes / 20)

    @staticmethod
    def load(path: str) -> 'QAgent':
        """Build an agent from a JSON weights file."""
        with open(path, 'r') as file:
            return QAgent(json.load(file))

    def save(self, path: str) -> None:
        """Save the agent's weights to a JSON file."""
        with open(path, 'w') as file:
            json.dump(self.__weights, file, indent=4)
