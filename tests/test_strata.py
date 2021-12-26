import unittest
from matplotlib.colors import ListedColormap


from matplotlib import colors
from mplStrater.strata import Symbology

class TestSymbology(unittest.TestCase):

    def test_color(self):
        colors=["green","white","blue"]
        s=Symbology(d={},colors=colors)
        self.assertIsInstance(s.d,dict)
        self.assertEqual(set(s.colors),set(colors))
        self.assertIsInstance(s.cmap,ListedColormap)
    
    def test_hatches(self):
        hatches=["","xxxxxxxxx",""]
        s=Symbology(d={},hatches=hatches)
        self.assertIsInstance(s.d,dict)
        self.assertEqual(set(s.hatches),set(hatches))    

if __name__=="__main__":
    unittest.main()