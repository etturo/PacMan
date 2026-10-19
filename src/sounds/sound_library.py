import random
import pygame

from src.sounds.sound_effects import SoundEffect
from src.sounds.sound_set import SoundSet

from src.utils.paths import resource_path

class SoundLibrary:
    sounds: dict[str, SoundSet] = {}
    current: dict[str, SoundEffect] = {}
    current_set_name: str = "classic"
    random_mode: bool = False
    chomp_channel_0: pygame.mixer.Channel
    chomp_channel_1: pygame.mixer.Channel
    loop_channel: pygame.mixer.Channel
    special_channel: pygame.mixer.Channel
    death_channel: pygame.mixer.Channel

    @classmethod
    def load(cls) -> None:
        cls.sounds = {
            "classic": SoundSet("classic"),
            "lmongili": SoundSet("lmongili")
        }
        cls.current_set_name = "classic"
        cls._use_set("classic")
        cls.random_mode = False
        pygame.mixer.set_reserved(5)
        cls.chomp_channel_0 = pygame.mixer.Channel(0)
        cls.chomp_channel_1 = pygame.mixer.Channel(1)
        cls.loop_channel = pygame.mixer.Channel(2)
        cls.special_channel = pygame.mixer.Channel(3)
        cls.death_channel = pygame.mixer.Channel(4)

    @classmethod
    def get(cls, key: str) -> SoundEffect:
        """Return the currently selected variant for key."""
        return cls.current[key]

    @classmethod
    def getCurrentSetName(cls) -> str:
        return cls.current_set_name

    @classmethod
    def isRandomMode(cls) -> bool:
        return cls.random_mode

    @classmethod
    def _use_set(cls, set_name: str) -> None:
        cls.current_set_name = set_name
        sound_set = cls.sounds[set_name]
        cls.current = {
            key: sound_set.getSound(key)
            for key in sound_set.getKeys()
        }

    @classmethod
    def nextSet(cls, set_name: str | None = None) -> None:
        if cls.random_mode:
            return
        set_names = list(cls.sounds)
        set_name = set_name or cls.current_set_name
        next_index = (set_names.index(set_name) + 1) % len(set_names)
        cls._use_set(set_names[next_index])

    @classmethod
    def prevSet(cls, set_name: str | None = None) -> None:
        if cls.random_mode:
            return
        set_names = list(cls.sounds)
        set_name = set_name or cls.current_set_name
        previous_index = (set_names.index(set_name) - 1) % len(set_names)
        cls._use_set(set_names[previous_index])

    @classmethod
    def pick(cls) -> None:
        """Enable random mode and pick each sound independently."""
        cls.random_mode = True
        sound_sets = list(cls.sounds.values())
        keys = next(iter(sound_sets)).getKeys()
        cls.current = {
            key: random.choice(sound_sets).getSound(key)
            for key in keys
        }

    @classmethod
    def toggleRandom(cls) -> None:
        """Toggle random mode, allowing manual set selection when disabled."""
        if cls.random_mode:
            cls.random_mode = False
            cls._use_set(cls.current_set_name)
        else:
            cls.pick()
