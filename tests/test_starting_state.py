import unittest

import pygame

from src.core.game import Game
from src.core.game_state import StartingState, MenuState
from src.utils.settings import GameEvent


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


if __name__ == "__main__":
    unittest.main()
