"""Define the entity module."""

import pygame

from abc import ABC

from src.world.cell import Direction


class Entity(ABC):
    """Represent the Entity component."""

    def __init__(
        self,
        initial_position: tuple[int, int],
        size: float,
        speed: float = 4.0
    ) -> None:
        """Initialize the component."""
        self._current_cell: tuple[int, int] = initial_position
        self._initial_cell = initial_position
        self._target_cell: tuple[int, int] = initial_position
        self._lerp_progress: float = 0.0
        self._speed: float = speed
        self._surface = pygame.Surface((size, size))
        self._is_alive: bool = True
        self._current_direction: Direction = Direction.STILL
        self._queued_direction: Direction = Direction.STILL

    def getCurrentCell(self) -> tuple[int, int]:
        """Perform the getCurrentCell operation."""
        return self._current_cell

    def getVisualPos(self) -> tuple[float, float]:
        """Perform the getVisualPos operation."""
        c_x, c_y = self._current_cell
        t_x, t_y = self._target_cell

        v_x = c_x + (t_x - c_x) * self._lerp_progress
        v_y = c_y + (t_y - c_y) * self._lerp_progress

        return v_x, v_y

    def getVisualCell(self) -> tuple[int, int]:
        """Get the cell the entity's center is in during a move."""
        v_x, v_y = self.getVisualPos()
        return round(v_x), round(v_y)

    def isAlive(self) -> bool:
        """Perform the isAlive operation."""
        return self._is_alive

    def getDir(self) -> Direction:
        """Perform the getDir operation."""
        return self._current_direction

    def getPos(self) -> tuple[int, int]:
        """Perform the getPos operation."""
        return self._current_cell

    def getCurrentDirection(self) -> Direction:
        """Perform the getCurrentDirection operation."""
        return self._current_direction

    def getQueuedDirection(self) -> Direction:
        """Perform the getQueuedDirection operation."""
        return self._queued_direction

    def setQueueDirection(self, new_dir: Direction) -> None:
        """Perform the setQueueDirection operation."""
        self._queued_direction = new_dir

    def setSpeed(self, new_speed: float) -> None:
        """Perform the setSpeed operation."""
        self._speed = new_speed

    def getSpeed(self) -> float:
        """Perform the getSpeed operation."""
        return self._speed

    def resetPosition(self) -> None:
        """Perform the resetPosition operation."""
        self._current_cell = self._initial_cell
        self._target_cell = self._initial_cell

    def isMoving(self) -> bool:
        """Perform the isMoving operation."""
        return self._current_cell != self._target_cell

    def moveTo(self, target: tuple[int, int], taken_dir: Direction) -> None:
        """Perform the moveTo operation."""
        if not self._is_alive:
            return
        self._target_cell = target
        self._lerp_progress = 0.0
        self._current_direction = taken_dir

    def update(self, dt: float) -> None:
        """Perform the update operation."""
        if not self._is_alive:
            return
        if self.isMoving():
            self._lerp_progress += self._speed * dt

            if self._lerp_progress >= 1.0:
                self._current_cell = self._target_cell
                self._lerp_progress = 0.0

    def render(
            self,
            screen: pygame.Surface,
            screen_pos: tuple[float, float],
            dt: float,
            ) -> None:
        """Perform the render operation."""
        rect = self._surface.get_rect(center=screen_pos)
        screen.blit(self._surface, rect)

    def die(self) -> None:
        """Perform the die operation."""
        self._is_alive = False
