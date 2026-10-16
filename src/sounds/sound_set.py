from src.sounds.sound_effects import SoundEffect
from src.utils.paths import resource_path


class SoundSet:
    def __init__(self, owner: str) -> None:
        self.__owner_name: str = owner

        self.__sounds: dict[str, SoundEffect] = {
            "button": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/button.wav"))
            ),
            "ed0": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/ed0.wav"))
            ),
            "ed1": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/ed1.wav"))
            ),
            "eyes": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/eyes.wav"))
            ),
            "fright": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/fright.wav"))
            ),
            "ghost_death": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/ghost_death.wav"))
            ),
            "ghost_move": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/ghost_move.wav"))
            ),
            "intro": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/intro.mp3"))
            ),
            "pacman_death": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/pacman_death.wav"))
            ),
            "pacman_intermission": SoundEffect(
                str(resource_path(
                    f"data/assets/sounds/classic/pacman_intermission.wav"
                ))
            ),
            "super_pacgum": SoundEffect(
                str(resource_path(f"data/assets/sounds/{owner}/super_pacgum.wav"))
            ),
        }

    def getSound(self, sound_name: str) -> SoundEffect:
        return self.__sounds[sound_name]

    def getLen(self) -> int:
        return len(self.__sounds)

    def getKeys(self) -> list[str]:
        return self.__sounds.keys()
