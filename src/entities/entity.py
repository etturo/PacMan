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
        self._target_cell: tuple[int, int] = initial_position
        self._lerp_progress: float = 0.0
        self._speed: float = speed
        self._surface = pygame.Surface((size, size))
        
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

    def getDir(self) -> Direction:
        return self._current_direction

    def get_current_direction(self) -> Direction:
        return self._current_direction

    def get_queued_direction(self) -> Direction:
        return self._queued_direction

    def queue_direction(self, new_dir: Direction) -> None:
        self._queued_direction = new_dir

    def is_moving(self) -> bool:
        return self._current_cell != self._target_cell

    def move_to(self, target: tuple[int, int], taken_dir: Direction) -> None:
        self._target_cell = target
        self._lerp_progress = 0.0
        self._current_direction = taken_dir

    def update(self, dt: float) -> None:
        if self.is_moving():
            self._lerp_progress += self._speed * dt
            
            if self._lerp_progress >= 1.0:
                self._current_cell = self._target_cell
                self._lerp_progress = 0.0

    def render(
            self,
            screen: pygame.Surface,
            screen_pos: tuple[float, float]
            ) -> None:
        rect = self._surface.get_rect(center=screen_pos)
        screen.blit(self._surface, rect)
