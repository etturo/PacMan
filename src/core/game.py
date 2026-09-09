from argparse import ArgumentParser

import pygame

from src.core.game_state import (
    BaseState,
    StartingState,
    MenuState,
    PlayingState,
    GameOverState,
    SettingState,
    PauseState,
    )

from src.world.maze import Maze
from src.world.maze_wrapper import MazeWrapper

from src.graphics.screen_manager import ScreenManager

from src.utils.models import GameSettings, ParsingError
from src.utils.settings import GameEvent
from src.utils.parser import SettingParser


class Game:
    def __init__(self) -> None:
        self._load_config_file()

        # RENDER UTILS
        self.__screen_manager: ScreenManager = ScreenManager()
        self.__is_crt = True
        self.__is_glow = True
        self.__is_glitch = True
        self.__is_rolling = True

        # GAME SETTINGS
        self.__is_running: bool = True
        self.__fps: int = 60
        self.__clock = pygame.time.Clock()
        self.__actual_level: int = 0
        self.__game_settings: GameSettings
        self.__active_state: BaseState = StartingState()

        # SIMULATION UTILS
        self.__quit_buttons: list[int] = [
            pygame.K_ESCAPE,
            pygame.QUIT
        ]

        # PYGAME ATTRIBUTES

        # SOUNDS UILS

        # WORLD ATTRIBUTES
        self.__maze: Maze
        self.__mazegen: MazeWrapper = MazeWrapper()

    def run(self) -> None:
        try:
            while self.__is_running:
                self.__dt = self.__clock.tick(self.__fps) / 1000.0
                events = pygame.event.get()
                self._catch_events(events)
                self.__active_state.handle_events(events)
                self.__active_state.update(self.__dt)
                self._render(self.__dt)
        except KeyboardInterrupt:
            exit("\nProgram ended by the user")
            pygame.quit()
        exit()
        pygame.quit()

    def _render(self, dt: float) -> None:
        self.__screen_manager.render(
            surface=self.__active_state.getSurface(dt),
            crt=self.__is_crt,
            glow=self.__is_glow,
            glitch=self.__is_glitch,
            rolling=self.__is_rolling,
        )

    def _catch_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            # Quit program conditions
            if (event.type == pygame.QUIT or
                    event.type == GameEvent.EXIT or
                    event.type == pygame.KEYDOWN and
                    event.key in self.__quit_buttons):
                self.__is_running = False
                exit()

            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_F11):
                pygame.display.toggle_fullscreen()

            elif event.type == GameEvent.MODE_TO_STARTING:
                self.__active_state = StartingState()

            elif event.type == GameEvent.MODE_TO_MENU:
                self.__active_state = MenuState()

            elif event.type == GameEvent.MODE_TO_PAUSE:
                self.__freeze_state = self.__active_state
                self.__active_state = PauseState()

            elif event.type == GameEvent.BACK_TO_GAME:
                self.__active_state = self.__freeze_state

            elif event.type == GameEvent.MODE_TO_PLAYING:
                self.__active_state = PlayingState(self.__game_settings)

            elif event.type == GameEvent.MODE_TO_SETTINGS:
                self.__active_state = SettingState(self.__game_settings)

            elif event.type == GameEvent.MODE_TO_GAME_OVER:
                # only with no cheat activated the score can be stored
                if (
                    self.__game_settings.ghost_freezed |
                    self.__game_settings.double_speeded |
                    self.__game_settings.invincibility
                ):
                    self.__active_state = MenuState()
                else:
                    points = self.__active_state.getPoints()
                    self.__active_state = GameOverState(points, False)
            elif event.type == GameEvent.MODE_TO_WIN:
                # only with no cheat activated the score can be stored
                if (
                    self.__game_settings.ghost_freezed |
                    self.__game_settings.double_speeded |
                    self.__game_settings.invincibility
                ):
                    self.__active_state = MenuState()
                else:
                    points = self.__active_state.getPoints()
                    self.__active_state = GameOverState(points, True)

            elif (
                event.type == GameEvent.ADD_A_LIFE and
                self.__game_settings.lives < 9
            ):
                self.__game_settings.lives += 1
            elif (
                event.type == GameEvent.SUB_A_LIFE and
                self.__game_settings.lives > 1
            ):
                self.__game_settings.lives -= 1

            elif event.type == GameEvent.TOGGLE_FREEZE:
                self.__game_settings.ghost_freezed = \
                    not self.__game_settings.ghost_freezed
            elif event.type == GameEvent.TOGGLE_DOUBLE_SPEED:
                self.__game_settings.double_speeded = \
                    not self.__game_settings.double_speeded
            elif event.type == GameEvent.TOGGLE_INVINCIBILITY:
                self.__game_settings.invincibility = \
                    not self.__game_settings.invincibility

            elif event.type == GameEvent.TOGGLE_FULLSCREEN:
                pygame.display.toggle_fullscreen()
            elif event.type == GameEvent.SUB_10_FPS:
                if self.__fps > 10:
                    self.__fps -= 10
            elif event.type == GameEvent.ADD_10_FPS:
                if self.__fps < 200:
                    self.__fps += 10
            elif event.type == GameEvent.TOGGLE_CRT_EFFECT:
                self.__is_crt = not self.__is_crt
            elif event.type == GameEvent.TOGGLE_GLOW_EFFECT:
                self.__is_glow = not self.__is_glow
            elif event.type == GameEvent.TOGGLE_GLITCH_EFFECT:
                self.__is_glitch = not self.__is_glitch
            elif event.type == GameEvent.TOGGLE_ROLLING_EFFECT:
                self.__is_rolling = not self.__is_rolling

    def _load_config_file(self) -> None:
        arg_parser = ArgumentParser(
            prog="PacMan",
            description="Clone of the legendary retro game."
            )
        arg_parser.add_argument("config_file")
        args = arg_parser.parse_args()

        parser = SettingParser()
        try:
            self.__game_settings = parser.parse(args.config_file)
        except ParsingError as exc:
            raise SystemExit(str(exc)) from exc
