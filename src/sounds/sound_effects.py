import pygame


class SoundEffect:
    def __init__(self, file_path: str) -> None:

        self.intro_music = pygame.mixer.Sound(file_path)
        self.intro_music.set_volume(0.05)
