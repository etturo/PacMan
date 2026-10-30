"""Define the train module."""

import os
import sys

import pygame

from src.ai.agent import QAgent
from src.core.game_state import PlayingState
from src.graphics.graphical_utils.sprite_library import SpriteLibrary
from src.sounds.sound_library import SoundLibrary
from src.utils.models import GameSettings
from src.utils.parser import SettingParser
from src.utils.settings import GameEvent

EPISODES = 200
DT = 1 / 30
WEIGHTS_PATH = 'data/ai/weights.json'
END_EVENTS = (
    GameEvent.RESET_POSITIONS,
    GameEvent.MODE_TO_GAME_OVER,
    GameEvent.MODE_TO_WIN,
)


def _init_headless() -> None:
    """Perform the _init_headless operation."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode((1, 1))
    SoundLibrary.load()
    SpriteLibrary.load()
    SpriteLibrary.add_item('title', 'white_text')
    SpriteLibrary.add_item('wall_skins', 'blue')
    SpriteLibrary.add_item('leadboard', 'pink_black')
    SpriteLibrary.add_item('eyes', 'black')


def _play_episode(settings: GameSettings, agent: QAgent) -> int:
    """Perform the _play_episode operation."""
    state = PlayingState(settings, agent)
    while True:
        state.update(DT)
        for event in pygame.event.get():
            if event.type in END_EVENTS:
                died = event.type != GameEvent.MODE_TO_WIN
                agent.final(state.getPacmanContext(), died)
                return state.getPoints()


def main() -> None:
    """Train the AI player without a window, then save its weights."""
    _init_headless()
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    settings = SettingParser().parse(config_file)
    settings.seed = 0
    agent = QAgent(training=True)

    scores: list[int] = []
    for episode in range(1, EPISODES + 1):
        scores.append(_play_episode(settings, agent))
        if episode % 10 == 0:
            average = sum(scores[-10:]) / 10
            print(f"Episode {episode}: average points {average:.0f}")

    agent.save(WEIGHTS_PATH)
    print(f"Weights saved in {WEIGHTS_PATH}")


if __name__ == "__main__":
    main()
