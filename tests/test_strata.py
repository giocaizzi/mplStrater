import unittest
from matplotlib.colors import ListedColormap
from mplStrater.strata import Symbology,Legend,Column
import pytest
import pandas as pd

@pytest.mark.usefixtures("test_symbology")
class TestSymbology(unittest.TestCase):

    def test_fill(self):
        #test symbology structure
        s=Symbology(d={},fill=self.fill_list)
        self.assertIsInstance(s.d,dict)
        self.assertEqual(set(s.fill),set(self.fill_list))
        self.assertIsInstance(s.cmap,ListedColormap)
    
    def test_hatches(self):
        #test symbology structure
        s=Symbology(d={},hatches=self.hatch_list)
        self.assertIsInstance(s.d,dict)
        self.assertEqual(set(s.hatches),set(self.hatch_list))

    def test_error(self):
        #test error input
        d={}
        self.assertRaises(
            ValueError,
            Symbology,
            d,fill=self.fill_list,hatches=self.hatch_list)

@pytest.mark.usefixtures("test_legend")
class TestLegend(unittest.TestCase):

    def test_init(self):
        #matrix and hatches are symbology 
        l=Legend(fill_dict=self.fill_dict,hatch_dict=self.hatch_dict)
        self.assertIsInstance(l.fill,Symbology)
        self.assertIsInstance(l.hatches,Symbology)


@pytest.mark.usefixtures("test_column")
class TestColumn(unittest.TestCase):

    @pytest.mark.wip
    def test_fixture(self):
        assert isinstance(self.first_column,pd.Series)

if __name__=="__main__":
    unittest.main()