import random
import pygame

from typing import cast

from src.sounds.sound_effects import SoundEffect
from src.sounds.sound_set import SoundSet

from src.utils.paths import resource_path

class SoundLibrary:
    sounds: dict[str, SoundSet] = {}
    current: dict[str, SoundEffect] = {}
    chomp_channel: pygame.mixer.Channel
    loop_channel: pygame.mixer.Channel

    @classmethod
    def load(cls) -> None:
        cls.sounds = {
            "classic": SoundSet("classic")
        }
        cls.pick()
        pygame.mixer.set_reserved(2)
        cls.chomp_channel = pygame.mixer.Channel(0)
        cls.loop_channel = pygame.mixer.Channel(1)

    @classmethod
    def get(cls, key: str) -> SoundEffect:
        """Return the currently selected variant for key."""
        return cls.current[key]

    @classmethod
    def pick(cls) -> None:
        """Pick one random variant per sound, kept until the next pick."""
        n = cls.sounds["classic"].getLen()
        # seleziono prima un set per ogni chiave
        selected = \
            [random.choice(list(cls.sounds.keys())) for _ in range(n)]
        # poi prendiamo la chiave giusta da quel set
        for i, k in enumerate(cls.sounds["classic"].getKeys()):
            cls.current[k] = cls.sounds[selected[i]].getSound(k)
