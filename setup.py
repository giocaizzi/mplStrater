from setuptools import setup, find_packages
import mplStrater

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mplStrater',
    version=mplStrater.__version__,
    description="plot geologic stratigraphic columns",
    author='giocaizzi',
    author_email='giocaizzi@gmail.com',
    url='',
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(include=['mplStrater', 'mplStrater.*']),
    install_requires=[
        "geopandas",
        "matplotlib",
        "numpy",
        "pandas",
        "rasterio",
        "rio_color"]
)