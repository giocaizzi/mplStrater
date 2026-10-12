<div align="center">

# mplStrater

**Geologic stratigraphic columns on matplotlib figures.**

[![PyPI](https://img.shields.io/pypi/v/mplStrater?color=blue)](https://pypi.org/project/mplStrater/)
[![Python](https://img.shields.io/pypi/pyversions/mplStrater)](https://pypi.org/project/mplStrater/)
[![CI](https://github.com/giocaizzi/mplStrater/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/giocaizzi/mplStrater/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/giocaizzi/mplStrater/branch/main/graph/badge.svg)](https://codecov.io/gh/giocaizzi/mplStrater)
[![Docs](https://img.shields.io/badge/docs-github%20pages-blue)](https://giocaizzi.github.io/mplStrater/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

This package provides the possibility to plot geologic stratigraphic columns with a structured symbology and labelling system on `matplotlib` figures.

The package allows to use georeferenced rasters as basemap.

![map](https://github.com/giocaizzi/mplStrater/blob/main/docsrc/source/images/map.png?raw=true)

Additionally, the package has the capability to just plot the single stratigraphic columns.

![columns](https://github.com/giocaizzi/mplStrater/blob/main/docsrc/source/images/columns.jpeg?raw=true)

## Installation

```bash
pip install mplStrater
```

## Documentation

Documentation with examples: [giocaizzi.github.io/mplStrater](https://giocaizzi.github.io/mplStrater/).

## Development

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/giocaizzi/mplStrater.git
cd mplStrater
uv sync
make check
```

## License

[MIT](LICENSE)
