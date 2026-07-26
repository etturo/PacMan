import pygame

SPRITE_LENGHT = 8
SPRITE_WIDTH = 8
NUMBER_ZERO_COORDINATES = (1, 1)
NUMBER_ONE_COORDINATES = (10, 1)
NUMBER_TWO_COORDINATES = (19, 1)
NUMBER_THREE_COORDINATES = (28, 1)
NUMBER_FOUR_COORDINATES = (37, 1)
NUMBER_FIVE_COORDINATES = (46, 1)
NUMBER_SIX_COORDINATES = (55, 1)
NUMBER_SEVEN_COORDINATES = (64, 1)
NUMBER_EIGHT_COORDINATES = (73, 1)
NUMBER_NINE_COORDINATES = (82, 1)


class SpriteSheet:
    def __init__(self, filename: str,
                 color_key: tuple[int, int, int] = (255, 0, 255)) -> None:
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.sheet.set_colorkey(color_key)
        self.data: dict[str, pygame.Surface] = {}

        self._load_numbers()

    def __getitem__(self, key: str) -> pygame.Surface:
        return self.data[key.lower().strip()]

    def _load_numbers(self) -> None:
        self.data['zero'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_ZERO_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['one'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_ONE_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['two'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_TWO_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['three'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_THREE_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['four'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_FOUR_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['five'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_FIVE_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['six'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_SIX_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['seven'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_SEVEN_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['eight'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_EIGHT_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
        self.data['nine'] = self.sheet.subsurface(
            pygame.Rect(
                *NUMBER_NINE_COORDINATES,
                SPRITE_WIDTH,
                SPRITE_LENGHT
            )
        )
