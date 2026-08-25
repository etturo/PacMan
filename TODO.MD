- [ ] Create a SoundManager class similar to the sprite library to handle sounds

# FUTURE ARCHITECTURAL IMPROVEMENTS
 - [ ] **Refactor Game Class to Instance-Based:** Replace the static `@classmethod` structure with an instantiable class to improve testability and allow clean state initialization/resets.
 - [ ] **Implement Game State Manager (State Pattern):** Decouple `GameMode` logic from rendering and loop functions. Use a context manager/state machine with independent state classes (e.g., `MenuState`, `PlayingState`).
 - [ ] **Add Virtual Resolution and Aspect Ratio Scaling (Letterboxing):** Render the game to a fixed-size retro canvas (e.g., 448x496) and scale it dynamically to fit the window with letterboxing.
 - [ ] **Fix Config Field Name Mismatch (Pydantic <-> JSON):** Rename `pacgum` to `pacgums` and `points_per_pacgum` to `points_per_pacgums` in `config.json` (or use validation aliases in `src/utils/models.py`) so configuration changes are not silently ignored.
 - [ ] **Relocate Sound Assets:** Move `pac-man-startup.mp3` from `temp/` to a permanent assets subdirectory (e.g., `data/assets/sounds/`) and reference it cleanly.
 - [ ] **Implement Movement, Collision, and AI Systems:** Complete the empty `Entity`, `Pacman`, and `Ghost` stubs using grid-to-screen coordinate mapping and standard Pac-man ghost behaviors.