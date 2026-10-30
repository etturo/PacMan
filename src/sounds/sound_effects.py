"""Define the sound effects module."""

import wave
from pathlib import Path

import pygame


class SoundEffect:
    """Represent the SoundEffect component."""

    def __init__(self, file_path: str) -> None:
        """Initialize the component."""
        path = Path(file_path)
        if not path.exists():
            file_path = str(path.parents[1] / "classic" / path.name)
        if self._is_empty(file_path):
            self.sound = pygame.mixer.Sound(buffer=bytes(4))
        else:
            self.sound = pygame.mixer.Sound(file_path)
        self.sound.set_volume(1)

    @staticmethod
    def _is_empty(file_path: str) -> bool:
        """Perform the _is_empty operation."""
        try:
            with wave.open(file_path, "rb") as wav:
                return wav.getnframes() == 0
        except wave.Error:
            return False

    def setVolume(self, volume_perc: int) -> None:
        """Perform the setVolume operation."""
        self.sound.set_volume(volume_perc / 100)

    def play(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        """Perform the play operation."""
        self.sound.play(loops, maxtime, fade_ms)

    def playOn(self, channel: pygame.mixer.Channel, loops: int = 0) -> None:
        """Play on the given channel, cutting what it was playing."""
        channel.play(self.sound, loops)

    def stop(self) -> None:
        """Perform the stop operation."""
        self.sound.stop()

    def getLength(self) -> float:
        """Return the sound duration in seconds."""
        return self.sound.get_length()
