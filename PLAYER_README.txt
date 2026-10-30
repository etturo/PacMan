PACMAN

Start the game by opening the Pacman executable. To use another config file:
    ./Pacman path/to/config.json

CONTROLS
  Arrows or WASD   move
  P                pause
  F11              fullscreen
  Esc              quit

RULES
  Eat every gum to clear the level, and clear every level to win.
  Big gums in the corners make the ghosts edible for a short time.
  Touching a ghost or running out of time costs a life.

OPTIONS (menu > Settings)
  Graphics: fullscreen, FPS, CRT, glitch, glow and rolling effects.
  Sound: choose a sound set or a random one.
  Cheats: ghost freeze, double speed, lives, shield, level skip.
  With level skip on, press N during the game to go to the next level.
  Scores made with cheats are not saved.

CONFIGURATION
  Edit config.json, next to the executable, then restart the game.
  Lines starting with # are comments. Invalid values fall back to the default.

  highscore_filename       score file name
  levels                   list of {"width": 3-100, "height": 3-100}
  lives                    starting lives, 1-99
  points_per_pacgum        points for a gum
  points_per_super_pacgum  points for a big gum, above points_per_pacgum
  points_per_ghost         points for the first ghost of a streak
  seed                     first level maze, 0 means random
  level_max_time           seconds for each level
  fps                      10-200
