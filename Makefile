.PHONY: install run debug clean lint lint-strict build train

ifeq ($(OS),Windows_NT)
PYTHON = $(VENV)/Scripts/python.exe
else
PYTHON = $(BIN)/python3
endif
PACMAN = pac-man.py
VENV = .venv
BIN = $(VENV)/bin
CONFIG_FILE = config.json

all: install run

install:
	uv sync

run:
	$(PYTHON) $(PACMAN) $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb $(PACMAN) $(CONFIG_FILE)

train:
	$(PYTHON) -m $(PACMAN).ai.train $(CONFIG_FILE)

build:
	$(PYTHON) -m PyInstaller --clean Pacman.spec

clean:
	$(PYTHON) -c "import shutil; from pathlib import Path;
	[shutil.rmtree(path, ignore_errors=True) for path in ('.venv', '.mypy_cache', 'PACMAN/.mypy_cache', 'build', 'dist')] + [shutil.rmtree(path, ignore_errors=True) for path in Path('.').rglob('__pycache__') if path.is_dir()]"

lint:
	$(BIN)/flake8 .
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs

lint-strict:
	$(BIN)/flake8 . --color=always
	$(BIN)/mypy . --strict --color-output

c:
	@clear
	@FORCE_COLOR=1 MYPY_FORCE_COLOR=1 make -s lint-strict | head -n 10
