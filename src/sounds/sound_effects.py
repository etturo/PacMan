import pygame


class SoundEffect:
    def __init__(self, file_path: str) -> None:
        self.intro_music = pygame.mixer.Sound(file_path)
        self.intro_music.set_volume(0.05)

    def play(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        self.intro_music.play(loops, maxtime, fade_ms)

    def stop(self) -> None:
        self.intro_music.stop()
