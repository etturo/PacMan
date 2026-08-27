import pygame

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.ui_utils import SpriteType
from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.graphical_utils.ui_utils import CHAR_MAPPING
from src.graphics.ui.drawable import Drawable

from src.sounds.sound_effects import SoundEffect

from src.utils.settings import GameEvent


class Button(Drawable):
    def __init__(self,
                 position: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 on_click: GameEvent,
                 text: str,
                 sprite_size: int,
                 on_click_sfx: SoundEffect | None = None,
                 anchor: str = "center",
                 secondary_sheet: None | SpriteSheet = None,
                 ) -> None:
        super().__init__(position, sprite_sheet, anchor)
        self.__text: str = text.upper()
        self.__on_click: GameEvent = on_click
        self.__on_click_sfx: SoundEffect | None = on_click_sfx
        self.__is_hovered: bool = False
        self.__font: SpriteFont = SpriteFont(sprite_sheet, sprite_size)
        # Offset in pixel
        self.__offset = 5
        self.__sprite_size = sprite_size

        self.__secondary_surface: pygame.Surface
        self.__secondary_font = self.__font
        if secondary_sheet is not None:
            self.__secondary_font = \
                SpriteFont(secondary_sheet, sprite_size)

        self.__is_pressed: bool = False

        self._create_textbox()

        self.__primary_surface: pygame.Surface = self._surface

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.__rect = self._get_rect()
            self.__is_hovered = self.__rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.__is_hovered:
                if self.__on_click_sfx:
                    self.__on_click_sfx.play()
                GameEvent.post(self.__on_click)

        if self.__is_hovered:
            self._surface = self.__primary_surface
        else:
            self._surface = self.__secondary_surface

    def _create_textbox(self) -> None:
        text_size = self.__sprite_size
        box_sprite_size = text_size / 2

        box_width, box_height = self._calculate_text_size(
            text=self.__text,
            sprite_size=text_size,
            box_sprite_size=int(box_sprite_size),
            offset=self.__offset,
            include_padding=True,
        )

        text_lines = self.__text.split("\n") or [""]
        _, text_height = self._calculate_text_render_size(
            self.__text,
            self.__sprite_size
        )

        inner_width = max(0, box_width - (box_sprite_size * 2))
        inner_height = max(0, box_height - (box_sprite_size * 2))

        y_padding = \
            box_sprite_size + max(0, (inner_height - text_height) / 2)

        h_border_lenght = max(1, box_width - (box_sprite_size * 2))
        v_border_lenght = max(1, box_height - (box_sprite_size * 2))

        horizontal_sprites = pygame.transform.scale(
            self._sheet[SpriteType.HORIZONTAL_EDGE],
            (h_border_lenght, box_sprite_size)
        )
        vertical_sprites = pygame.transform.scale(
            self._sheet[SpriteType.VERTICAL_EDGE],
            (box_sprite_size, v_border_lenght)
        )
        top_left_sprite = pygame.transform.scale(
            self._sheet[SpriteType.TOP_LEFT],
            (box_sprite_size, box_sprite_size)
        )
        top_right_sprite = pygame.transform.scale(
            self._sheet[SpriteType.TOP_RIGHT],
            (box_sprite_size, box_sprite_size)
        )
        bottom_left_sprite = pygame.transform.scale(
            self._sheet[SpriteType.BOTTOM_LEFT],
            (box_sprite_size, box_sprite_size)
        )
        bottom_right_sprite = pygame.transform.scale(
            self._sheet[SpriteType.BOTTOM_RIGHT],
            (box_sprite_size, box_sprite_size)
        )

        self._surface = pygame.Surface((box_width, box_height))
        self.__secondary_surface = pygame.Surface((box_width, box_height))
        self.__rect = self._get_rect()

        # top horizontal border
        self._surface.blit(
            horizontal_sprites,
            (box_sprite_size, 0))

        # bottom horizontal border
        self._surface.blit(
            horizontal_sprites,
            (box_sprite_size, box_height - box_sprite_size))

        # left vertical border
        self._surface.blit(
            vertical_sprites,
            (0, box_sprite_size))

        # right vertical blit
        self._surface.blit(
            vertical_sprites,
            (box_width - box_sprite_size, box_sprite_size))

        self._surface.blit(
            top_left_sprite,
            (0, 0))
        self._surface.blit(
            top_right_sprite,
            (box_width - box_sprite_size, 0))
        self._surface.blit(
            bottom_left_sprite,
            (0, box_height - box_sprite_size))
        self._surface.blit(
            bottom_right_sprite,
            (box_width - box_sprite_size, box_height - box_sprite_size))

        # Center each line independently so
        #  multiline labels are truly centered.
        for line_index, line in enumerate(text_lines):
            line_width, _ = self._calculate_text_render_size(
                line,
                text_size
            )
            x_padding = \
                box_sprite_size + max(0, (inner_width - line_width) / 2)
            line_y = y_padding + (line_index * text_size)
            self.__secondary_font.render(
                self.__secondary_surface, (x_padding, line_y), line)
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
