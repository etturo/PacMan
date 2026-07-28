from src.world.maze import Maze
from src.graphics.sprite_sheet import SpriteSheet, SpriteType


class Renderer:
    def __init__(self, maze: Maze) -> None:
        self.__maze = maze
        SpriteSheet('data/assets/sprites/red-sprite-sheet.png')

    def render(self) -> None:
        self._render_maze()

    def _render_maze(self) -> None:
        ...
