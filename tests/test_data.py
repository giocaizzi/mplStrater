import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from mplStrater.data import StrataFrame
import geopandas as gp
import pytest
import pyproj 

#first three rows of repository example
example_dataset="tests/test.csv"
epsg=32633

def partial_init(self,df,epsg):
    self.epsg=epsg
    self.df=df

class TestStrataFrame(unittest.TestCase):

    def setUp(self):
        self.df=pd.read_csv(example_dataset)

    def test_init_fail(self):
        d={}
        self.assertRaises(ValueError,StrataFrame,d,epsg)

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

    def test_group_data(self):
        data=StrataFrame.group_data(self.df,"matrice","lista_matrici").reset_index()
        data.set_index("punto",inplace=True)
        data_list=data.at["SI01","lista_matrici"]
        original_len=len(self.df[self.df["punto"]=="SI01"])
        #check that has one more value than the original
        self.assertEqual(len(data_list),original_len+1)

    @patch.object(StrataFrame,"__init__",partial_init)
    def test_patched_init(self):
        sf=StrataFrame(self.df,epsg)
        #lambda function otherwise throws attribute error
        self.assertRaises(AttributeError,lambda: sf.strataframe)

    @pytest.mark.wip
    @patch.object(StrataFrame,"__init__",partial_init)
    def test_set_df(self):
        sf=StrataFrame(self.df,epsg)
        sf.set_df()
        #test is df
        self.assertIsInstance(sf.strataframe,pd.DataFrame)
        #test points are the same
        punti_in=self.df.punto.unique().tolist()
        punti_out=sf.strataframe.punto.unique().tolist()
        self.assertEqual(len(punti_in),len(punti_out))
        
    @pytest.mark.wip
    @patch.object(StrataFrame,"__init__",partial_init)
    def test_geo_df(self):
        sf=StrataFrame(self.df,epsg)
        sf.set_df()
        sf.geodf()
        #crs is a pyproj object
        self.assertIsInstance(sf.strataframe.crs,pyproj.CRS)

if __name__=="__main__":
    unittest.main()