import pygame
import random

from abc import ABC, abstractmethod

from src import __version__, __authors__

from src.graphics.ui.button import Button
from src.graphics.ui.text import Text
from src.graphics.ui.element import Element

from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.graphical_utils.ui_utils import CHAR_MAPPING, SpriteType
from src.graphics.maze_render import MazeRender

from src.world.maze_wrapper import MazeWrapper
from src.world.maze import Maze

from src.utils.settings import Settings, GameEvent
from src.utils.models import GameSettings


class BaseState(ABC):
    @abstractmethod
    def getSurface(self) -> pygame.Surface:
        pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass


class MenuState(BaseState):
    def __init__(self) -> None:
        self.__buttons: list[Button]
        self.__texts: list[Text]

        screen_width = Settings.WINDOW_WIDTH
        screen_height = Settings.WINDOW_HEIGHT

        button_size = 60
        first_y_button = screen_height / 3

        # List of buttons
        start_button = Button(
            (screen_width / 2, first_y_button),
            SpriteLibrary['yellow'],
            GameEvent.MODE_TO_PLAYING,
            text='play',
            anchor='center',
            sprite_size=button_size,
            secondary_sheet=SpriteLibrary['yellow']
        )
        settings_button = Button(
            (screen_width / 2, first_y_button + 2 * button_size + 10),
            SpriteLibrary['yellow'],
            GameEvent.MODE_TO_SETTINGS,
            text='settings',
            anchor='center',
            sprite_size=button_size,
            secondary_sheet=SpriteLibrary['yellow']
        )
        scores_button = Button(
            (screen_width / 2, first_y_button + 4 * button_size + 20),
            SpriteLibrary['yellow'],
            GameEvent.MODE_TO_SCORES,
            text='scores',
            anchor='center',
            sprite_size=button_size,
            secondary_sheet=SpriteLibrary['yellow']
        )
        exit_button = Button(
            (screen_width / 2, first_y_button + 6 * button_size + 30),
            SpriteLibrary['yellow'],
            GameEvent.EXIT,
            text='exit',
            anchor='center',
            sprite_size=button_size,
            secondary_sheet=SpriteLibrary['yellow']
        )

        # List of text boxes
        title_txt = Text(
            "pacman",
            (screen_width / 2, screen_height / 6),
            SpriteLibrary['yellow'],
            100,
            anchor='center',
        )
        credits_text = Text(
            f"authors - {__authors__}",
            (0, screen_height),
            SpriteLibrary['white_text'],
            20,
            anchor='bottom left'
        )
        version_text = Text(
            f"version - {__version__}",
            (screen_width, screen_height),
            SpriteLibrary['white_text'],
            20,
            anchor='bottom right'
        )

        self.__buttons = [
            start_button,
            settings_button,
            scores_button,
            exit_button
        ]
        self.__texts = [
            title_txt,
            credits_text,
            version_text,
        ]
        self.__elements = [
            
        ]

        self.__surface = \
            pygame.Surface(
                (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT),
                )

    def getSurface(self) -> pygame.Surface:
        self.__surface.fill((0, 0, 0))
        for element in self.__buttons + self.__texts + self.__elements:
            element.render(self.__surface)
        return self.__surface

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.__buttons:
                button.handle_event(event)

    def update(self) -> None:
        pass


class StartingState(BaseState):
    def __init__(self) -> None:
        self.__screen_width = Settings.WINDOW_WIDTH
        self.__screen_height = Settings.WINDOW_HEIGHT
        self.__starting_buffer = ""
        self.__start_font = SpriteFont(SpriteLibrary.get('title'), 100)
        self.__end_font = SpriteFont(SpriteLibrary.get('yellow'), 100)
        self.__glyph_size = max(8, self.__start_font.getSize())
        self.__columns: int = max(10, self.__screen_width // self.__glyph_size)
        if self.__columns % 2 == 1:
            self.__columns -= 1
        self.__rows: int = max(8, self.__screen_height // self.__glyph_size)
        self.__chars = [char for char in CHAR_MAPPING if char != " "]
        self.__target_word = "PACMAN"
        self.__center_row = self.__rows // 2
        self.__start_col = \
            max(0,
                int((self.__columns - len(self.__target_word)) / 2 + 0.5))
        self.__reveal_start = 80
        self.__reveal_duration = 100
        self.__frame_count = 0

    def getSurface(self) -> pygame.Surface:
        '''Logic of the starting screen:
        - Keep the random background linear and smooth
        - After a fixed delay, start overriding the letters with PACMAN
        - During the reveal, characters become less likely while
            spaces become more likely
        '''
        screen = pygame.Surface(
            (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
            )
        if self.__frame_count < self.__reveal_start:
            if self.__frame_count % 10 == 0:
                grid = []
                for _ in range(self.__rows):
                    row = []
                    for _ in range(self.__columns):
                        if random.random() < 0.15:
                            row.append(" ")
                        else:
                            row.append(random.choice(self.__chars))
                    grid.append("".join(row))
                self.__starting_buffer = "\n".join(grid)

            title = Text(
                self.__starting_buffer,
                (self.__screen_width // 2, self.__screen_height // 2),
                SpriteLibrary.get('title'),
                100,
                anchor='center',
            )
            title.render(screen)

            return screen

        reveal_progress = \
            (self.__frame_count - self.__reveal_start) / self.__reveal_duration
        char_probability = 0.9 - (reveal_progress * 1.75)
        space_probability = 1.0 - char_probability

        if self.__frame_count % 10 == 0:
            lines = \
                (self.__starting_buffer.splitlines()
                    if self.__starting_buffer else []
                 )
            while len(lines) < self.__rows:
                lines.append("")
            lines = lines[:self.__rows]

            for row_index in range(self.__rows):
                line = [" "] * self.__columns

                if row_index == self.__center_row:
                    for offset, char in enumerate(self.__target_word):
                        line[self.__start_col + offset] = char

                    for col_index in range(self.__columns):
                        if random.random() < space_probability and not (
                            self.__start_col <= col_index <
                            self.__start_col + len(self.__target_word)
                        ):
                            line[col_index] = " "
                        elif not (self.__start_col <= col_index <
                                  self.__start_col + len(self.__target_word)):
                            line[col_index] = random.choice(self.__chars)
                else:
                    for col_index in range(self.__columns):
                        if random.random() < space_probability:
                            line[col_index] = " "
                        else:
                            line[col_index] = random.choice(self.__chars)

                lines[row_index] = "".join(line)

            self.__starting_buffer = "\n".join(lines)

        if space_probability < 1.15:
            title_sheet = SpriteLibrary.get('title')
        else:
            title_sheet = SpriteLibrary.get('yellow')
        title = Text(
            self.__starting_buffer,
            (self.__screen_width // 2, self.__screen_height // 2),
            title_sheet,
            100,
            anchor='center',
        )
        title.render(screen)

        if space_probability > 1.15:
            prompt = Text(
                "PRESS ENTER",
                (self.__screen_width // 2, self.__screen_height // 2 + 140),
                SpriteLibrary.get('yellow'),
                35,
                anchor='center',
            )
            prompt.render(screen)

        return screen

    def update(self) -> None:
        self.__frame_count += 1

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                GameEvent.post(GameEvent.MODE_TO_MENU)


class PlayingState(BaseState):
    def __init__(self, settings: GameSettings) -> None:
        self.__maze_renderer = MazeRender()
        self.__screen_width = Settings.WINDOW_WIDTH
        self.__screen_height = Settings.WINDOW_HEIGHT

        self.__actual_level = 0
        size = (
            settings.levels[self.__actual_level].width,
            settings.levels[self.__actual_level].height
        )
        self.__maze_wrapper = MazeWrapper()
        self.__maze_wrapper.generate(size=size, seed=settings.seed)
        self.__actual_maze = self.__maze_wrapper.maze

        self.__surface = pygame.Surface(
            (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        )

    def getSurface(self) -> pygame.Surface:
        self._render_maze(self.__actual_maze)
        return self.__surface

    def update(self) -> None:
        ...

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        ...

    def _render_maze(self, maze: Maze) -> None:
        # Calculation to make the tiles of the maze proportional to the size
        # of the screen. The -1 is to not cut out of the screen the maze
        cell_size = min(
            self.__screen_width // maze.getSize()[0],
            self.__screen_height // maze.getSize()[1]
        ) // 2 - 1

        if not self.__maze_renderer.is_initialized():
            self.__maze_renderer.init_maze(
                maze,
                cell_size,
                SpriteLibrary.get('wall_skins')
                )

        self.__maze_renderer.render(
            self.__surface,
            maze,
            cell_size,
            self.__screen_width,
            self.__screen_height
            )
