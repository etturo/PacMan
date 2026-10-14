import random
import pygame

from typing import cast

from src.sounds.sound_effects import SoundEffect

from src.utils.paths import resource_path


class SoundLibraryMeta(type):
    def __getitem__(cls, key: str) -> SoundEffect:
        current = cast(
            dict[str, SoundEffect],
            getattr(cls, 'current', {})
        )
        return current[key]


class SoundLibrary(metaclass=SoundLibraryMeta):
    sounds: dict[str, list[SoundEffect]] = {}
    current: dict[str, SoundEffect] = {}
    chomp_channel: pygame.mixer.Channel
    loop_channel: pygame.mixer.Channel

    @classmethod
    def load(cls) -> None:
        cls.sounds = {
            "intro":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/pac-man-startup.mp3'
                        )),
                ),
            ],
            "death":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/pacman_death.wav'
                        )),
                ),
            ],
            "eat_ghost":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/pacman_eatghost.wav'
                        )),
                ),
            ],
            "eat_fruit":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/pacman_eatfruit.wav'
                        )),
                ),
            ],
            "extra_pac":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/pacman_extrapac.wav'
                        )),
                ),
            ],
            "intermission":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/pacman_intermission.wav'
                        )),
                ),
            ],
            "credit":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/credit.wav'
                        )),
                ),
            ],
            "ed0":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/eat_dot_0.wav'
                        )),
                ),
            ],
            "ed1":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/eat_dot_1.wav'
                        )),
                ),
            ],
            "siren":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/siren0.wav'
                        )),
                ),
            ],
            "fright":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/fright.wav'
                        )),
                ),
            ],
            "eyes":
            [
                SoundEffect(
                    str(resource_path(
                        'data/assets/sounds/eyes.wav'
                        )),
                ),
            ]
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
        cls.current = {k: random.choice(v) for k, v in cls.sounds.items()}
