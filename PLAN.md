# Intro info
the file audio of the original intro is in the /temp folder
the real duration of the audio is 4.3336 seconds

knowing that the game is running at 60fps
every frame last $1/60 = 0,016666667 \approx 0.0167$

so the total number of frame of the initial screen to fit into the audio track lenght is:
$$
4.3336 / 0.0167 = 259,497005988 \approx 260 \space frames
$$

the remaining time is in silence, but sticazzi


# REFACTORING NEEDED
 - [x] Create a sprite library (SpriteLibrary) an interface to store all the sprite sheets into one place and let the other parts of the programs to access that variable without creating multiple instances of the same sheet.
 - [x] Create a element ABC class to inherite all the UI elements.
 - [X] Change the Maze renderer to a instanced object to use self and store the maze surface so isnt recalculated every frame.


# FUTURE ARCHITECTURAL IMPROVEMENTS
 - [ ] **Refactor Game Class to Instance-Based:** Replace the static `@classmethod` structure with an instantiable class to improve testability and allow clean state initialization/resets.
 - [ ] **Implement Game State Manager (State Pattern):** Decouple `GameMode` logic from rendering and loop functions. Use a context manager/state machine with independent state classes (e.g., `MenuState`, `PlayingState`).
 - [ ] **Add Virtual Resolution and Aspect Ratio Scaling (Letterboxing):** Render the game to a fixed-size retro canvas (e.g., 448x496) and scale it dynamically to fit the window with letterboxing.
 - [ ] **Fix Config Field Name Mismatch (Pydantic <-> JSON):** Rename `pacgum` to `pacgums` and `points_per_pacgum` to `points_per_pacgums` in `config.json` (or use validation aliases in `src/utils/models.py`) so configuration changes are not silently ignored.
 - [ ] **Relocate Sound Assets:** Move `pac-man-startup.mp3` from `temp/` to a permanent assets subdirectory (e.g., `data/assets/sounds/`) and reference it cleanly.
 - [ ] **Implement Movement, Collision, and AI Systems:** Complete the empty `Entity`, `Pacman`, and `Ghost` stubs using grid-to-screen coordinate mapping and standard Pac-man ghost behaviors.