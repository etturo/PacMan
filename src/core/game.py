from argparse import ArgumentParser

import pygame

from src.core.game_state import (
    BaseState,
    StartingState,
    MenuState,
    PlayingState
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

        # GAME SETTINGS
        self.__is_running: bool = True
        self.__fps: int = 60
        self.__clock = pygame.time.Clock()
        self.__actual_level: int = 0
        self.__game_settings: GameSettings
        self.__active_state: BaseState = StartingState()

        # SIMULATION UTILS
        self.__quit_buttons: list[int] = [
            pygame.K_q,
            pygame.QUIT
        ]

        # PYGAME ATTRIBUTES

        # RENDER UTILS
        self.__screen_manager: ScreenManager = ScreenManager()

        # SOUNDS UILS

        # WORLD ATTRIBUTES
        self.__maze: Maze
        self.__mazegen: MazeWrapper = MazeWrapper()

    def run(self) -> None:
        try:
            while self.__is_running:
                dt = self.__clock.tick(self.__fps) / 1000.0
                events = pygame.event.get()
                self._catch_events(events)
                self.__active_state.handle_events(events)
                self.__active_state.update(dt)
                self._render()
        except KeyboardInterrupt:
            exit("\nProgram ended by the user")
            pygame.quit()
        exit()
        pygame.quit()

    def _render(self) -> None:
        self.__screen_manager.render(
            surface=self.__active_state.getSurface(),
            crt=True
        )

    def _catch_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            # Quit program conditions
            if (event.type == pygame.QUIT or
                    event.type == GameEvent.EXIT or
                    event.type == pygame.KEYDOWN and
                    event.key in self.__quit_buttons):
                self.__is_running = False

            elif event.type == GameEvent.MODE_TO_STARTING:
                self.__active_state = StartingState()

            elif event.type == GameEvent.MODE_TO_MENU:
                self.__active_state = MenuState()

            elif event.type == GameEvent.MODE_TO_PLAYING:
                self.__active_state = PlayingState(self.__game_settings)

            # elif event.type == GameEvent.MODE_TO_SCORES:
            #     self.__active_state = ScoresState()

            # elif event.type == GameEvent.MODE_TO_SETTINGS:
            #     self.__active_state = SettingsState()

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
