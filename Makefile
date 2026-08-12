.PHONY: install run debug clean lint lint-strict

PYTHON = $(BIN)/python3
SRC = src
VENV = .venv
BIN = $(VENV)/bin

all: install run

install:
	uv sync

run:
	$(PYTHON) -m $(SRC)

debug:
	$(PYTHON) -m pdb -m $(SRC)

clean:
	rm -rf .venv
	rm -rf .mypy_cache
	rm -rf src/.mypy_cache
	rm -rf __pycache__

lint:
	$(BIN)/flake8 $(SRC)
	$(BIN)/mypy $(SRC) --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs

lint-strict:
	$(BIN)/flake8 $(SRC)
	$(BIN)/mypy $(SRC) --strict

c:
	clear
	make lint-strict
