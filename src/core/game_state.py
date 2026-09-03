import pygame
import random
import json

from abc import ABC, abstractmethod
from pathlib import Path

from src import __version__, __authors__

from src.entities.pacman import Pacman
from src.entities.entity import Entity
from src.entities.pacgums import Pacgum, SuperPacgum
from src.entities.ghost import Ghost, GhostMode

from src.graphics.ui.button import Button, ToggleButton, SlideButton
from src.graphics.ui.text import Text
from src.graphics.ui.element import (
    LiveElement,
    Lives,
    Points,
    TextInput,
    Leadboard,
    Box,
    Element,
    Timer
    )

from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.graphics.graphical_utils.sprite_font import SpriteFont
from src.graphics.graphical_utils.ui_utils import CHAR_MAPPING, SpriteType
from src.graphics.maze_render import MazeRender

from src.world.maze_wrapper import MazeWrapper
from src.world.cell import Direction

from src.utils.settings import Settings, GameEvent
from src.utils.models import GameSettings


class BaseState(ABC):
    @abstractmethod
    def getSurface(self, dt: float) -> pygame.Surface:
        pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    def getPoints(self) -> int:
        # mypy says this has to be like that... ok...
        return 0

    def getLives(self) -> int:
        # mypy says this has to be like that... ok...
        return 0


class MenuState(BaseState):
    def __init__(self) -> None:
        self.__buttons: list[Button]
        self.__texts: list[Text]

        screen_width = Settings.VIRTUAL_WINDOW_WIDTH
        screen_height = Settings.VIRTUAL_WINDOW_HEIGHT

        button_size = screen_height / 15
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
            (screen_width / 2,
             first_y_button + button_size * 2 + screen_height / 30),
            SpriteLibrary['yellow'],
            GameEvent.MODE_TO_SETTINGS,
            text='settings',
            anchor='center',
            sprite_size=button_size,
            secondary_sheet=SpriteLibrary['yellow']
        )
        exit_button = Button(
            (screen_width / 2,
             first_y_button + button_size * 4 + screen_height / 15),
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
            (screen_width / 2, screen_height / 8),
            SpriteLibrary['yellow'],
            screen_height / 10,
            anchor='center',
        )
        credits_text = Text(
            f"authors: {__authors__}",
            (0, screen_height),
            SpriteLibrary['white_text'],
            screen_height / 30,
            anchor='bottom left'
        )
        version_text = Text(
            f"version: {__version__}",
            (screen_width, screen_height),
            SpriteLibrary['white_text'],
            screen_height / 30,
            anchor='bottom right'
        )

        leadboard = Leadboard(
            (10, 10),
            screen_width / 3.5,
            screen_height - (screen_height / 10),
            SpriteLibrary['leadboard'],
            SpriteType.EMPTY_WALL,
            button_size
        )

        self.__buttons = [
            start_button,
            exit_button,
            settings_button,
        ]
        self.__texts = [
            title_txt,
            credits_text,
            version_text,
        ]
        self.__elements = [
            leadboard
        ]

        self.__surface = \
            pygame.Surface(
                (Settings.VIRTUAL_WINDOW_WIDTH,
                 Settings.VIRTUAL_WINDOW_HEIGHT)
                )

    def getSurface(self, dt: float) -> pygame.Surface:
        self.__surface.fill((0, 0, 0))
        for element in self.__buttons + self.__texts + self.__elements:
            element.render(self.__surface)
        return self.__surface

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.__buttons:
                button.handle_event(event)

    def update(self, dt: float) -> None:
        pass


class StartingState(BaseState):
    def __init__(self) -> None:
        self.__screen_width = Settings.VIRTUAL_WINDOW_WIDTH
        self.__screen_height = Settings.VIRTUAL_WINDOW_HEIGHT

        self.__surface = pygame.Surface(
            (self.__screen_width, self.__screen_height)
        )

        self.__starting_buffer = ""
        self.__text_size = self.__screen_height // 16
        self.__start_font = SpriteFont(
            SpriteLibrary.get('title'), self.__text_size)
        self.__end_font = SpriteFont(
            SpriteLibrary.get('yellow'), self.__text_size)
        self.__glyph_size = max(8, self.__start_font.getSize())
        self.__columns = int(max(10, self.__screen_width // self.__glyph_size))
        if self.__columns % 2 == 1:
            self.__columns -= 1
        self.__rows = int(max(8, self.__screen_height // self.__glyph_size))
        self.__chars = [char for char in CHAR_MAPPING if char != " "]
        self.__target_word = "PACMAN"
        self.__center_row = self.__rows // 2
        self.__start_col = \
            max(0, int((self.__columns - len(self.__target_word)) / 2 + 0.5))

        self.__reveal_start = 1.5
        self.__reveal_duration = 1.5
        self.__elapsed_time = 0.0
        self.__grid_timer = 0.0
        self.__grid_interval = 0.15

    def getSurface(self, dt: float) -> pygame.Surface:
        self.__surface.fill((0, 0, 0))

        if self.__elapsed_time < self.__reveal_start:
            if self.__grid_timer >= self.__grid_interval:
                self.__grid_timer = 0.0
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
                self.__text_size,
                anchor='center',
            )
            title.render(self.__surface)

            return self.__surface

        reveal_progress = \
            (self.__elapsed_time - self.__reveal_start) \
            / self.__reveal_duration
        reveal_progress = min(1.0, max(0.0, reveal_progress))

        char_probability = 0.9 - (reveal_progress * 1.75)
        space_probability = 1.0 - char_probability

        if self.__grid_timer >= self.__grid_interval:
            self.__grid_timer = 0.0
            lines = (
                self.__starting_buffer.splitlines()
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
                        if random.random() < space_probability and not \
                            (self.__start_col <=
                             col_index < self.__start_col +
                             len(self.__target_word)
                             ):
                            line[col_index] = " "
                        elif not (
                                self.__start_col <=
                                col_index <
                                self.__start_col +
                                len(self.__target_word)
                                ):
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
            self.__text_size,
            anchor='center',
        )
        title.render(self.__surface)

        if space_probability > 1.15:
            prompt = Text(
                "PRESS ENTER",
                (self.__screen_width // 2,
                 self.__screen_height // 2 + self.__text_size + 20),
                SpriteLibrary.get('yellow'),
                12,
                anchor='center',
            )
            prompt.render(self.__surface)

        return self.__surface

    def update(self, dt: float) -> None:
        self.__elapsed_time += dt
        self.__grid_timer += dt

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.event.post(pygame.event.Event(GameEvent.MODE_TO_MENU))


class PlayingState(BaseState):
    def __init__(self, settings: GameSettings) -> None:
        self.__maze_renderer = MazeRender()
        self.__screen_width = Settings.VIRTUAL_WINDOW_WIDTH
        self.__screen_height = Settings.VIRTUAL_WINDOW_HEIGHT

        self.__settings = settings
        self.__points: int = 0
        self.__max_seconds = settings.level_max_time
        self.__time_elapsed = 0.0

        self.__actual_level = 0
        size = (
            settings.levels[self.__actual_level].width,
            settings.levels[self.__actual_level].height
        )
        self.__maze_wrapper = MazeWrapper()
        self.__maze_wrapper.generate(size=size, seed=settings.seed)
        self.__actual_maze = self.__maze_wrapper.maze

        self.__surface = pygame.Surface(
            (Settings.VIRTUAL_WINDOW_WIDTH, Settings.VIRTUAL_WINDOW_HEIGHT)
        )

        self.__entities: list[Entity] = []
        self._render_maze()

        maze_w, maze_h = self.__actual_maze.getSize()
        self.__scaled_size = self.__screen_height / (maze_h * 2 + 1) / 1.1

        self.__text_size = self.__screen_width / 30

        if (maze_w % 2 != 0):
            self.__pacman_initial_pos = (maze_w // 2, maze_h // 2)
        else:
            self.__pacman_initial_pos = ((maze_w // 2) - 1, maze_h // 2)

        self.__pacman: Pacman = Pacman(
            self.__pacman_initial_pos,
            self.__scaled_size * 1.6,
            4.0,
            settings.lives
            )
        self.__current_direction = self.__pacman.getDir()

        self.__pacgums: list[Pacgum | SuperPacgum] = []
        self.__ft_cells = self._get_42_coord()

        self.__is_started = False

        # ================#
        from src.world.maze import Maze

        def nothing(
            maze: Maze,
            pos: tuple[int, int],
            target: tuple[int, int]
        ) -> Direction:
            return Direction.STILL
        # ================#

        self.__ghost = Ghost(
            (0, 0),
            self.__scaled_size * 1.6,
            0,
            SpriteLibrary.get('red'),
            nothing
        )

        for x in range(maze_w):
            for y in range(maze_h):
                if (x, y) in self.__ft_cells:
                    continue
                if (
                        (x == 0 and y == 0) or
                        (x == 0 and y == maze_h - 1) or
                        (x == maze_w - 1 and y == 0) or
                        (x == maze_w - 1 and y == maze_h - 1)
                        ):
                    self.__pacgums.append(
                        SuperPacgum(
                            (x, y),
                            self.__scaled_size,
                            settings.points_per_super_pacgum
                            )
                        )

                elif (x, y) == self.__pacman_initial_pos:
                    continue

                else:
                    self.__pacgums.append(
                        Pacgum(
                            (x, y),
                            self.__scaled_size,
                            settings.points_per_pacgum
                            )
                        )

        lives = Lives(
            position=(0, 0),
            sprite_sheet=SpriteLibrary['yellow'],
            sprite_type=SpriteType.LIVES_SPRITE,
            size=self.__text_size * 1.5,
            initial_lives=settings.lives
            )
        points = Points(
            position=(Settings.VIRTUAL_WINDOW_WIDTH - 220, 10),
            sprite_sheet=SpriteLibrary['white'],
            size=self.__text_size / 1.2,
            initial_points=self.__points,
            )
        self.__timer = Timer(
            position=(
                Settings.VIRTUAL_WINDOW_WIDTH,
                Settings.VIRTUAL_WINDOW_HEIGHT),
            anchor="bottom right",
            width=self.__text_size * 5,
            height=self.__text_size * 4,
            sprite_sheet=SpriteLibrary['white'],
            sprite_type=SpriteType.EMPTY_WALL,
            size=self.__text_size / 1.2,
            time=self.__time_elapsed,
            max_time_seconds=self.__settings.level_max_time
        )

        self.__ui_elements: list[LiveElement] = [
            lives,
            points,
            self.__timer,
        ]
        self.__entities.extend(self.__pacgums)
        self.__entities.append(self.__pacman)
        self.__entities.append(self.__ghost)

    def getSurface(self, dt: float) -> pygame.Surface:
        self.__surface.fill((0, 0, 0))
        self._render_maze()

        for element in self.__ui_elements:
            element.render(self.__surface)

        for entity in self.__entities:
            if self.__pacman.isAlive() is False and isinstance(entity, Ghost):
                continue
            e_x, e_y = entity.get_visual_pos()
            screen_x, screen_y = self._get_entity_screen_pos(e_x, e_y)

            entity.render(self.__surface, (screen_x, screen_y), dt)

        return self.__surface

    def getPoints(self) -> int:
        return self.__points

    def getLives(self) -> int:
        return self.__pacman.getLives()

    def getRemainingTime(self) -> float:
        return self.__timer.getRemainingTime()

    def update(self, dt: float) -> None:
        for element in self.__ui_elements:
            if isinstance(element, Lives):
                element.update(self.__pacman.getLives())
            elif isinstance(element, Points):
                element.update(self.__points)
            elif isinstance(element, Timer):
                element.update(dt)

        if not self.__is_started:
            return

        self.__time_elapsed = self.getRemainingTime()

        if self.__time_elapsed <= 0:
            GameEvent.post(GameEvent.MODE_TO_GAME_OVER)

        self.__pacman.update(dt)
        if self.__pacman.getLives() <= 0:
            GameEvent.post(GameEvent.MODE_TO_GAME_OVER)
        self._detect_collision()

        for entity in self.__entities:
            if not entity.isAlive() and not isinstance(entity, Pacman | Ghost):
                self.__entities.remove(entity)

            if not isinstance(entity, Pacman):
                entity.update(dt)

            if not entity.isMoving():
                current_cell = entity.getCurrentCell()
                queued_dir = entity.getQueuedDirection()
                current_dir = entity.getCurrentDirection()

                if (
                    queued_dir != Direction.STILL
                    and not
                    self.__actual_maze[current_cell].hasWall(queued_dir)
                    and
                    (queued_dir != current_dir.opposite()
                     or
                     isinstance(entity, Pacman))
                ):
                    d_x, d_y = queued_dir.vector()
                    target_cell = (
                        current_cell[0] + d_x,
                        current_cell[1] + d_y
                        )
                    entity.moveTo(target_cell, queued_dir)

                elif (current_dir != Direction.STILL and not
                      self.__actual_maze[current_cell].hasWall(current_dir)
                      ):
                    d_x, d_y = current_dir.vector()
                    target_cell = (
                        current_cell[0] + d_x,
                        current_cell[1] + d_y
                        )
                    entity.moveTo(target_cell, current_dir)

                else:
                    entity.moveTo(current_cell, current_dir)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:

            if event.type == GameEvent.RESET_POSITIONS:
                self._reset_entity_pos()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.__pacman.setQueueDirection(Direction.NORTH)
                    if not self.__is_started:
                        self.__is_started = True
                        self.__timer.start()
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.__pacman.setQueueDirection(Direction.WEST)
                    if not self.__is_started:
                            self.__is_started = True
                            self.__timer.start()
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.__pacman.setQueueDirection(Direction.EAST)
                    if not self.__is_started:
                            self.__is_started = True
                            self.__timer.start()
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.__pacman.setQueueDirection(Direction.SOUTH)
                    if not self.__is_started:
                            self.__is_started = True
                            self.__timer.start()


    def _reset_entity_pos(self) -> None:
        for entity in self.__entities:
            entity.resetPosition()

        if self.__pacman.getLives() > 0:
            self.__pacman.respawn()

    def _render_maze(self) -> None:
        columns, rows = self.__actual_maze.getSize()

        self.__cell_size = min(
            self.__screen_width // (columns * 2 + 1),
            self.__screen_height // (rows * 2 + 1)
        )

        self.__cell_size = max(8, (self.__cell_size // 8) * 8) + 1

        if not self.__maze_renderer.is_initialized():
            self.__maze_renderer.init_maze(
                self.__actual_maze,
                self.__cell_size,
                SpriteLibrary.get('wall_skins')
            )
            self.__maze_renderer.build_maze_surface()

        self.__maze_renderer.render(self.__surface)

    def _detect_collision(self) -> None:
        pacman_pos = self.__pacman.getPos()

        for entity in self.__entities:
            if entity == self.__pacman or not self.__pacman.isAlive():
                continue
            if entity.getPos() == pacman_pos:
                if isinstance(entity, Pacgum):
                    entity.die()
                    self.__points += self.__settings.points_per_pacgum
                if isinstance(entity, SuperPacgum):
                    entity.die()
                    self.__points += self.__settings.points_per_super_pacgum
                if (
                    isinstance(entity, Ghost)
                    and entity.getMode() != GhostMode.FRIGHTENED
                ):
                    self.__pacman.die()

    def _get_entity_screen_pos(
            self,
            logical_x: float,
            logical_y: float
            ) -> tuple[float, float]:
        maze_columns, maze_rows = self.__actual_maze.getSize()

        v_maze_width = maze_columns * 2 + 1
        v_maze_height = maze_rows * 2 + 1

        original_maze_height = v_maze_height * self.__cell_size
        original_maze_width = v_maze_width * self.__cell_size

        scale_factor = self.__screen_height / original_maze_height

        scaled_cell_size = self.__cell_size * scale_factor
        scaled_maze_width = original_maze_width * scale_factor

        offset_x = (self.__screen_width - scaled_maze_width) / 2
        offset_y = 0

        v_x = logical_x * 2 + 1
        v_y = logical_y * 2 + 1

        pixel_x = offset_x + (v_x + 0.5) * scaled_cell_size
        pixel_y = offset_y + (v_y + 0.5) * scaled_cell_size

        return pixel_x, pixel_y

    def _get_42_coord(self) -> list[tuple[int, int]]:
        ft_small = [[1, 0, 0, 0, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 0, 1, 1, 1],
                    [0, 0, 1, 0, 1, 0, 0],
                    [0, 0, 1, 0, 1, 1, 1]
                    ]
        maze_w, maze_h = self.__actual_maze.getSize()
        ft_cells: list[tuple[int, int]] = []
        if len(ft_small)*2 > maze_h or len(ft_small[0])*2 > maze_w:
            return ft_cells
        posy = int((maze_h - len(ft_small)) / 2)
        posx = int((maze_w - len(ft_small[0])) / 2)
        for y in range(len(ft_small)):
            for x in range(len(ft_small[0])):
                if ft_small[y][x] == 1:
                    ft_cells.append((x + posx, y + posy))
        return ft_cells


class GameOverState(BaseState):
    def __init__(self, points: int, lives: int, time: float) -> None:
        self.__points = points

        screen_width = Settings.VIRTUAL_WINDOW_WIDTH
        screen_height = Settings.VIRTUAL_WINDOW_HEIGHT

        title = ""
        if lives <= 0 or time <= 0:
            title = "GAME OVER"
        else:
            title = "YOU WON"

        self.__game_over_txt = Text(
            title,
            (screen_width / 2, screen_height / 6),
            SpriteLibrary['yellow'],
            screen_height / 8,
            anchor='center'
        )
        line_width = 25
        line1 = "You have made".center(line_width)
        line2 = f"{points} points!".center(line_width)
        line3 = "Type your nickname here.".center(line_width)
        formatted_string = f"{line1}\n{line2}\n{line3}"
        self.__text = Text(
            formatted_string,
            (screen_width / 2, screen_height / 3),
            SpriteLibrary['yellow'],
            screen_height / 16,
            anchor='center'
            )
        self.__name_text = TextInput(
            (screen_width / 2, screen_height / 1.5),
            SpriteLibrary['white'],
            screen_height / 8,
            10
        )

        self.__elements: list[Text | TextInput] = [
            self.__text,
            self.__game_over_txt,
            self.__name_text
        ]

        self.__surface = \
            pygame.Surface(
                (Settings.VIRTUAL_WINDOW_WIDTH,
                 Settings.VIRTUAL_WINDOW_HEIGHT),
                )

    def update(self, dt: float) -> None:
        if self.__name_text.isFinished():
            name = self.__name_text.get_text()
            self._update_leadboard(name, self.__points)

        for element in self.__elements:
            if isinstance(element, LiveElement):
                element.update()

    @staticmethod
    def _update_leadboard(new_player: str, new_score: int) -> None:
        try:
            with open('data/leadboard/scores.json', 'r') as file:
                leadboard: list[tuple[str, int]] = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            leadboard = []

        leadboard.append((new_player, new_score))

        Path("data/leadboard/").mkdir(parents=True, exist_ok=True)
        path = Path("data/leadboard/scores.json")

        if path.exists():
            with open("data/leadboard/scores.json", 'w') as file:
                json.dump(leadboard, file, indent=4)
        else:
            with open("data/leadboard/scores.json", 'x') as file:
                json.dump(leadboard, file, indent=4)

        GameEvent.post(GameEvent.MODE_TO_MENU)

    def getSurface(self, dt: float) -> pygame.Surface:
        self.__surface.fill((0, 0, 0))

        for element in self.__elements:
            element.render(self.__surface)

        return self.__surface

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for element in self.__elements:
            if isinstance(element, LiveElement):
                element.handle_events(events)


class SettingState(BaseState):
    def __init__(self, settings: GameSettings) -> None:
        self.__buttons: list[Button] = []
        self.__texts: list[Text] = []
        self.__elements: list[Element] = []

        screen_width = Settings.VIRTUAL_WINDOW_WIDTH
        screen_height = Settings.VIRTUAL_WINDOW_HEIGHT

        button_size = screen_height / 30

        title = Text(
            text='settings',
            position=(screen_width / 2, screen_height / 8),
            sprite_sheet=SpriteLibrary['yellow'],
            text_size=screen_height / 10,
        )
        cheat_box = Box(
            title='cheat',
            position=(screen_width / 50, screen_height / 5),
            width=screen_width / 3,
            height=screen_height / 1.3,
            sprite_sheet=SpriteLibrary['white'],
            sprite_type=SpriteType.EMPTY_WALL,
            size=screen_height / 15,
            anchor='top left'
        )
        go_back_button = Button(
            position=(screen_width / 50, screen_height / 50),
            sprite_sheet=SpriteLibrary['yellow'],
            on_click=GameEvent.MODE_TO_MENU,
            text="go back",
            sprite_size=button_size,
            anchor='top left'
        )
        ghost_freeze_button = ToggleButton(
            position=(screen_width / 25, screen_height / 3),
            sprite_sheet=SpriteLibrary['white'],
            on_click=GameEvent.TOGGLE_FREEZE,
            text="ghost freeze",
            initial_value=settings.ghost_freezed,
            sprite_size=button_size,
            anchor='top left',
            active_sheet=SpriteLibrary['orange_green'],
            secondary_active_sheet=SpriteLibrary['white'],
        )
        invincibility_button = ToggleButton(
            position=(screen_width / 5.5, screen_height / 1.5),
            sprite_sheet=SpriteLibrary['white'],
            on_click=GameEvent.TOGGLE_INVINCIBILITY,
            text="shield",
            initial_value=settings.invincibility,
            sprite_size=button_size,
            anchor='top left',
            active_sheet=SpriteLibrary['orange_green'],
            secondary_active_sheet=SpriteLibrary['white'],
        )
        double_speed_button = ToggleButton(
            position=(screen_width / 25, screen_height / 2),
            sprite_sheet=SpriteLibrary['white'],
            on_click=GameEvent.TOGGLE_DOUBLE_SPEED,
            text="double speed",
            initial_value=settings.double_speeded,
            sprite_size=button_size,
            anchor='top left',
            active_sheet=SpriteLibrary['orange_green'],
            secondary_active_sheet=SpriteLibrary['white']
        )
        lives_button = SlideButton(
            position=(screen_width / 25, screen_height / 1.5),
            sprite_sheet=SpriteLibrary['white'],
            increment_on_click=GameEvent.ADD_A_LIFE,
            decrement_on_click=GameEvent.SUB_A_LIFE,
            initial_value=settings.lives,
            text="lives",
            sprite_size=button_size,
            anchor=' top left',
            max_value=9,
            min_value=1,
        )
        graphics_box = Box(
            title='graphics',
            position=(screen_width / 2.8, screen_height / 5),
            width=screen_width / 2,
            height=screen_height / 1.3,
            sprite_sheet=SpriteLibrary['white'],
            sprite_type=SpriteType.EMPTY_WALL,
            size=screen_height / 15,
            anchor='top left'
        )
        toggle_fullscreen = ToggleButton(
            position=(screen_width / 2.5, screen_height / 3),
            sprite_sheet=SpriteLibrary['white'],
            on_click=GameEvent.TOGGLE_FULLSCREEN,
            text="toggle\nfullscreen",
            sprite_size=button_size,
            initial_value=pygame.display.is_fullscreen(),
            anchor='top left',
            active_sheet=SpriteLibrary['orange_green'],
            secondary_active_sheet=SpriteLibrary['white']
        )
        fps_slider = SlideButton(
            position=(screen_width / 1.55, screen_height / 3),
            sprite_sheet=SpriteLibrary['white'],
            increment_on_click=GameEvent.ADD_10_FPS,
            decrement_on_click=GameEvent.SUB_10_FPS,
            initial_value=pygame.display.get_desktop_refresh_rates()[0],
            text="  fps  ",
            sprite_size=button_size,
            anchor=' top left',
            step_value=10,
            max_value=200,
            min_value=10,
        )
        toggle_crt = ToggleButton(
            position=(screen_width / 1.67, screen_height / 2.05),
            sprite_sheet=SpriteLibrary['white'],
            on_click=GameEvent.TOGGLE_CRT_EFFECT,
            text="set crt effect",
            sprite_size=button_size,
            initial_value=True,
            anchor='mid top',
            active_sheet=SpriteLibrary['orange_green'],
            secondary_active_sheet=SpriteLibrary['white']
        )
        toggle_glitch = ToggleButton(
            position=(screen_width / 1.67, screen_height / 1.67),
            sprite_sheet=SpriteLibrary['white'],
            on_click=GameEvent.TOGGLE_GLITCH_EFFECT,
            text="set glitch vfx",
            sprite_size=button_size,
            initial_value=True,
            anchor='mid top',
            active_sheet=SpriteLibrary['orange_green'],
            secondary_active_sheet=SpriteLibrary['white']
        )
        toggle_glow = ToggleButton(
            position=(screen_width / 1.67, screen_height / 1.41),
            sprite_sheet=SpriteLibrary['white'],
            on_click=GameEvent.TOGGLE_GLOW_EFFECT,
            text="set glow vfx",
            sprite_size=button_size,
            initial_value=True,
            anchor='mid top',
            active_sheet=SpriteLibrary['orange_green'],
            secondary_active_sheet=SpriteLibrary['white']
        )
        toggle_rolling = ToggleButton(
            position=(screen_width / 1.67, screen_height / 1.22),
            sprite_sheet=SpriteLibrary['white'],
            on_click=GameEvent.TOGGLE_ROLLING_EFFECT,
            text="set rolling vfx",
            sprite_size=button_size,
            initial_value=True,
            anchor='mid top',
            active_sheet=SpriteLibrary['orange_green'],
            secondary_active_sheet=SpriteLibrary['white']
        )

        self.__texts = [
            title,
        ]
        self.__elements = [
            cheat_box,
            graphics_box,
        ]
        self.__buttons = [
            ghost_freeze_button,
            double_speed_button,
            go_back_button,
            lives_button,
            invincibility_button,
            toggle_fullscreen,
            fps_slider,
            toggle_crt,
            toggle_glitch,
            toggle_glow,
            toggle_rolling,
        ]

        self.__surface = pygame.Surface((screen_width, screen_height))

    def getSurface(self, dt: float) -> pygame.Surface:
        self.__surface.fill((0, 0, 0))
        for element in self.__elements + self.__buttons + self.__texts:
            element.render(self.__surface)
        return self.__surface

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.__buttons:
                button.handle_event(event)

    def update(self, dt: float) -> None:
        pass
