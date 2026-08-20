import pygame

from typing import Callable

from src.utils.sprite_sheet import SpriteSheet, SpriteType

from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.drawable import Drawable

class Button(Drawable):
    def __init__(self,
                 position: tuple[int, int],
                 text: str,
                 sprite_sheet: SpriteSheet,
                 on_click: Callable[[], None],
                 ) -> None:
        super().__init__(position, sprite_sheet)
        self.__text: str = text.upper()
        self.__on_click: Callable[[], None] = on_click
        self.__is_hovered: bool = False
        self.__font: SpriteFont = SpriteFont(sprite_sheet, 80)
        # Offset in pixel
        self.__offset = 5
        self.__sprite_size = self.__font.getSize()
        self.__surface: pygame.Surface

        self._create_textbox()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.__is_hovered = self.__rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.__is_hovered:
                self.__on_click()

    def _create_textbox(self) -> None:
        box_width, box_height = self._calculate_text_size(
            self.__text,
            self.__sprite_size,
            self.__offset,
            self.__font.CHAR_MAPPING
            )

        text_lines = self.__text.split("\n") or [""]
        _, text_height = self._calculate_text_render_size(
            self.__text,
            self.__sprite_size,
            self.__font.CHAR_MAPPING
        )

        inner_width = max(0, box_width - (self.__sprite_size * 2))
        inner_height = max(0, box_height - (self.__sprite_size * 2))

        y_padding: int = self.__sprite_size + max(0, (inner_height - text_height) // 2)

        h_border_lenght = max(1, box_width - (self.__sprite_size * 2))
        v_border_lenght = max(1, box_height - (self.__sprite_size * 2))

        horizontal_sprites = pygame.transform.scale(
            self.__sheet[SpriteType.HORIZONTAL_EDGE],
            (h_border_lenght, self.__sprite_size)
        )
        vertical_sprites = pygame.transform.scale(
            self.__sheet[SpriteType.VERTICAL_EDGE],
            (self.__sprite_size, v_border_lenght)
        )
        top_left_sprite = pygame.transform.scale(
            self.__sheet[SpriteType.TOP_LEFT],
            (self.__sprite_size, self.__sprite_size)
        )
        top_right_sprite = pygame.transform.scale(
            self.__sheet[SpriteType.TOP_RIGHT],
            (self.__sprite_size, self.__sprite_size)
        )
        bottom_left_sprite = pygame.transform.scale(
            self.__sheet[SpriteType.BOTTOM_LEFT],
            (self.__sprite_size, self.__sprite_size)
        )
        bottom_right_sprite = pygame.transform.scale(
            self.__sheet[SpriteType.BOTTOM_RIGHT],
            (self.__sprite_size, self.__sprite_size)
        )

        self.__surface = pygame.Surface((box_width, box_height))

        # top horizontal border
        self.__surface.blit(
            horizontal_sprites,
            (self.__sprite_size, 0))

        # bottom horizontal border
        self.__surface.blit(
            horizontal_sprites,
            (self.__sprite_size, box_height - self.__sprite_size))

        # left vertical border
        self.__surface.blit(
            vertical_sprites,
            (0, self.__sprite_size))

        # right vertical blit
        self.__surface.blit(
            vertical_sprites,
            (box_width - self.__sprite_size, self.__sprite_size))

        self.__surface.blit(
            top_left_sprite,
            (0, 0))
        self.__surface.blit(
            top_right_sprite,
            (box_width - self.__sprite_size, 0))
        self.__surface.blit(
            bottom_left_sprite,
            (0, box_height - self.__sprite_size))
        self.__surface.blit(
            bottom_right_sprite,
            (box_width - self.__sprite_size, box_height - self.__sprite_size))

        # Center each line independently so multiline labels are truly centered.
        for line_index, line in enumerate(text_lines):
            line_width, _ = self._calculate_text_render_size(
                line,
                self.__sprite_size,
                self.__font.CHAR_MAPPING
            )
            x_padding = self.__sprite_size + max(0, (inner_width - line_width) // 2)
            line_y = y_padding + (line_index * self.__sprite_size)
            self.__font.render(self.__surface, x_padding, line_y, line)

    @staticmethod
    def _calculate_text_size(text: str,
                             sprite_size: int,
                             offset: int,
                             CHAR_MAPPING: dict[str, SpriteType]
                             ) -> tuple[int, int]:
        if not text:
            return (sprite_size * 2, sprite_size * 2)

        text_lines = text.split("\n") or [text]
        max_line_length = 0

        for line in text_lines:
            visible_chars = sum(
                1 for char in line if char in CHAR_MAPPING
            )
            max_line_length = max(max_line_length, visible_chars)

        box_width = max(1, max_line_length) * (sprite_size + offset)
        box_height = max(1, len(text_lines)) * (sprite_size + offset)

        box_width += sprite_size * 2
        box_height += sprite_size * 2

        print(visible_chars)

        return (box_width, box_height)

    @staticmethod
    def _calculate_text_render_size(text: str,
                                    sprite_size: int,
                                    CHAR_MAPPING: dict[str, SpriteType]
                                    ) -> tuple[int, int]:
        if not text:
            return (0, 0)

        text_lines = text.split("\n") or [""]
        max_line_length = 0

        for line in text_lines:
            visible_chars = sum(
                1 for char in line if char.upper() in CHAR_MAPPING
            )
            max_line_length = max(max_line_length, visible_chars)

        text_width = max_line_length * sprite_size
        text_height = len(text_lines) * sprite_size

        return (text_width, text_height)
