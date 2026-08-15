from enum import Enum, auto
from argparse import ArgumentParser

import pygame

from src.world.maze import Maze
from src.world.maze_wrapper import MazeWrapper

from src.graphics.renderer import Renderer

from src.utils.models import BaseSettings, ParsingError
from src.utils.parser import SettingParser


class Game:
    class Mode(Enum):
        MAIN_MENU = auto()
        SETTINGS_MENU = auto()
        PAUSED = auto()
        GAME_OVER = auto()

    # GAME SETTINGS
    __is_running = True
    __fps = 60
    __actual_level: int = 0

    # SIMULATION UTILS
    __quit_buttons = [
        pygame.K_q,
        pygame.QUIT
    ]

    # PYGAME ATTRIBUTES
    __screen: pygame.Surface
    __clock: pygame.time.Clock

    # RENDER UTILS
    __renderer: Renderer

    # WORLD ATTRIBUTES
    __maze: Maze
    __mazegen: MazeWrapper

    @classmethod
    def _init(cls) -> None:
        cls._load_config_file()

        cls.__clock = pygame.time.Clock()
        cls.__game_settings: BaseSettings

        cls.__renderer = Renderer()

        cls.__mazegen = MazeWrapper()

    @classmethod
    def run(cls) -> None:
        cls._init()

        cls._generate_new_level()

        try:
            while cls.__is_running:
                cls._catch_events()
                cls._update_logic()
                cls._render_graphics()
                cls.__clock.tick(cls.__fps)
        except KeyboardInterrupt:
            exit("\nProgram ended by the user")
        finally:
            pygame.quit()

    @classmethod
    def _catch_events(cls) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cls.__is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in cls.__quit_buttons:
                    cls.__is_running = False

    @classmethod
    def _update_logic(cls) -> None:
        ...

    @classmethod
    def _render_graphics(cls) -> None:
        cls.__renderer.render(cls.__maze)

    @classmethod
    def _load_config_file(cls) -> None:
        arg_parser = ArgumentParser(
            prog="PacMan",
            description="Clone of the legendary retro game."
            )
        arg_parser.add_argument("config_file")
        args = arg_parser.parse_args()

        parser = SettingParser()
        try:
            cls.__game_settings = parser.parse(args.config_file)
        except ParsingError as exc:
            raise SystemExit(str(exc)) from exc

    @classmethod
    def _generate_new_level(cls) -> None:
        maze_size = (
            cls.__game_settings.levels[cls.__actual_level].width,
            cls.__game_settings.levels[cls.__actual_level].height
        )
        cls.__mazegen.generate(
            maze_size,
            cls.__game_settings.seed
        )
        cls.__maze = cls.__mazegen.maze

    # @classmethod
    # def _handle_main_menu(cls) -> None:
