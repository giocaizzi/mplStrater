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

##### SYMBOLOGY and LEGEND ############################

FILL_DICT={
    'Terreno conforme': 'lightgreen',
    'Riporto conforme': 'darkgreen',
    'Riporto non conforme': 'orange',
    'Rifiuto': 'red',
    'Assenza campione': 'white'
    }

HATCH_DICT={
    'Non pericoloso': '',
    'Pericoloso': 'xxxxxxxxx',
    '_': ''
    }

@pytest.fixture(scope="class")
def test_symbology(request):
    request.cls.fill_list=list(FILL_DICT.values())
    request.cls.hatch_list=list(HATCH_DICT.values())

@pytest.fixture(scope="class")
def test_legend(request):
    request.cls.fill_dict=FILL_DICT
    request.cls.hatch_dict=HATCH_DICT

##### COLUMN ############################
@pytest.fixture(scope="class")
def test_column(request):
    request.cls.first_column=read_csv(FIN).iloc[0]
