from enum import IntEnum
from typing import Tuple


class InvalidCellOperation(Exception):
    """Exception raised when an invalid operation is attempted on a cell."""
    pass


class Direction(IntEnum):
    """Represent the 4 cardinal directions and their encoded binary flags."""
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    STILL = 0

    def __str__(self) -> str:
        """Return the first letter of the named Enum for printing."""
        return self.name[0]

    def vector(self) -> Tuple[int, int]:
        """Retrieve the 2D coordinate vector associated with the direction."""
        mapping = {
            Direction.NORTH: (0, -1),
            Direction.SOUTH: (0, 1),
            Direction.EAST:  (1, 0),
            Direction.WEST:  (-1, 0),
            Direction.STILL: (0, 0),
        }
        return mapping[self]

    @property
    def opposite(self) -> "Direction":
        """Retrieve the exact logical opposite cardinal direction."""
        mapping = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST:  Direction.WEST,
            Direction.WEST:  Direction.EAST,
            Direction.STILL: Direction.STILL,
        }
        return mapping[self]

    @staticmethod
    def vecToDir(vector: Tuple[int, int]) -> "Direction":
        """Map a 2D unit direction vector back to its Direction enum."""
        return {(0, -1): Direction.NORTH,
                (0, 1):  Direction.SOUTH,
                (1, 0):  Direction.EAST,
                (-1, 0): Direction.WEST,
                (0, 0):  Direction.STILL}[vector]


class Cell:
    """Mutable state structure for an individual node in a 2D grid."""

    def __init__(self, walls: int = 0xF,
                 invicible_walls: int = 0x0) -> None:
        """Initialize the structural state configuring physical walls."""
        self.invincible_walls: int = invicible_walls
        self.walls: int = walls

    def hasWall(self, dir: Direction) -> bool:
        """Calculate whether the cell has a wall blocking a direction."""
        return ((self.walls | self.invincible_walls) & dir) != 0

    def __str__(self) -> str:
        return f"{self.walls:X}"

    def setCell(self, walls: int) -> None:
        self.walls = walls
