from src.utils.sprite_sheet import SpriteSheet


class SpriteLibrary:
    sprites: dict[str, SpriteSheet] = {
        "azure": SpriteSheet('data/assets/sprites/azure-sprite-sheet.png'),
        "b&w": SpriteSheet('data/assets/sprites/b&w-sprite-sheet.png'),
        "blue": SpriteSheet('data/assets/sprites/blue-sprite-sheet.png'),
        "melon": SpriteSheet('data/assets/sprites/melon-sprite-sheet.png'),
        "orange": SpriteSheet('data/assets/sprites/orange-sprite-sheet.png'),
        "pink": SpriteSheet('data/assets/sprites/pink-sprite-sheet.png'),
        "red": SpriteSheet('data/assets/sprites/red-sprite-sheet.png'),
        "white_text": SpriteSheet('data/assets/sprites/white_text-sprite-sheet.png'),
        "yellow": SpriteSheet('data/assets/sprites/yellow-sprite-sheet.png')
    }
    __original_keys = list(sprites.keys())
    __default_sprite = sprites['b&w']

    @classmethod
    def __getitem__(cls, key) -> SpriteSheet:
        try:
            return cls.sprites[key]
        except KeyError:
            return cls.__default_sprite

    def __class_getitem__(cls, key) -> SpriteSheet:
        return cls.__getitem__(key)

    @classmethod
    def add_item(cls, new_item: str, sheet_to_link: str) -> None:
        try:
            cls.sprites[new_item] = cls.sprites[sheet_to_link]
        except KeyError:
            print(f"WARNING! tried to link {new_item} to {sheet_to_link} unsuccesfully")
            return

    @classmethod
    def delete_item(cls, item_to_delete: str) -> None:
        if not item_to_delete in cls.__original_keys:
            cls.sprites.pop(item_to_delete)
