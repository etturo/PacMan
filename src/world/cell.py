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

    def __str__(self) -> str:
        """Return the first letter of the named Enum for printing."""
        return self.name[0]

    @property
    def vector(self) -> Tuple[int, int]:
        """Retrieve the 2D coordinate vector associated with the direction."""
        mapping = {
            Direction.NORTH: (0, -1),
            Direction.SOUTH: (0, 1),
            Direction.EAST:  (1, 0),
            Direction.WEST:  (-1, 0),
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
        }
        return mapping[self]

    @staticmethod
    def vecToDir(vector: Tuple[int, int]) -> "Direction":
        """Map a 2D unit direction vector back to its Direction enum."""
        return {(0, -1): Direction.NORTH,
                (0, 1): Direction.SOUTH,
                (1, 0): Direction.EAST,
                (-1, 0): Direction.WEST}[vector]


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

    def __setitem__(self, d: Direction, value: bool) -> None:
        """Manually inject or override a wall into a specific direction."""
        if not value and self.invincible_walls & d != 0:
            raise InvalidCellOperation("Tried deleting and invincible wall")
        self.walls = (self.walls | d) if value else (self.walls & ~d)

    def __iadd__(self, dir: Direction) -> "Cell":
        """Build a basic mutable wall inside the cell along the given dir."""
        self.walls |= dir
        return self

    def __isub__(self, dir: Direction) -> "Cell":
        """Remove a standard movable wall boundary along the orientation."""
        if self.invincible_walls & dir != 0:
            raise InvalidCellOperation("Tried deleting and invincible wall")
        self.walls &= ~dir
        return self

    def __str__(self) -> str:
        return f"{self.walls:X}"

    @staticmethod
    def addWall(walls: int, dir: Direction) -> int:
        """Provide a logical operation bit masking by adding a flag."""
        return walls | dir

    def setCell(self, walls: int) -> None:
        self.walls = walls

    def setInvincible(self, dir: int) -> None:
        """Permanently block a static physical wall over this node."""
        self.invincible_walls |= dir


class ReadonlyCell:
    """Immutable representation structure for grid instances.
    Directly modifying a cell is dangerous cause the maze could become incoherent"""

    def __init__(self, cell: Cell) -> None:
        """Store an inner private pointer to wrap accessors."""
        self.cell = cell

    @property
    def walls(self) -> int:
        """Return the immutable bits of movable interior walls."""
        return self.cell.walls

    @property
    def invincible_walls(self) -> int:
        """Return immutable permanently blocked boundary walls flags."""
        return self.cell.invincible_walls

    def hasWall(self, dir: Direction) -> bool:
        """Calculate whether the cell has a wall blocking a direction."""
        return ((self.walls | self.invincible_walls) & dir) != 0
