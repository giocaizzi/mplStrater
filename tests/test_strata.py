import unittest
from matplotlib.colors import ListedColormap


from matplotlib import colors
from mplStrater.strata import Symbology,Legend

class TestSymbology(unittest.TestCase):

    def test_color(self):
        #test symbology structure
        colors=["green","white","blue"]
        s=Symbology(d={},colors=colors)
        self.assertIsInstance(s.d,dict)
        self.assertEqual(set(s.colors),set(colors))
        self.assertIsInstance(s.cmap,ListedColormap)
    
    def test_hatches(self):
        #test symbology structure
        hatches=["","xxxxxxxxx",""]
        s=Symbology(d={},hatches=hatches)
        self.assertIsInstance(s.d,dict)
        self.assertEqual(set(s.hatches),set(hatches))

class TestLegend(unittest.TestCase):

    def test_init(self):
        #matrix and hatches are symbology 
        l=Legend()
        self.assertIsInstance(l.matrix,Symbology)
        self.assertIsInstance(l.hatches,Symbology)


if __name__=="__main__":
    unittest.main()