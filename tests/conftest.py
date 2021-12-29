from pathlib import Path
import pytest
from pandas import read_csv


CWD = Path(__file__).resolve()
FIN = CWD.parent / "test.csv"
CRS=32633

def pytest_configure(config):
    config.addinivalue_line("markers", "wip: WORK IN PROGRESS")

@pytest.fixture(scope="class")
def test_data(request):
    request.cls.test_data=read_csv(FIN)
    request.cls.epsg=CRS