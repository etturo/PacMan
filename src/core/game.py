from enum import Enum, auto

import pygame

from src.world.maze import Maze
from src.graphics.renderer import Renderer
from src.world.maze_wrapper import MazeWrapper


class Game:
    class Mode(Enum):
        MAIN_MENU = auto()
        SETTINGS_MENU = auto()
        PAUSED = auto()
        GAME_OVER = auto()

    # GAME SETTINGS
    __is_running = True
    __fps = 60

    # SIMULATION UTILS
    __quit_buttons = [
        pygame.K_q,
        pygame.QUIT
    ]

    # PYGAME ATTRIBUTES
    __screen: pygame.Surface
    __clock: pygame.time.Clock

    # RENDER UTILS
    __renderer = Renderer()

    # WORLD ATTRIBUTES
    __maze: Maze
    __mazegen: MazeWrapper

    @classmethod
    def _init(cls) -> None:
        cls.__clock = pygame.time.Clock()

    @classmethod
    def run(cls) -> None:
        cls._init()

        cls.__mazegen = MazeWrapper()

        cls.__mazegen.generate((25, 25), 0)
        cls.__maze = cls.__mazegen.maze

        print(cls.__maze)

        try:
            while cls.__is_running:
                cls._catch_events()
                cls._update_logic()
                cls._render_graphics()
                # cls.__renderer.updateFrame()
                cls.__clock.tick(60)
        except KeyboardInterrupt:
            exit("\nProgram ended by the user")

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
