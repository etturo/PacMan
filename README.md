*This project has been created as part of the 42 curriculum by aflorea, eturini.*

# Pacman

## Description

Pacman is a playable desktop recreation of the classic Pac-Man game, written in
Python with Pygame Community Edition. The player controls Pac-Man through
procedurally generated mazes, collects pac-gums and super pac-gums, avoids or
eats ghosts, and tries to obtain a place in the leaderboard.

The project also explores how a small game can be structured into independent
systems: configuration parsing, game states, entities, maze generation,
rendering, sound, and persistent scores. The interface deliberately combines
the original arcade vocabulary with a CRT-inspired visual style, including
optional glow, glitch, rolling, and CRT effects.

## Features

- Start screen, menu, settings, pause, gameplay, victory, and game-over states.
- Keyboard controls using the arrow keys or `W`, `A`, `S`, and `D`.
- Multiple configurable levels and a deterministic maze seed.
- Four ghost personalities inspired by the original Pac-Man behaviors:
  Blinky, Pinky, Inky, and Clyde.
- Scatter/chase scheduling, frightened ghosts, ghost eating, lives, timers,
  and progressive scoring.
- Sprite-sheet rendering, original-style sound effects, and post-processing
  display effects.
- Persistent top-ten highscore display.
- Linux and Windows executable builds through GitHub Actions and PyInstaller.

## Instructions

### Requirements

- Python 3.12 or newer.
- `uv` for dependency and virtual-environment management.
- A desktop environment capable of opening a Pygame window.

### Install and run

From the repository root:

```bash
make install
make run
```

`make install` runs `uv sync` and installs the dependencies declared in
[`pyproject.toml`](./pyproject.toml), including Pygame CE, Pydantic, mypy,
flake8, PyInstaller, and the assigned `mazegenerator` wheel.

The normal run command loads [`config.json`](./config.json). A different
configuration file can be supplied directly:

```bash
.venv/bin/python3 -m src path/to/config.json
```

On Windows, use `.venv\Scripts\python.exe -m src config.json`.

Useful Make targets:

```text
make debug       Run through Python's debugger
make lint        Run flake8 and the configured mypy checks
make lint-strict Run the strict lint configuration
make build       Build the PyInstaller executable
make clean       Remove generated caches and build directories
```

Controls are shown in the in-game menu. In short, use the arrow keys or
`WASD` to move, `P` to pause, `F11` to toggle fullscreen, and `Escape` to
exit. The settings screen also exposes FPS, visual effects, lives, and
development cheats.

## Configuration

The configuration file is JSON. `SettingParser` removes comments before
decoding it and validates the result with the `GameSettings` Pydantic model.
Invalid JSON, missing files, and invalid values are reported as explicit
startup errors.

The supported structure and model defaults are:

| Key | Type | Default | Meaning |
| --- | --- | --- | --- |
| `highscore_filename` | string | `scores.json` | Filename used in the per-user data directory |
| `levels` | list of `{width, height}` | `5x5`, `15x15`, `28x36` | Maze dimensions for successive levels |
| `lives` | positive integer | `3` | Starting lives |
| `pacgums` | non-negative integer | `42` | Pac-gum setting used by the game rules |
| `points_per_pacgum` | positive integer | `10` | Score awarded for a normal pac-gum |
| `points_per_super_pacgum` | positive integer | `50` | Score awarded for a super pac-gum |
| `points_per_ghost` | integer | `200` | Base score awarded for a ghost |
| `seed` | non-negative integer | `42` | Deterministic maze-generation seed |
| `level_max_time` | positive integer | `90` | Time limit per level in seconds |
| `ghost_freezed` | boolean | `false` | Development cheat that freezes ghosts |
| `double_speeded` | boolean | `false` | Development cheat that increases speed |
| `invincibility` | boolean | `false` | Development cheat that prevents lethal collisions |
| `fps` | integer | `60` | Target update/render frequency |
| `crt`, `glitch`, `glow`, `rolling` | boolean | `true` | Initial visual post-processing options |

The checked-in configuration intentionally differs from some model defaults:
it uses three levels (`15x15`, `15x15`, `28x36`), one starting life, and writes
to `highscore.txt`. The configuration file is therefore the authoritative
runtime choice for this checkout. `points_per_super_pacgum` must always be
greater than `points_per_pacgum`.

## Highscore

When a game ends normally, the player enters an alphanumeric name and the
score is appended to a JSON list of `[name, score]` pairs. The menu sorts the
list numerically and displays the ten highest entries.

Scores are saved outside the repository so that playing the game does not
modify installed assets:

- Linux: `$XDG_DATA_HOME/BarkMan/<highscore_filename>`, or
  `~/.local/share/BarkMan/<highscore_filename>` when `XDG_DATA_HOME` is unset.
- Windows: `%LOCALAPPDATA%\BarkMan\<highscore_filename>`.

If no user score file exists, the bundled
[`data/leadboard/scores.json`](./data/leadboard/scores.json) is used as the
initial display. Scores made while a development cheat is active are not
stored. This keeps the leaderboard comparable while still allowing cheats to
be useful for testing and demonstrations. JSON was chosen because the
leaderboard is small, human-readable, and does not require a database.

## Maze Generation

The project uses the assigned A-Maze-ing package from
[`data/external_libraries/mazegenerator-2.1.0-py3-none-any.whl`](./data/external_libraries/mazegenerator-2.1.0-py3-none-any.whl).
`MazeWrapper` adapts the package's `MazeGenerator` to the game's own `Maze`
and `Cell` classes.

For each level, the wrapper passes the configured dimensions and seed to
`MazeGenerator`, requests a non-perfect maze, and uses `(0, 0)` and `(1, 1)`
as the generator's entry and exit cells. The generated integer wall map is
then copied into the internal row-major maze representation. Keeping this
adapter separate means the rest of the game only depends on the project's
maze interface and can use the same maze for rendering, collision checks, and
ghost pathfinding. A fixed seed makes a run reproducible; changing `seed`
changes the generated layouts.

## Implementation

The game loop is driven by Pygame. Each frame, `Game` limits the frame rate,
collects events, forwards them to the active state, updates the simulation,
and renders the resulting surface through `ScreenManager`.

Important implementation choices include:

- **State-driven flow:** menu, gameplay, pause, settings, start, victory, and
  game-over screens are separate state objects with a common `BaseState`
  interface.
- **Grid-based world:** `Maze` stores cells and wall directions; entities use
  grid positions while rendering interpolated movement at screen coordinates.
- **Ghost AI:** a shared `GhostModeController` schedules scatter and chase
  phases. Individual strategies select targets, and breadth-first search
  chooses the shortest available direction with deterministic tie-breaking.
- **Reusable graphics:** `SpriteLibrary` and sprite sheets centralize asset
  loading. UI elements derive from drawable/live element abstractions so
  buttons, text, score, lives, and timers share rendering conventions.
- **Validation at the boundary:** JSON is parsed once into typed Pydantic
  settings before the game starts, preventing invalid gameplay parameters from
  spreading through the simulation.
- **Packaged resources:** `paths.resource_path` supports both normal source
  execution and PyInstaller's bundled resource directory.

## General Software Architecture

The main relationships are:

```text
src/__main__.py
        |
       Game  ----------------------> ScreenManager
        |                                  |
        +--> active BaseState              +--> sprite and post-processing
        |       |
        |       +--> Menu / Starting / Playing / Pause /
        |            Setting / GameOver states
        |
        +--> SettingParser --> GameSettings
        |
        +--> MazeWrapper --> Maze --> Cell
        |                         ^
        |                         |
        +--> PlayingState --> Pacman, Ghost, Pacgum, SuperPacgum
                              |
                              +--> GhostModeController and strategies

SoundLibrary and SpriteLibrary provide shared asset services to the states
and UI elements. paths.py owns platform-specific resource and score paths.
```

The code is grouped by responsibility:

- [`src/core`](./src/core): application loop and state transitions.
- [`src/entities`](./src/entities): Pac-Man, ghosts, collectibles, and
  movement/AI logic.
- [`src/world`](./src/world): maze, cells, directions, and the generator
  adapter.
- [`src/graphics`](./src/graphics): rendering, sprite sheets, screen effects,
  and UI components.
- [`src/sounds`](./src/sounds): sound loading and playback.
- [`src/utils`](./src/utils): settings models, parsing, paths, and constants.
- [`tests`](./tests): focused tests for UI behavior and gameplay state.

## Project Management

Development notes, solved issues, refactoring tasks, and remaining ideas are
tracked in [`PLAN.md`](./PLAN.md).

## Resources

- [Pygame CE documentation](https://pyga.me/docs/) — windowing, input,
  surfaces, timing, and audio.
- [Pydantic documentation](https://docs.pydantic.dev/) — typed validation of
  configuration data.
- [Python `json` documentation](https://docs.python.org/3/library/json.html)
  — leaderboard serialization.
- [Pac-Man Dossier](https://pacman.holenet.info/) — original game rules,
  ghost behavior, and timing reference.
- [CRT and glitch effects in Pygame](https://dev.to/chrisgreening/simulating-simple-crt-and-glitch-effects-in-pygame-1mf1)
  — inspiration for the display post-processing choices.
- [Pygame Example Library](https://github.com/yoyoberenguer/PEL) — reference
  material for Pygame-oriented implementation patterns.

### Use of AI

AI was used as a documentation and review aid for this deliverable. It
inspected the existing source tree and configuration, summarized the
architecture and design decisions, checked that the requested README sections
were covered, and helped organize the English explanations. AI did not replace
the project's gameplay implementation, asset creation, maze package, or
testing decisions; those remain part of the repository's implementation and
the authors' design work.
