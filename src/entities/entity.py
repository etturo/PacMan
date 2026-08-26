import pygame

from abc import ABC

from src.world.maze import Direction


class Entity(ABC):
    def __init__(
        self,
        initial_position: tuple[float, float],
        size: int,
        speed: float
        ) -> None:
        self._position: tuple[float, float] = initial_position
        self._surface = pygame.Surface((size, size))
        self._direction: Direction = Direction.STILL
        self._speed = speed

    def getPos(self) -> tuple[float, float]:
        return self._position

    def getSpeed(self) -> float:
        return self._speed

    def getDir(self) -> Direction:
        return self._direction

    def setDir(self, new_dir: Direction) -> Direction:
        self._direction = new_dir

    def update(self, new_pos: tuple[float, float]) -> None:
        self._position = new_pos
        print(self._position)

    def render(
            self,
            screen: pygame.Surface,
            screen_pos: tuple[float, float]
            ) -> None:
        rect = self._surface.get_rect(center=screen_pos)

        screen.blit(self._surface, rect)
