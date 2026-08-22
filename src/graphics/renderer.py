import pygame
import random

from src.graphics.maze_render import MazeRender
from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.graphical_utils.ui_utils import CHAR_MAPPING
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.sprite_sheet import SpriteSheet
from src.graphics.ui.button import Button
from src.graphics.ui.text import Text
from src.graphics.menu import Menu

from src.world.maze import Maze

from src.utils.settings import Settings

from src.utils.settings import GameMode

class Renderer:
    def __init__(self) -> None:
        # RENDER UTILS
        self.__screen_width = Settings.WINDOW_WIDTH
        self.__screen_height = Settings.WINDOW_HEIGHT
        self.__frame_count = 0

        # PYGAME VARIABLE INITIALIZED
        pygame.init()
        self.__screen = pygame.display.set_mode(
            (self.__screen_width, self.__screen_height),
            pygame.FULLSCREEN | pygame.SCALED
            )
        pygame.display.set_caption('PacMan')

        # The maze renderer is an interface that render the maze,
        # the steps to make it work are first init, so it can initialize
        # every attribute that it need, and then the render method itself
        self.__maze_renderer: MazeRender = MazeRender()

        # The sprite sheet library loads all the sheets that are in the
        # 'data/assets/sprites' folder you can access to all the sprites
        # like a dictionary to the SpriteLibrary interface
        SpriteLibrary()
        # Is possible to add new key to access to the same value
        # so it's easier to access to the same value in different contexts
        SpriteLibrary.add_item('title', 'white_text')
        SpriteLibrary.add_item('wall_skins', 'blue')

        self.__menu: Menu = Menu()

    def render(
            self,
            maze: Maze,
            actual_game_mode: GameMode
            ) -> None:
        # Render BG
        self.__screen.fill((0, 0, 0))

        if actual_game_mode == GameMode.STARTING:
            self._render_starting_screen()
        if actual_game_mode == GameMode.MAIN_MENU:
            self._render_main_menu()
        if actual_game_mode == GameMode.PLAYING:
            self._render_maze(maze)

        # Update the screen
        pygame.display.update()
        self.__frame_count += 1

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
                SpriteLibrary['wall_skins']
                )

        self.__maze_renderer.render(
            self.__screen,
            maze,
            cell_size,
            self.__screen_width,
            self.__screen_height
            )

    def _render_main_menu(self) -> None:
        self.__menu.render(self.__screen)

    def _render_starting_screen(self) -> None:
        '''Logic of the starting screen:
        - Keep the random background linear and smooth
        - After a fixed delay, start overriding the letters with PACMAN
        - During the reveal, characters become less likely while
            spaces become more likely
        '''
        if not hasattr(self, "_starting_buffer"):
            self._starting_buffer = ""

        if not hasattr(self, "__start_font"):
            self.__start_font = SpriteFont(SpriteLibrary['title'], 100)
        if not hasattr(self, "__end_font"):
            self.__end_font = SpriteFont(SpriteLibrary['yellow'], 100)

        glyph_size = max(8, self.__start_font.getSize())
        columns: int = max(10, self.__screen_width // glyph_size)
        if columns % 2 == 1:
            columns -= 1
        rows: int = max(8, self.__screen_height // glyph_size)

        chars = [char for char in CHAR_MAPPING if char != " "]
        target_word = "PACMAN"
        center_row = rows // 2
        # Center the word in the available columns by rounding to the nearest
        # valid cell, instead of always floor()ing to the left.
        start_col = max(0, int((columns - len(target_word)) / 2 + 0.5))

        reveal_start = 80
        reveal_duration = 100

        if self.__frame_count < reveal_start:
            if self.__frame_count % 10 == 0:
                grid = []
                for _ in range(rows):
                    row = []
                    for _ in range(columns):
                        if random.random() < 0.15:
                            row.append(" ")
                        else:
                            row.append(random.choice(chars))
                    grid.append("".join(row))
                self._starting_buffer = "\n".join(grid)

            title = Text(
                self._starting_buffer,
                (self.__screen_width // 2, self.__screen_height // 2),
                SpriteLibrary['title'],
                100,
                anchor='center',
            )
            title.render(self.__screen)
            return

        reveal_progress = (self.__frame_count - reveal_start) / reveal_duration
        char_probability = 0.9 - (reveal_progress * 1.75)
        space_probability = 1.0 - char_probability

        if self.__frame_count % 10 == 0:
            lines = (self._starting_buffer.splitlines() if self._starting_buffer else [])
            while len(lines) < rows:
                lines.append("")
            lines = lines[:rows]

            for row_index in range(rows):
                line = [" "] * columns

                if row_index == center_row:
                    for offset, char in enumerate(target_word):
                        line[start_col + offset] = char

                    for col_index in range(columns):
                        if random.random() < space_probability and not (
                            start_col <= col_index < start_col + len(target_word)
                        ):
                            line[col_index] = " "
                        elif not (start_col <= col_index < start_col + len(target_word)):
                            line[col_index] = random.choice(chars)
                else:
                    for col_index in range(columns):
                        if random.random() < space_probability:
                            line[col_index] = " "
                        else:
                            line[col_index] = random.choice(chars)

                lines[row_index] = "".join(line)

            self._starting_buffer = "\n".join(lines)

        if space_probability < 1.15:
            title_sheet = SpriteLibrary['title']
        else:
            title_sheet = SpriteLibrary['yellow']
        title = Text(
            self._starting_buffer,
            (self.__screen_width // 2, self.__screen_height // 2),
            title_sheet,
            100,
            anchor='center',
        )
        title.render(self.__screen)

        if space_probability > 1.15:
            prompt = Text(
                "PRESS ENTER",
                (self.__screen_width // 2, self.__screen_height // 2 + 140),
                SpriteLibrary['yellow'],
                35,
                anchor='center',
            )
            prompt.render(self.__screen)

    def handle_menu_events(self, events: list[pygame.event.Event]) -> None:
        self.__menu.handle_events(events)
