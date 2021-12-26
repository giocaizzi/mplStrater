from setuptools import setup, find_packages
import mplStrater

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mplStrater',
    version=mplStrater.__version__,
    description="plot geologic stratigraphic columns with python",
    author='giocaizzi',
    author_email='giocaizzi@gmail.com',
    url='https://github.com/giocaizzi/mplStrater',
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(include=['mplStrater','mplStrater/*']),
    setup_requires=[],
    tests_require=['pytest'],
    install_requires=[
        "geopandas",
        "matplotlib",
        "numpy>=1.17",
        "pandas",
        "rasterio",
        "rio_color"],
    extras_require={
        "docs":[
            "sphinx",
            "nbsphinx",
            "sphinx_rtd_theme"
            ],
        "dev":[],
        'test':['pytest'],
        "coverage":["coveralls","pytest-cov"]
    },
    project_urls={
        'Documentation':'https://giocaizzi.github.io/mplStrater/',
        'Bug Reports': 'https://github.com/giocaizzi/mplStrater/issues',
        'Source': 'https://github.com/giocaizzi/mplStrater',
    },
)