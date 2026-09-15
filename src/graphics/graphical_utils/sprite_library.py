from typing import Optional, cast

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.utils.paths import resource_path


class SpriteLibraryMeta(type):
    def __getitem__(cls, key: str) -> SpriteSheet:
        sprites = cast(
            dict[str, SpriteSheet],
            getattr(cls, 'sprites', {})
        )
        if key in sprites:
            return sprites[key]

        default = getattr(cls, '_SpriteLibrary__default_sprite', None)
        if default is not None:
            return cast(SpriteSheet, default)
        raise KeyError(key)


class SpriteLibrary(metaclass=SpriteLibraryMeta):
    sprites: dict[str, SpriteSheet] = {}
    __original_keys: list[str] = []
    __default_sprite: Optional[SpriteSheet] = None

    @classmethod
    def load(cls) -> None:
        cls.sprites = {
            "azure": SpriteSheet(
                str(resource_path('data/assets/sprites/azure-sprite-sheet.png'))
                ),
            "b&w": SpriteSheet(
                str(resource_path('data/assets/sprites/b&w-sprite-sheet.png'))
                ),
            "blue": SpriteSheet(
                str(resource_path('data/assets/sprites/blue-sprite-sheet.png'))
                ),
            "melon": SpriteSheet(
                str(resource_path('data/assets/sprites/melon-sprite-sheet.png'))
                ),
            "orange": SpriteSheet(
                str(resource_path('data/assets/sprites/orange-sprite-sheet.png'))
                ),
            "pink": SpriteSheet(
                str(resource_path('data/assets/sprites/pink-sprite-sheet.png'))
                ),
            "red": SpriteSheet(
                str(resource_path('data/assets/sprites/red-sprite-sheet.png'))
                ),
            "white_text": SpriteSheet(
                str(resource_path('data/assets/sprites/white_text-sprite-sheet.png'))
                ),
            "yellow": SpriteSheet(
                str(resource_path('data/assets/sprites/yellow-sprite-sheet.png'))
                ),
            "green": SpriteSheet(
                str(resource_path('data/assets/sprites/green-sprite-sheet.png'))
                ),
            "pink_black": SpriteSheet(
                str(resource_path('data/assets/sprites/pink_black-sprite-sheet.png'))
                ),
            "orange_green": SpriteSheet(
                str(resource_path('data/assets/sprites/orange_green-sprite-sheet.png'))
                ),
        }
        cls.__original_keys = list(cls.sprites.keys())
        cls.__default_sprite = cls.sprites['b&w']

    @classmethod
    def get(cls, key: str) -> SpriteSheet:
        if key in cls.sprites:
            return cls.sprites[key]
        if cls.__default_sprite is not None:
            return cls.__default_sprite
        raise KeyError(key)

    @classmethod
    def add_item(cls, new_item: str, sheet_to_link: str) -> None:
        if sheet_to_link in cls.sprites:
            cls.sprites[new_item] = cls.sprites[sheet_to_link]
        else:
            print(f"WARNING! tried to link {new_item}"
                  f" to {sheet_to_link} unsuccesfully")

    @classmethod
    def delete_item(cls, item_to_delete: str) -> None:
        if item_to_delete not in cls.__original_keys:
            cls.sprites.pop(item_to_delete, None)
