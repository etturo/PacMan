from typing import cast, Optional

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet


class SpriteLibraryMeta(type):
    def __getitem__(cls, key: str) -> SpriteSheet:
        sprite_map = \
            cast(dict[str, SpriteSheet], cls.__dict__.get('sprites', {}))
        try:
            return sprite_map[key]
        except KeyError:
            return cast(
                SpriteSheet,
                cls.__dict__.get('_SpriteLibrary__default_sprite')
                )


class SpriteLibrary(metaclass=SpriteLibraryMeta):
    sprites: dict[str, SpriteSheet] = {}
    __original_keys: list[str] = []
    __default_sprite: Optional[SpriteSheet] = None

    @classmethod
    def load(cls) -> None:
        cls.sprites = {
            "azure": SpriteSheet('data/assets/sprites/azure-sprite-sheet.png'),
            "b&w": SpriteSheet('data/assets/sprites/b&w-sprite-sheet.png'),
            "blue": SpriteSheet('data/assets/sprites/blue-sprite-sheet.png'),
            "melon": SpriteSheet('data/assets/sprites/melon-sprite-sheet.png'),
            "orange": SpriteSheet('data/assets/sprites/orange-sprite-sheet.png'),
            "pink": SpriteSheet('data/assets/sprites/pink-sprite-sheet.png'),
            "red": SpriteSheet('data/assets/sprites/red-sprite-sheet.png'),
            "white_text": SpriteSheet(
                'data/assets/sprites/white_text-sprite-sheet.png'),
            "yellow": SpriteSheet('data/assets/sprites/yellow-sprite-sheet.png'),
            "green": SpriteSheet('data/assets/sprites/green-sprite-sheet.png'),
        }
        cls.__original_keys = list(cls.sprites.keys())
        cls.__default_sprite = cls.sprites['b&w']

    @classmethod
    def __class_getitem__(cls, key: str) -> SpriteSheet:
        return cls.get(key)

    @classmethod
    def get(cls, key: str) -> SpriteSheet:
        sprite_map = \
            cast(dict[str, SpriteSheet], cls.__dict__.get('sprites', {}))
        try:
            return sprite_map[key]
        except KeyError:
            return cast(
                SpriteSheet,
                cls.__dict__.get('_SpriteLibrary__default_sprite')
                )

    @classmethod
    def add_item(cls, new_item: str, sheet_to_link: str) -> None:
        sprite_map = \
            cast(dict[str, SpriteSheet], cls.__dict__.get('sprites', {}))
        try:
            sprite_map[new_item] = sprite_map[sheet_to_link]
        except KeyError:
            print(f"WARNING! tried to link {new_item}"
                  f" to {sheet_to_link} unsuccesfully")
            return

    @classmethod
    def delete_item(cls, item_to_delete: str) -> None:
        sprite_map = \
            cast(dict[str, SpriteSheet], cls.__dict__.get('sprites', {}))
        if item_to_delete not in cls.__original_keys:
            sprite_map.pop(item_to_delete)