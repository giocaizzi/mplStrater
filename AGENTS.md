# AGENTS.md

`mplStrater`: Python library that plots geologic stratigraphic columns on matplotlib figures. Published on PyPI.

## Commands

- `uv sync`: install the package with the `dev` group.
- `make help | lint | test | check`: CI runs `make check` (ruff check, ruff format --check, pytest with coverage).
- Docs: `uv run --group docs make -C docsrc github` builds Sphinx from `docsrc/source` into `docs/` (served by GitHub Pages).

## Gotchas

- Python is pinned to 3.12 (`.python-version`): `rio-color` ships only an sdist whose build pins `numpy==2.0.2`, which has no 3.13 wheels.
- The version lives in both `pyproject.toml` and `__version__` in `mplStrater/__init__.py`; bump both.
- `docs/` is generated HTML; edit `docsrc/source`, never `docs/`.
- `main` changes only through squash-merged PRs with a Conventional Commit title; the required check is `check` in `.github/workflows/ci.yml`. See the [GitHub standard](https://github.com/giocaizzi/.github/blob/main/docs/standard.md).
