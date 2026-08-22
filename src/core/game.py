from argparse import ArgumentParser

import pygame

from src.world.maze import Maze
from src.world.maze_wrapper import MazeWrapper

from src.graphics.renderer import Renderer
from src.graphics.graphical_utils.sprite_library import SpriteLibrary

from src.utils.models import BaseSettings, ParsingError
from src.utils.settings import GameMode
from src.utils.parser import SettingParser

from src.sounds.sound_effects import SoundEffect

class Game:
    # GAME SETTINGS
    __is_running = True
    __fps = 60
    __actual_level: int = 0
    __game_settings: BaseSettings
    __game_mode: GameMode

    # SIMULATION UTILS
    __quit_buttons = [
        pygame.K_q,
        pygame.QUIT
    ]

    # PYGAME ATTRIBUTES
    pygame.mixer.init()
    __screen: pygame.Surface
    __clock: pygame.time.Clock

    # RENDER UTILS
    __renderer: Renderer

    # SOUNDS UILS
    __sounds: SoundEffect
    __has_intro_played = False

    # WORLD ATTRIBUTES
    __maze: Maze
    __mazegen: MazeWrapper

    @classmethod
    def _init(cls) -> None:
        cls._load_config_file()

        cls.__clock = pygame.time.Clock()
        cls.__game_mode = GameMode.STARTING

        cls.__renderer = Renderer()
        cls.__sound = SoundEffect()

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
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                cls.__is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in cls.__quit_buttons:
                    cls.__is_running = False

                if cls.__game_mode == GameMode.STARTING:
                    if event.key == pygame.K_RETURN:
                        cls.__game_mode = GameMode.MAIN_MENU
                        cls.__sounds.intro_music.stop()

        if cls.__game_mode == GameMode.MAIN_MENU:
            cls.__renderer.handle_menu_events(events)

    @classmethod
    def _update_logic(cls) -> None:
        ...

    @classmethod
    def _render_graphics(cls) -> None:
        if cls.__game_mode == GameMode.STARTING and not cls.__has_intro_played:
            cls.__sounds.intro_music.play()
            cls.__has_intro_played = True
        cls.__renderer.render(
            cls.__maze,
            cls.__game_mode
            )

    @classmethod
    def getGameMode(cls) -> GameMode:
        return cls.__game_mode

    @classmethod
    def setGameMode(cls, game_mode: GameMode) -> None:
        cls.__game_mode = game_mode

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
