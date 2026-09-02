import pygame

from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.ui_utils import SpriteType
from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.graphical_utils.ui_utils import CHAR_MAPPING
from src.graphics.ui.drawable import Drawable
from src.graphics.ui.element import Text

from src.sounds.sound_effects import SoundEffect

from src.utils.settings import GameEvent


class Button(Drawable):
    def __init__(self,
                 position: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 on_click: GameEvent,
                 text: str,
                 sprite_size: float,
                 on_click_sfx: SoundEffect | None = None,
                 anchor: str = "center",
                 secondary_sheet: None | SpriteSheet = None,
                 ) -> None:
        super().__init__(position, sprite_sheet, anchor)
        self._text: str = text.upper()
        self._on_click: GameEvent = on_click
        self._on_click_sfx: SoundEffect | None = on_click_sfx
        self._is_hovered: bool = False
        self._font: SpriteFont = SpriteFont(sprite_sheet, sprite_size)
        # Offset in pixel
        self._offset = 5
        self._sprite_size = sprite_size

        self._secondary_surface: pygame.Surface
        self._secondary_font = self._font
        if secondary_sheet is not None:
            self._secondary_font = \
                SpriteFont(secondary_sheet, sprite_size)

        self._is_pressed: bool = False

        self._create_textbox()

        self._primary_surface: pygame.Surface = self._surface

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._rect = self._get_rect()
            self._is_hovered = self._rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self._is_hovered:
                if self._on_click_sfx:
                    self._on_click_sfx.play()
                GameEvent.post(self._on_click)

        if self._is_hovered:
            self._surface = self._primary_surface
        else:
            self._surface = self._secondary_surface

    def _create_textbox(self) -> None:
        text_size = self._sprite_size
        box_sprite_size = text_size / 2

        box_width, box_height = self._calculate_text_size(
            text=self._text,
            sprite_size=text_size,
            box_sprite_size=int(box_sprite_size),
            offset=self._offset,
            include_padding=True,
        )

        text_lines = self._text.split("\n") or [""]
        _, text_height = self._calculate_text_render_size(
            self._text,
            self._sprite_size
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
        self._secondary_surface = pygame.Surface((box_width, box_height))
        self._rect = self._get_rect()

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
            self._secondary_font.render(
                self._secondary_surface, (x_padding, line_y), line)
            self._font.render(self._surface, (x_padding, line_y), line)

    @staticmethod
    def _calculate_text_render_size(text: str,
                                    sprite_size: float
                                    ) -> tuple[float, float]:
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


class ToggleButton(Button):
    def __init__(self,
                 position: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 on_click: GameEvent,
                 text: str,
                 sprite_size: float,
                 initial_value: bool,
                 on_click_sfx: SoundEffect | None = None,
                 anchor: str = "center",
                 secondary_sheet: None | SpriteSheet = None,
                 active_sheet: None | SpriteSheet = None,
                 secondary_active_sheet: None | SpriteSheet = None,
        ) -> None:

        self.__toggled: bool = initial_value
        self.__title_text = text
        self.__status_text = str(self.__toggled)
        self._text = f"{self.__title_text}\n{self.__status_text}"
        
        self.__base_sheet = sprite_sheet
        self.__base_secondary_sheet = secondary_sheet
        self.__active_sheet = active_sheet
        self.__secondary_active_sheet = secondary_active_sheet

        super().__init__(
            position,
            sprite_sheet,
            on_click,
            self._text,
            sprite_size,
            on_click_sfx,
            anchor,
            secondary_sheet
        )

        if self.__toggled:
            if self.__active_sheet:
                self._sheet = self.__active_sheet
            if self.__secondary_active_sheet:
                self._secondary_font = SpriteFont(
                    self.__secondary_active_sheet, 
                    self._sprite_size
                )
        else:
            self._sheet = self.__base_sheet
            if self.__base_secondary_sheet:
                self._secondary_font = SpriteFont(
                    self.__base_secondary_sheet, 
                    self._sprite_size
                )

        self._create_textbox()
        self._primary_surface = self._surface

        if self.__toggled:
            self._surface = self.__active_sheet
        else:
            self._surface = self._secondary_surface


    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._rect = self._get_rect()
            self._is_hovered = self._rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self._is_hovered:
                if self._on_click_sfx:
                    self._on_click_sfx.play()
                GameEvent.post(self._on_click)
                self.__toggled = not self.__toggled
                self.__status_text = str(self.__toggled)
                self._text = f"{self.__title_text}\n{self.__status_text}".upper()

                if self.__toggled:
                    if self.__active_sheet:
                        self._sheet = self.__active_sheet
                    if self.__secondary_active_sheet:
                        self._secondary_font = SpriteFont(
                            self.__secondary_active_sheet, 
                            self._sprite_size
                        )
                else:
                    self._sheet = self.__base_sheet
                    if self.__base_secondary_sheet:
                        self._secondary_font = SpriteFont(
                            self.__base_secondary_sheet, 
                            self._sprite_size
                        )

                self._create_textbox()
                self._primary_surface = self._surface

        if self._is_hovered or self.__toggled:
            self._surface = self._primary_surface
        else:
            self._surface = self._secondary_surface


class SlideButton(Button):
    def __init__(self,
                 position: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 increment_on_click: GameEvent,
                 decrement_on_click: GameEvent,
                 initial_value: int,
                 text: str,
                 sprite_size: float,
                 step_value: int = 1,
                 on_click_sfx: SoundEffect | None = None,
                 anchor: str = "center",
                 secondary_sheet: None | SpriteSheet = None,
        ) -> None:
        super(Button, self).__init__(position, sprite_sheet, anchor)
        self._text: str = f"{text}\n\n"
        self.__increment_on_click: GameEvent = increment_on_click
        self.__decrement_on_click: GameEvent = decrement_on_click
        self._on_click_sfx: SoundEffect | None = on_click_sfx
        self._is_hovered: bool = False
        self._font: SpriteFont = SpriteFont(sprite_sheet, sprite_size)
        self.__value: int = initial_value
        self.__step_value = step_value

        self._offset = 5
        self._sprite_size = sprite_size

        self._secondary_surface: pygame.Surface
        self._secondary_font = self._font
        if secondary_sheet is not None:
            self._secondary_font = SpriteFont(secondary_sheet, sprite_size)

        self._is_pressed: bool = False

        self._create_textbox()

        self._clean_primary = self._surface.copy()
        self._clean_secondary = self._secondary_surface.copy()

        self.__left_arrow = Button(
            position=(0, self._clean_primary.get_height()),
            sprite_sheet=sprite_sheet,
            on_click=decrement_on_click,
            text="<",
            sprite_size=sprite_size,
            on_click_sfx=on_click_sfx,
            anchor='bottom left',
            secondary_sheet=secondary_sheet
        )

        self.__right_arrow = Button(
            position=(self._clean_primary.get_width(), self._clean_primary.get_height()),
            sprite_sheet=sprite_sheet,
            on_click=increment_on_click,
            text=">",
            sprite_size=sprite_size,
            on_click_sfx=on_click_sfx,
            anchor='bottom right',
            secondary_sheet=secondary_sheet
        )

        self.__value_count = Text(
            text=str(self.__value),
            position=(self._surface.get_width() / 2, self._surface.get_height() / 1.15),
            sprite_sheet=sprite_sheet,
            text_size=sprite_size,
            anchor="mid bottom"
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self._rect = self._get_rect()
            self._is_hovered = self._rect.collidepoint(event.pos)

            local_pos = (event.pos[0] - self._rect.left, event.pos[1] - self._rect.top)

            event_dict = {'pos': local_pos}
            if hasattr(event, 'button'):
                event_dict['button'] = event.button

            local_event = pygame.event.Event(event.type, event_dict)
            self.__left_arrow.handle_event(local_event)
            self.__right_arrow.handle_event(local_event)

        if event.type == self.__increment_on_click:
            self.__value += self.__step_value
        elif event.type == self.__decrement_on_click:
            self.__value -= self.__step_value

        self.__value_count.setText(str(self.__value))

        base_bg = self._clean_secondary
        self._surface = base_bg.copy()

        self.__left_arrow.render(self._surface)
        self.__right_arrow.render(self._surface)
        self.__value_count.render(self._surface)
