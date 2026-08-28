import pygame

from abc import ABC

from src.world.maze import Direction

class Entity(ABC):
    def __init__(
        self,
        initial_position: tuple[int, int],
        size: int,
        speed: float = 4.0
    ) -> None:
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
        return self._current_cell

    def get_visual_pos(self) -> tuple[float, float]:
        c_x, c_y = self._current_cell
        t_x, t_y = self._target_cell

        v_x = c_x + (t_x - c_x) * self._lerp_progress
        v_y = c_y + (t_y - c_y) * self._lerp_progress

        return v_x, v_y

    def isAlive(self) -> bool:
        return self._is_alive

    def getDir(self) -> Direction:
        return self._current_direction

    def getPos(self) -> tuple[int, int]:
        return self._current_cell

    def getCurrentDirection(self) -> Direction:
        return self._current_direction

    def getQueuedDirection(self) -> Direction:
        return self._queued_direction

    def setQueueDirection(self, new_dir: Direction) -> None:
        self._queued_direction = new_dir

    def setSpeed(self, new_speed: float) -> None:
        self._speed = new_speed

    def resetPosition(self) -> None:
        self._current_cell = self._initial_cell

    def isMoving(self) -> bool:
        return self._current_cell != self._target_cell

    def moveTo(self, target: tuple[int, int], taken_dir: Direction) -> None:
        if not self._is_alive:
            return
        self._target_cell = target
        self._lerp_progress = 0.0
        self._current_direction = taken_dir

    def update(self, dt: float) -> None:
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
        rect = self._surface.get_rect(center=screen_pos)
        screen.blit(self._surface, rect)

    def die(self) -> None:
        self._is_alive = False
