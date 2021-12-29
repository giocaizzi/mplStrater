import unittest
from unittest.mock import patch
import pandas as pd
from mplStrater.data import StrataFrame
import geopandas as gp
import pytest
import pyproj

def partial_init(self,df,epsg):
    self.epsg=epsg
    self.df=df

@pytest.mark.usefixtures("test_data")
class TestStrataFrame(unittest.TestCase):

    def test_init_fail(self):
        d={}
        self.assertRaises(ValueError,StrataFrame,d,self.epsg)

    def test_fixture_test_data(self):
        assert hasattr(self, "test_data")
        assert isinstance(self.test_data, pd.DataFrame)

    def test_group_layers(self):
        profondita=StrataFrame.group_layers(self.test_data).reset_index()
        profondita.set_index("punto",inplace=True)
        profondita_l=profondita.at["SI01","layers"].tolist()
        original_len=len(self.test_data[self.test_data["punto"]=="SI01"])
        #check that has one more value than the original
        assert len(profondita_l)== original_len+1
        #check that is sorted
        assert profondita_l==sorted(profondita_l)
        #check that there are no duplicates
        assert  len(profondita_l) == len(set(profondita_l))

    def test_group_data(self):
        data=StrataFrame.group_data(self.test_data,"matrice","lista_matrici").reset_index()
        data.set_index("punto",inplace=True)
        data_list=data.at["SI01","lista_matrici"]
        original_len=len(self.test_data[self.test_data["punto"]=="SI01"])
        #check that has one more value than the original
        self.assertEqual(len(data_list),original_len+1)

    @patch.object(StrataFrame,"__init__",partial_init)
    def test_patched_init(self):
        sf=StrataFrame(self.test_data,self.epsg)
        #lambda function otherwise throws attribute error
        self.assertRaises(AttributeError,lambda: sf.strataframe)

    @patch.object(StrataFrame,"__init__",partial_init)
    def test_set_df(self):
        sf=StrataFrame(self.test_data,self.epsg)
        sf.set_df()
        #test is df
        self.assertIsInstance(sf.strataframe,pd.DataFrame)
        #test points are the sameself.
        punti_in=self.test_data.punto.unique().tolist()
        punti_out=sf.strataframe.punto.unique().tolist()
        self.assertEqual(len(punti_in),len(punti_out))
        
    @patch.object(StrataFrame,"__init__",partial_init)
    def test_geo_df(self):
        sf=StrataFrame(self.test_data,self.epsg)
        sf.set_df()
        sf.geodf()
        #crs is a pyproj object
        self.assertIsInstance(sf.strataframe.crs,pyproj.CRS)

if __name__=="__main__":
    unittest.main()