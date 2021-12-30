import unittest
from matplotlib.colors import ListedColormap
from mplStrater.strata import Symbology,Legend,Column
import pytest
import pandas as pd

@pytest.mark.usefixtures("test_symbology")
class TestSymbology(unittest.TestCase):

    def test_color(self):
        #test symbology structure
        s=Symbology(d={},colors=self.colors)
        self.assertIsInstance(s.d,dict)
        self.assertEqual(set(s.colors),set(self.colors))
        self.assertIsInstance(s.cmap,ListedColormap)
    
    def test_hatches(self):
        #test symbology structure
        s=Symbology(d={},hatches=self.hatches)
        self.assertIsInstance(s.d,dict)
        self.assertEqual(set(s.hatches),set(self.hatches))

    def test_error(self):
        #test error input
        d={}
        self.assertRaises(
            ValueError,
            Symbology,
            d,colors=self.colors,hatches=self.hatches)

class TestLegend(unittest.TestCase):

    def test_init(self):
        #matrix and hatches are symbology 
        l=Legend()
        self.assertIsInstance(l.matrix,Symbology)
        self.assertIsInstance(l.hatches,Symbology)


@pytest.mark.usefixtures("test_column")
class TestColumn(unittest.TestCase):

    @pytest.mark.wip
    def test_fixture(self):
        assert isinstance(self.first_column,pd.Series)

if __name__=="__main__":
    unittest.main()