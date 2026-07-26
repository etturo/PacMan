from abc import ABC


class Entity(ABC):
    def update(self) -> None:
        ...
