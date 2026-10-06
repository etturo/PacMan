import pygame


class SoundEffect:
    def __init__(self, file_path: str) -> None:
        self.sound = pygame.mixer.Sound(file_path)
        self.sound.set_volume(1)

    def setVolume(self, volume_perc: int) -> None:
        self.sound.set_volume(volume_perc / 100)

    def play(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        self.sound.play(loops, maxtime, fade_ms)

    def playOn(self, channel: pygame.mixer.Channel) -> None:
        """Play on the given channel, cutting what it was playing."""
        channel.play(self.sound)

    def stop(self) -> None:
        self.sound.stop()
