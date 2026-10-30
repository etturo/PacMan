"""Define the PacMan package metadata and public API."""

__version__ = "1.4.2"
__authors__ = "aflorea/eturini"

from .core.game import Game

__all__ = ["Game", "__version__", "__authors__"]
