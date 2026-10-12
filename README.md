# mplStrater

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mplStrater)
![PyPI](https://img.shields.io/pypi/v/mplStrater?color=blue)

![GitHub Release Date](https://img.shields.io/github/release-date/giocaizzi/mplStrater)
![CI](https://github.com/giocaizzi/mplStrater/actions/workflows/ci.yml/badge.svg?branch=main)
![Codecov](https://img.shields.io/codecov/c/github/giocaizzi/mplStrater)
[![Requirements Status](https://requires.io/github/giocaizzi/mplStrater/requirements.svg?branch=main)](https://requires.io/github/giocaizzi/mplStrater/requirements/?branch=main)
![License](https://img.shields.io/github/license/giocaizzi/mplStrater)
![GitHub issues](https://img.shields.io/github/issues/giocaizzi/mplStrater)

This package provides the possibility to plot geologic stratigraphic columns with a structured symbology and labelling system on `matplotlib` figures.

The package allows to use georeferenced rasters as basemap.

![map](https://github.com/giocaizzi/mplStrater/blob/main/docsrc/source/images/map.png?raw=true)

Additionally, the package has the capability to just plot the single stratigraphic columns.

![columns](https://github.com/giocaizzi/mplStrater/blob/main/docsrc/source/images/columns.jpeg?raw=true)

## Documentation

The documentation with examples can be found [here](https://giocaizzi.github.io/mplStrater/).

## Installation with pip

```
pip install mplStrater
```

## Development

Requires [uv](https://docs.astral.sh/uv/).

```
git clone https://github.com/giocaizzi/mplStrater.git
cd mplStrater
uv sync
make check
```
