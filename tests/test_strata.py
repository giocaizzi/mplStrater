import unittest
from matplotlib.colors import ListedColormap
from numpy import less_equal
from mplStrater.strata import Symbology,Legend,Column

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

    def test_error(self):
        #test error input
        d={}
        hatches=["","xxxxxxxxx",""]
        colors=["green","white","blue"]
        self.assertRaises(
            ValueError,
            Symbology,
            d,colors=colors,hatches=hatches)

class TestLegend(unittest.TestCase):

    def test_init(self):
        #matrix and hatches are symbology 
        l=Legend()
        self.assertIsInstance(l.matrix,Symbology)
        self.assertIsInstance(l.hatches,Symbology)

# class TestColumn(unittest.TestCase):

#     def setUp(self):
#         self.l=Legend()
#         self.c=Column(
#             name="P01",
#             legend=self.l,
#             coord=(5,5),
#             prof=5,
#             layers=[],

#         )
#         return 

#     def test(self):
#         pass

if __name__=="__main__":
    unittest.main()