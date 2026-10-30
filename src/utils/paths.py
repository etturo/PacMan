"""Define the paths module."""

import os
import sys
from pathlib import Path

highscore_filename = "scores.json"


def resource_path(relative_path: str) -> Path:
    """Perform the resource_path operation."""
    base_path = Path(getattr(
        sys, "_MEIPASS",
        Path(__file__).resolve().parents[2])
        )
    return base_path / relative_path


def config_path() -> Path:
    """Perform the config_path operation."""
    return resource_path("config.json")


def leaderboard_path() -> Path:
    """Perform the leaderboard_path operation."""
    if os.name == "nt":
        data_root = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    else:
        data_root = Path(
            os.environ.get(
                "XDG_DATA_HOME",
                Path.home() / ".local" / "share"
                )
            )
    return data_root / "Pacman" / highscore_filename


def initial_leaderboard_path() -> Path:
    """Perform the initial_leaderboard_path operation."""
    return resource_path("data/leadboard/scores.json")
