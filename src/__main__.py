"""Provide the command-line entry point for PacMan."""

import sys

from src.core.game import Game


def main() -> None:
    """Start the game using the configuration file from the command line."""
    try:
        if len(sys.argv) != 2:
            sys.exit("The argument should be one.")
        game = Game(sys.argv[1])
        game.run()
    except Exception as e:
        print(e)
        sys.exit("u u, fatal error.")


if __name__ == "__main__":
    main()
