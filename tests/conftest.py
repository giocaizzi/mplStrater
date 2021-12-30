from pathlib import Path
import pytest
from pandas import read_csv

##### MARKS #############################

def pytest_configure(config):
    config.addinivalue_line("markers", "wip: WORK IN PROGRESS")

##### DATA  #############################
CWD = Path(__file__).resolve()
FIN = CWD.parent / "test.csv"
CRS=32633

@pytest.fixture(scope="class")
def test_data(request):
    request.cls.test_data=read_csv(FIN)
    request.cls.epsg=CRS

##### SYMBOLOGY ############################

COLORS=["green","white","blue"]
HATCHES=["","xxxxxxxxx",""]

@pytest.fixture(scope="class")
def test_symbology(request):
    request.cls.colors=COLORS
    request.cls.hatches=HATCHES

##### COLUMN ############################
@pytest.fixture(scope="class")
def test_column(request):
    request.cls.first_column=read_csv(FIN).iloc[0]
