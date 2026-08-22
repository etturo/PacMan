import pygame

from typing import Callable

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.ui_utils import SpriteType

from src.graphics.graphical_utils.sprite_font import SpriteFont, CHAR_MAPPING
from src.graphics.ui.drawable import Drawable

class Button(Drawable):
    def __init__(self,
                 position: tuple[int, int],
                 sprite_sheet: SpriteSheet,
                 on_click: Callable[[], None],
                 text: str,
                 anchor: str = "center"
                 ) -> None:
        super().__init__(position, sprite_sheet, anchor)
        self.__text: str = text.upper()
        self.__on_click: Callable[[], None] = on_click
        self.__is_hovered: bool = False
        self.__font: SpriteFont = SpriteFont(sprite_sheet, 80)
        # Offset in pixel
        self.__offset = 5
        self.__sprite_size = self.__font.getSize()

        self._create_textbox()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.__rect = self._get_rect()
            self.__is_hovered = self.__rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.__is_hovered:
                self.__on_click()

    def _create_textbox(self) -> None:
        box_width, box_height = self._calculate_text_size(
            text=self.__text,
            sprite_size=self.__sprite_size,
            offset=self.__offset,
            include_padding=True,
        )

        text_lines = self.__text.split("\n") or [""]
        _, text_height = self._calculate_text_render_size(
            self.__text,
            self.__sprite_size
        )

        inner_width = max(0, box_width - (self.__sprite_size * 2))
        inner_height = max(0, box_height - (self.__sprite_size * 2))

        y_padding: int = self.__sprite_size + max(0, (inner_height - text_height) // 2)

        h_border_lenght = max(1, box_width - (self.__sprite_size * 2))
        v_border_lenght = max(1, box_height - (self.__sprite_size * 2))

        horizontal_sprites = pygame.transform.scale(
            self._sheet[SpriteType.HORIZONTAL_EDGE],
            (h_border_lenght, self.__sprite_size)
        )
        vertical_sprites = pygame.transform.scale(
            self._sheet[SpriteType.VERTICAL_EDGE],
            (self.__sprite_size, v_border_lenght)
        )
        top_left_sprite = pygame.transform.scale(
            self._sheet[SpriteType.TOP_LEFT],
            (self.__sprite_size, self.__sprite_size)
        )
        top_right_sprite = pygame.transform.scale(
            self._sheet[SpriteType.TOP_RIGHT],
            (self.__sprite_size, self.__sprite_size)
        )
        bottom_left_sprite = pygame.transform.scale(
            self._sheet[SpriteType.BOTTOM_LEFT],
            (self.__sprite_size, self.__sprite_size)
        )
        bottom_right_sprite = pygame.transform.scale(
            self._sheet[SpriteType.BOTTOM_RIGHT],
            (self.__sprite_size, self.__sprite_size)
        )

        self._surface = pygame.Surface((box_width, box_height))
        self.__rect = self._get_rect()

        # top horizontal border
        self._surface.blit(
            horizontal_sprites,
            (self.__sprite_size, 0))

        # bottom horizontal border
        self._surface.blit(
            horizontal_sprites,
            (self.__sprite_size, box_height - self.__sprite_size))

        # left vertical border
        self._surface.blit(
            vertical_sprites,
            (0, self.__sprite_size))

        # right vertical blit
        self._surface.blit(
            vertical_sprites,
            (box_width - self.__sprite_size, self.__sprite_size))

        self._surface.blit(
            top_left_sprite,
            (0, 0))
        self._surface.blit(
            top_right_sprite,
            (box_width - self.__sprite_size, 0))
        self._surface.blit(
            bottom_left_sprite,
            (0, box_height - self.__sprite_size))
        self._surface.blit(
            bottom_right_sprite,
            (box_width - self.__sprite_size, box_height - self.__sprite_size))

        # Center each line independently so multiline labels are truly centered.
        for line_index, line in enumerate(text_lines):
            line_width, _ = self._calculate_text_render_size(
                line,
                self.__sprite_size
            )
            x_padding = self.__sprite_size + max(0, (inner_width - line_width) // 2)
            line_y = y_padding + (line_index * self.__sprite_size)
            self.__font.render(self._surface, (x_padding, line_y), line)

    @staticmethod
    def _calculate_text_render_size(text: str,
                                    sprite_size: int
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
