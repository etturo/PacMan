import pygame


class SoundEffects:
    def __init__(self) -> None:
        # TODO change the mp3 file, has not to be in the temp folder
        pygame.mixer.init()

        self.intro_music = pygame.mixer.Sound('temp/pac-man-startup.mp3')
        self.intro_music.set_volume(0.05)
