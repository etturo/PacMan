.PHONY: install run debug clean lint lint-strict build

ifeq ($(OS),Windows_NT)
PYTHON = $(VENV)/Scripts/python.exe
else
PYTHON = $(BIN)/python3
endif
SRC = src
VENV = .venv
BIN = $(VENV)/bin
CONFIG_FILE = config.json

all: install run

install:
	uv sync

run:
	$(PYTHON) -m $(SRC) $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb -m $(SRC) $(CONFIG_FILE)

build:
	$(PYTHON) -m PyInstaller --clean BarkMan.spec

clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(path, ignore_errors=True) for path in ('.mypy_cache', 'src/.mypy_cache', '__pycache__', 'build', 'dist')]"

lint:
	$(BIN)/flake8 $(SRC)
	$(BIN)/mypy $(SRC) --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs

lint-strict:
	$(BIN)/flake8 $(SRC) --color=always
	$(BIN)/mypy $(SRC) --strict --color-output

c:
	@clear
	@FORCE_COLOR=1 MYPY_FORCE_COLOR=1 make -s lint-strict | head -n 10
