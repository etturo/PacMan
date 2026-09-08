import unittest

import pygame

from src.core.game import Game
from src.core.game_state import StartingState, MenuState, PlayingState
from src.entities.ghost import Ghost
from src.entities.ghost_intelligence import GhostMode, blinky_strategy
from src.entities.pacman import Pacman
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.utils.settings import GameEvent
from src.world.cell import Direction


class TestStartingState(unittest.TestCase):
    def test_render_accepts_surface_and_does_not_crash(self):
        pygame.init()
        try:
            state = StartingState()
            state.update()
            surface = state.getSurface()
            self.assertIsInstance(surface, pygame.Surface)
        finally:
            pygame.quit()

    def test_menu_state_returns_surface(self):
        pygame.init()
        try:
            state = MenuState()
            surface = state.getSurface()
            self.assertIsInstance(surface, pygame.Surface)
        finally:
            pygame.quit()

    def test_game_loop_consumes_menu_event_from_starting_state(self):
        pygame.init()
        try:
            class DummyScreenManager:
                def render(self, surface, crt=True):
                    pass

            class DummyState:
                def getSurface(self):
                    return pygame.Surface((10, 10))

                def handle_events(self, events):
                    pygame.event.post(pygame.event.Event(GameEvent.MODE_TO_MENU))

                def update(self):
                    game._Game__is_running = False

            game = object.__new__(Game)
            game._Game__is_running = True
            game._Game__screen_manager = DummyScreenManager()
            game._Game__active_state = DummyState()

            game.run()

            self.assertIsInstance(game._Game__active_state, MenuState)
        finally:
            pygame.quit()

    def test_ghost_resets_position_after_death_animation(self):
        SpriteLibrary.load()

        ghost = Ghost(
            init_pos=(3, 4),
            size=16,
            speed=2.0,
            sprite_sheet=SpriteLibrary['yellow'],
            strategy=blinky_strategy,
        )
        ghost.setMode(GhostMode.FRIGHTENED)
        ghost.moveTo((3, 4), Direction.STILL)
        ghost.die(200)

        self.assertFalse(ghost.isAlive())
        self.assertEqual(ghost.getPos(), (3, 4))

        for _ in range(10):
            ghost.update(0.1)
            self.assertFalse(ghost.isAlive())

        ghost.update(0.1)
        self.assertTrue(ghost.isAlive())
        self.assertEqual(ghost.getPos(), (3, 4))

    def test_dead_ghost_in_same_cell_does_not_trigger_collision_again(self):
        pacman = Pacman((3, 4), 12, 4.0)
        ghost = Ghost(
            init_pos=(3, 4),
            size=12,
            speed=2.0,
            sprite_sheet=SpriteLibrary['yellow'],
            strategy=blinky_strategy,
        )
        ghost.die(200)

        state = object.__new__(PlayingState)
        state._PlayingState__pacman = pacman
        state._PlayingState__entities = [pacman, ghost]
        state._PlayingState__points = 0
        state._PlayingState__ghost_combo = 200
        state._PlayingState__settings = type(
            'DummySettings',
            (),
            {'points_per_ghost': 400, 'points_per_pacgum': 10,
             'points_per_super_pacgum': 50}
        )()

        state._detect_collision()

        self.assertEqual(state._PlayingState__points, 0)
        self.assertFalse(ghost.isAlive())


if __name__ == "__main__":
    unittest.main()
