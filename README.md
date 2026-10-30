*This project has been created as part of the 42 curriculum by eturini, aflorea.*

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
glow, glitch, rolling, and CRT effects. These effects start enabled when the
game is launched; the settings screen can toggle them while the game runs.

### Play the packaged game

The game is available on itch.io: <ITCH_URL>

## Features

- Start screen, menu, settings, pause, gameplay, victory, and game-over states.
- Keyboard controls using the arrow keys or `W`, `A`, `S`, and `D`.
- Multiple configurable levels: the first maze comes from a fixed seed, the
  following ones are random.
- Four ghost personalities inspired by the original Pac-Man behaviours:
  Blinky, Pinky, Inky, and Clyde.
- Scatter/chase scheduling, frightened ghosts, ghost eating, lives, timers,
  and progressive scoring.
- Sprite-sheet rendering, original-style sound effects, and post-processing
  display effects.
- Persistent top-ten highscore display.
- AI mode: Pacman plays by himself and tries to win. More details in the
  [dedicated section](#ai-mode).
- Linux and Windows executable builds through GitHub Actions and PyInstaller.
- Cheats ;)

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
flake8, PyInstaller, ruff, and the assigned `mazegenerator` wheel.

The normal run command loads [`config.json`](./config.json). A different
configuration file can be supplied directly:

```bash
.venv/bin/python3 pac-man.py path/to/config.json
```

On Windows, use `.venv\Scripts\python.exe pac-man.py config.json`.

Useful Make targets:

```text
make debug       Run through Python's debugger
make lint        Run flake8 and the configured mypy checks
make lint-strict Run the strict lint configuration
make build       Build the PyInstaller executable
make clean       Remove generated caches and build directories
make train       Train the AI player and update its weights
```

Controls are shown in the in-game menu. In short, use the arrow keys or
`WASD` to move, `P` to pause, `F11` to toggle fullscreen, and `Escape` to
exit. The settings screen also exposes FPS, visual effects, lives, and
development cheats.

### Building a release package

The root [`Pacman.spec`](./Pacman.spec) is the reproducible PyInstaller
packaging definition. After installing dependencies, regenerate the executable
with:

```bash
make build
```

The result is `dist/Pacman` on Linux and `dist/Pacman.exe` on Windows. The
executable is a one-file package containing the source resources, sounds,
sprites, maze-generator dependency, and default configuration. Do not copy
the repository's `build/` directory as the release: upload the executable
from `dist/` to the selected private or unlisted distribution page.

Before publishing a build, launch the executable on the target operating
system, open the main menu, verify the controls panel, start a game, open
settings, and confirm that fullscreen, FPS, visual effects, lives, sound-set
selection, and the development options respond correctly. The main menu
contains the minimal player instructions, so no separate runtime dependency
is required.

The main menu shows the controls and the rules. `PLAYER_README.txt`, shipped
next to the executable, also covers the options and the configuration. The
executable reads the `config.json` next to it, and falls back to the bundled
one when it is missing.

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
| `points_per_ghost` | positive integer | `200` | Score of the first ghost of a streak; it doubles for each next ghost, up to 8 times |
| `seed` | non-negative integer | `42` | Seed of the first level; `0` makes it random |
| `level_max_time` | positive integer | `90` | Time limit per level in seconds |
| `ghost_freezed` | boolean | `false` | Development cheat that freezes ghosts |
| `double_speeded` | boolean | `false` | Development cheat that increases speed |
| `invincibility` | boolean | `false` | Development cheat that prevents lethal collisions |
| `fps` | integer | `60` | Target update/render frequency |
| `crt`, `glitch`, `glow`, `rolling` | boolean | `true` | Initial visual post-processing options |

The checked-in [`config.json`](./config.json) is the authoritative runtime
configuration for this checkout. It uses three levels (`15x15`, `5x5`,
`7x7`), three starting lives, a 120-second level timer, and writes to
`highscore.txt`. The parser also accepts the documented model defaults when a
field is omitted. `points_per_super_pacgum` must always be greater than
`points_per_pacgum`.

The `pacgums` setting is retained in the configuration model but is not used
to determine the number of collectibles. On mazes large enough for it,
gameplay reserves a fixed central pattern of cells; the four corner cells
receive super pac-gums.

## Highscore

When a game ends normally, the player enters an alphanumeric name and the
score is appended to a JSON list of `[name, score]` pairs. The menu sorts the
list numerically and displays the ten highest entries.

Scores are saved outside the repository so that playing the game does not
modify installed assets:

- Linux: `$XDG_DATA_HOME/Pacman/<highscore_filename>`, or
  `~/.local/share/Pacman/<highscore_filename>` when `XDG_DATA_HOME` is unset.
- Windows: `%LOCALAPPDATA%\Pacman\<highscore_filename>`.

If no user score file exists, the bundled
[`data/leadboard/scores.json`](./data/leadboard/scores.json) is used as the
initial display and copied to the user data path. Scores made while a
development cheat is active are not stored: the game returns to the menu
instead of opening the score-entry screen. JSON is used even when the
configured filename has a `.txt` extension.

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
changes the generated layouts. The wrapper suppresses generator output and
silently leaves the maze uninitialized if generation raises an exception.

## AI mode

The **ai play** button in the main menu lets Pacman play by himself. The player
uses linear approximate Q-learning: instead of storing a value for every game
state, it describes each possible move with a few numeric features and scores
the move with a weighted sum of them. Scores made in AI mode are not stored in
the leaderboard.

### How a move is chosen

Whenever Pacman stops on a cell, `PlayingState` builds a `PacmanContext` with
the maze, Pacman's position, the released ghosts and their modes, the remaining
food, and the frightened time left. `QAgent` then computes, for each direction
without a wall:

$Q(s, a) = \sum_i w_i \, f_i(s, a)$

and takes the move with the highest value.

### Features

Distances are breadth-first search distances in the maze, measured from the
cell the move leads to.

| Feature | Meaning |
| --- | --- |
| `bias` | Constant term |
| `ghosts-1-step` | Dangerous ghosts within one step |
| `eats-food` | 1 if the move lands on food with no danger nearby |
| `closest-food` | Distance to the nearest food, divided by the maze area |
| `eats-ghost` | Reachable frightened ghosts within one step |
| `closest-scared` | Closeness of the nearest reachable frightened ghost: near 1 when adjacent, 0 when there is none |

A frightened ghost counts as reachable only if Pacman can get there before the
frightened time ends. Otherwise it counts as dangerous, because it will soon be
lethal again.

### Training

`make train` runs 200 episodes of the real game without a window, using dummy drivers and a fixed time step. An episode lasts one life, and every maze
is random, so the weights do not overfit a single layout. After each move the
weights are corrected:

$\delta = r + \gamma \max_{a'} Q(s', a') - Q(s, a)$

$w_i \leftarrow w_i + \alpha \, \delta \, f_i(s, a)$

- **Reward $r$:** the points gained since the previous decision, minus 1 per move, and minus 500 when the life ends without a win.
- **Discount:** $\gamma = 0.8$.
- **Exploration:** a random move 5% of the time during training (but never while playing).
- **Learning rate:** $\alpha$ starts at 0.2 and decays after each episode as $\alpha = \frac{0.2}{1 + \text{episodes} / 20}$, which keeps the weights from oscillating.

This equation is represented in the method `extract`, which represents a linear approximation of the utility-action Q-function.
The result is saved in [`data/ai/weights.json`](./data/ai/weights.json) and shipped with the executable.

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
  chooses the shortest available direction with deterministic tiebreaking.
- **Reusable graphics:** `SpriteLibrary` and sprite sheets centralise asset
  loading. UI elements derive from drawable/live element abstractions, so
  buttons, text, score, lives, and timers share rendering conventions.
- **Validation at the boundary:** JSON is parsed once into typed Pydantic
  settings before the game starts. The model validates lives, pac-gum points,
  seed, level time, and the relationship between normal and super pac-gum
  scores; the model does not range-constrain level dimensions and FPS.
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
- [`src/ai`](./src/ai): features, Q-learning agent, and headless training.
- [`src/utils`](./src/utils): settings models, parsing, paths, and constants.

## Project Management

Development notes, solved issues, refactoring tasks, and remaining ideas were
tracked in a [`PLAN.md`](./PLAN.md).

## Resources

- [Pygame CE documentation](https://pyga.me/docs/): windowing, input,
  surfaces, timing, and audio.
- [Pydantic documentation](https://docs.pydantic.dev/): typed validation of
  configuration data.
- [Python `json` documentation](https://docs.python.org/3/library/json.html)
  : leaderboard serialization.
- [Pac-Man Dossier](https://pacman.holenet.info/): original game rules,
  ghost behavior, and timing reference.
- [CRT and glitch effects in Pygame](https://dev.to/chrisgreening/simulating-simple-crt-and-glitch-effects-in-pygame-1mf1): inspiration for the display post-processing choices.
- [Pygame Example Library](https://github.com/yoyoberenguer/PEL): reference
  material for Pygame-oriented implementation patterns.
- [Berkeley CS188, Project 3: Reinforcement Learning](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj3/)
- [Texas University, Reinforcement learning assignment](https://www.cs.utexas.edu/~grauman/courses/spring2014/psets/ps3/03-reinforcement.html)
- Stuart Russell and Peter Norvig,
  [*Artificial Intelligence: A Modern Approach*](https://aima.cs.berkeley.edu/),
  4th ed., chapter 22 (Reinforcement Learning): Q-learning and linear function
  approximation.

### Use of AI

AI was used as a documentation and review aid for this deliverable. It
inspected the existing source tree and configuration, summarised the
architecture and design decisions, checked that the requested README sections
were covered, and helped organise the English explanations. AI did not replace
the project's gameplay implementation, asset creation, maze package, or
testing decisions; those remain part of the repository's implementation and
the authors' design work.
