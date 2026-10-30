import sys

from src.core.game import Game

def main():
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
