import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from mplStrater.data import StrataFrame
import geopandas as gp

#first three rows of repository example
example={'x': {0: 204026.93, 1: 204026.93, 2: 204026.93},
'y': {0: 4973197.522, 1: 4973197.522, 2: 4973197.522},
'z': {0: 258.399, 1: 258.399, 2: 258.399},
'punto': {0: 'SI01', 1: 'SI01', 2: 'SI01'},
'campione': {0: '1', 1: '2', 2: '2'},
'da': {0: 0.0, 1: 0.6, 2: 2.0},
'a': {0: 0.6, 1: 2.0, 2: 3.5},
'area': {0: '2A', 1: '2A', 2: '2A'},
'matrice': {0: 'Riporto conforme', 1: 'Assenza campione', 2: 'Rifiuto'},
'pericolosita': {0: '_', 1: '_', 2: 'Pericoloso'},
'sostanza_pericolosità': {0: np.nan, 1: '_', 2: 'PIOMBO'},
'smaltibilità_riutilizzo': {0: '_', 1: '_', 2: 'IA'},
'amianto_qualitativa': {0: '_', 1: '_', 2: 'non rilevato'},
'amianto_quantitativa': {0: -1, 1: -1, 2: -1}}
epsg=32633

def partial_init(self,df,epsg):
    self.epsg=epsg
    self.df=df

class TestStrataFrame(unittest.TestCase):

    def setUp(self):
        self.df=pd.DataFrame(example)

    def test_init_fail(self):
        d={}
        self.assertRaises(ValueError,StrataFrame,d,epsg)
    
    def test_init_correct(self):
        sf=StrataFrame(self.df,epsg)
        self.assertIsInstance(sf.strataframe,gp.GeoDataFrame)
    
    # @patch(StrataFrame,"__init__",partial_init)
    # def test_set_df(self):
    #     sf=StrataFrame(self.df,epsg)
    #     pass

if __name__=="__main__":
    unittest.main()