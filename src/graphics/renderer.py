import pygame
import random

from src.graphics.maze_render import MazeRender
from src.graphics.sprite_sheet import SpriteSheet
from src.graphics.graphical_utils.sprite_font import SpriteFont

from src.world.maze import Maze

from src.utils.settings import GameMode


class Renderer:
    def __init__(self) -> None:
        # PYGAME VARIABLE INITIALIZED
        pygame.init()
        self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('PacMan')

        # RENDER UTILS
        self.__screen_width = self.__screen.get_width()
        self.__screen_height = self.__screen.get_height()
        self.__frame_count = 0

        # The maze renderer is an interface that render the maze,
        # the steps to make it work are first init, so it can initialize
        # every attribute that it need, and then the render method itself
        self.__maze_renderer: MazeRender = MazeRender()

        # The sprite sheet represent a sheet with a color palette associeted,
        # we can load different sheets with different palette but the usage is
        # equivalent
        self.__walls_sheet = SpriteSheet(
            'data/assets/sprites/blue-sprite-sheet.png'
        )
        self.__sheet = SpriteSheet(
            'data/assets/sprites/orange-sprite-sheet.png'
        )
        self.__text_sheet = SpriteSheet(
            'data/assets/sprites/white_text-sprite-sheet.png'
        )

        self.__text: SpriteFont = SpriteFont(self.__text_sheet)
        self.__start_text = SpriteFont(self.__text_sheet, 100)

        title_sheet = SpriteSheet(
            'data/assets/sprites/yellow-sprite-sheet.png'
        )
        self.__title_text = SpriteFont(title_sheet, 100)

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
        pygame.display.flip()
        self.__frame_count += 1

    def _render_maze(self, maze: Maze) -> None:
        # Calculation to make the tiles of the maze proportional to the size
        # of the screen
        cell_size = min(
            self.__screen_width // maze.getSize()[0],
            self.__screen_height // maze.getSize()[1]
        ) // 2 - 1

        self.__maze_renderer.render(
            self.__screen,
            self.__walls_sheet,
            maze,
            cell_size,
            self.__screen_width,
            self.__screen_height
            )

    def _render_main_menu(self) -> None:
        text = SpriteFont(self.__sheet)

        text.render(self.__screen, 0, 0, "CIAO, sono ettore\nPACMAN")

    def _render_starting_screen(self) -> None:
        '''Logic of the starting screen:
        - Keep the random background linear and smooth
        - After a fixed delay, start overriding the letters with PACMAN
        - During the reveal, characters become less likely while
            spaces become more likely
        '''
        if not hasattr(self, "_starting_buffer"):
            self._starting_buffer = ""

        glyph_size = max(8, self.__start_text.getSize())
        columns = max(10, self.__screen_width // glyph_size)
        rows = max(8, self.__screen_height // glyph_size)
        chars = \
            [char for char in self.__start_text.CHAR_MAPPING if char != " "]
        target_word = "PACMAN"
        center_row = rows // 2
        center_col = max(0, (columns // 2) - (len(target_word) // 2))

        reveal_start = 100
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
            self.__start_text.render(self.__screen,
                                     0, 0,
                                     self._starting_buffer)
            return

        reveal_progress = (self.__frame_count - reveal_start) / reveal_duration
        char_probability = 0.9 - (reveal_progress * 0.8)
        space_probability = 1.0 - char_probability

        if self.__frame_count % 10 == 0:
            lines = (self._starting_buffer.splitlines()
                     if self._starting_buffer else [])
            while len(lines) < rows:
                lines.append("")
            lines = lines[:rows]

            for row_index in range(rows):
                line = list(lines[row_index].ljust(columns))
                line = line[:columns]

                if row_index == center_row:
                    for col_index in range(columns):
                        word_offset = col_index - center_col
                        if 0 <= word_offset < len(target_word):
                            line[col_index] = target_word[word_offset]
                        elif random.random() < space_probability:
                            line[col_index] = " "
                        else:
                            line[col_index] = random.choice(chars)
                else:
                    for col_index in range(columns):
                        if random.random() < space_probability:
                            line[col_index] = " "
                        else:
                            line[col_index] = random.choice(chars)

                lines[row_index] = "".join(line)

            self._starting_buffer = "\n".join(lines)

        if space_probability < 1.27:
            self.__start_text.render(self.__screen,
                                     0, 0,
                                     self._starting_buffer)
        else:
            self.__title_text.render(self.__screen,
                                     0, 0,
                                     self._starting_buffer)
