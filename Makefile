.PHONY: install run debug clean lint lint-strict build

PYTHON = $(BIN)/python3
SRC = src
VENV = .venv
BIN = $(VENV)/bin
CONFIG_FILE = "config.json"

all: install run

install:
	uv sync

run:
	$(PYTHON) -m $(SRC) $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb -m $(SRC) $(CONFIG_FILE)

build:
# 	For linux
	pyinstaller --noconsole --onefile -n "BarkMan" --add-data "data:data" src/__main__.py
# 	For windows
	pyinstaller --noconsole --onefile -n "BarkMan" --add-data "data;data" src/__main__.py

clean:
	rm -rf .venv
	rm -rf .mypy_cache
	rm -rf src/.mypy_cache
	rm -rf __pycache__
	rm -rf *.spec
	rm -rf build
	rm -rf dist
	systemctl --user restart pipewire pipewire-pulse pulseaudio

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
