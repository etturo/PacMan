from abc import ABC

from src.utils.sprite_sheet import SpriteSheet


class ElementUI(ABC):
    def __init__(
        self,
        position: tuple[int, int],
        sprite_sheet: SpriteSheet)