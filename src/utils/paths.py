import os
import sys
from pathlib import Path


def resource_path(relative_path: str) -> Path:
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base_path / relative_path


def config_path() -> Path:
    return resource_path("config.json")


def leaderboard_path() -> Path:
    if os.name == "nt":
        data_root = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    else:
        data_root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return data_root / "BarkMan" / "scores.json"


def initial_leaderboard_path() -> Path:
    return resource_path("data/leadboard/scores.json")