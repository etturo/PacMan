from typing import Optional, cast

import pygame

from src.sounds.sound_effects import SoundEffect

from src.utils.paths import resource_path


class SoundLibraryMeta(type):
    def __getitem__(cls, key: str) -> SoundEffect:
        sounds = cast(
            dict[str, SoundEffect],
            getattr(cls, 'sprites', {})
        )
        if key in sounds:
            return sounds[key]

        default = getattr(cls, '_SoundLibrary__default_sound', None)
        if default is not None:
            return cast(SoundEffect, default)
        raise KeyError(key)


class SoundLibrary(metaclass=SoundLibraryMeta):
    sounds: dict[str, SoundEffect] = {}

    @classmethod
    def load(cls) -> None:
        cls.sounds = {
            "intro" : SoundEffect(
                str(resource_path(
                    'data/assets/sounds/pac-man-startup.mp3'))
            )
        }

    @classmethod
    def get(cls, key: str) -> SoundEffect:
        if key in cls.sounds.keys():
            return cls.sounds[key]
        raise KeyError(key)
