from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mplStrater',
    version="0.0.2",
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
        "rio_color"
        ],
        
    extras_require={
        "docs":[
            "sphinx",
            "nbsphinx",
            "myst-parser",
            "sphinx_rtd_theme",
            "docutils==0.16"],
        "dev":[],
        'test':['pytest',"pytest-cov"],
        },
    project_urls={
        'Documentation':'https://giocaizzi.github.io/mplStrater/',
        'Bug Reports': 'https://github.com/giocaizzi/mplStrater/issues',
        'Source': 'https://github.com/giocaizzi/mplStrater',
    },
)