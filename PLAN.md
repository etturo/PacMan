# CLASSES:
- `Game`: manages display and timing.

- `Entity` (`pygame.sprite.Sprite`): holds common logic (position, velocity, rendering, etc...)

  - `Pacman` (`Entity`): manages the coordinate of the player and the input parsing

  - `Ghost` (`Entity`): manages the algorithm of tracking, and the ghost movement
