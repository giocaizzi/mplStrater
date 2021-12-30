from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mplStrater',
    version="0.0.5",
    description="plot geologic stratigraphic columns with python",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/giocaizzi/mplStrater',
    author='giocaizzi',
    author_email='giocaizzi@gmail.com',
    license="MIT",
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
    # extras_require={
    #     "docs":[
    #         "sphinx",
    #         "nbsphinx",
    #         "myst-parser",
    #         "sphinx_rtd_theme",
    #         "docutils==0.16"],
    #     "dev":[],
    #     'test':['pytest',"pytest-cov"],
    #     },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    project_urls={
        'Documentation':'https://giocaizzi.github.io/mplStrater/',
        'Bug Reports': 'https://github.com/giocaizzi/mplStrater/issues',
        'Source': 'https://github.com/giocaizzi/mplStrater',
    },
)