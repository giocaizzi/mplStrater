import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from mplStrater.data import StrataFrame
import geopandas as gp
import pytest

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
    
    # def test_init_correct(self):
    #     sf=StrataFrame(self.df,epsg)
    #     self.assertIsInstance(sf.strataframe,gp.GeoDataFrame)

    def test_group_layers(self):
        profondita=StrataFrame.group_layers(self.df).reset_index()
        profondita.set_index("punto",inplace=True)
        profondita_l=profondita.at["SI01","layers"].tolist()
        original_len=len(self.df[self.df["punto"]=="SI01"])
        #check that has one more value than the original
        self.assertEqual(len(profondita_l),original_len+1)
        #check that is sorted
        self.assertListEqual(profondita_l,sorted(profondita_l))
        #check that there are no duplicates
        self.assertEqual(len(profondita_l), len(set(profondita_l)))

    @pytest.mark.wip
    def test_group_data(self):
        data=StrataFrame.group_data(self.df,"matrice","lista_matrici").reset_index()
        data.set_index("punto",inplace=True)
        data_list=data.at["SI01","lista_matrici"]
        original_len=len(self.df[self.df["punto"]=="SI01"])
        #check that has one more value than the original
        self.assertEqual(len(data_list),original_len+1)
    
    # @patch.object(StrataFrame,"__init__",partial_init)
    # def test_patched_init(self):
    #     sf=StrataFrame(self.df,epsg)
    #     self.assertRaises(AttributeError,sf.strataframe)

if __name__=="__main__":
    unittest.main()