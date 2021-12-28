import pandas as pd
import numpy as np
import geopandas as gp

class StrataFrame:
    """

    StrataFrame is a `pandas.DataFrame` object with some added methods
    functional to stratigraphic column plotting.

    Arguments:
        df (:obj:`pandas.DataFrame`): dataframe of stratigraphic data.
        epsg (str) : EPSG code string of GeoDataFrame CRS

    """

    def __init__(self,df=None,epsg=None):
        
        #geodf
        self.epsg=epsg

        #handle path_to_data values
        if df is not None and isinstance(df,pd.DataFrame):
            self.df=df
            self.set_df()
            self.geodf()
        else:
            raise ValueError("Must provide a pandas dataframe with stratigraphic data.")
        pass

    def set_df(self):
        """
        process the dataframe to get the desired information to plot the data.
        """
        profondita = _group_layers(self.df)
        matrici = _group_data(self.df,"matrice","lista_matrici")
        pericolosita = _group_data(self.df,'pericolosita',"lista_pericolo")
        destino = _group_data(self.df,"smaltibilità_riutilizzo","destino")
        amianto_qual=_group_data(self.df,"amianto_qualitativa","amianto_qual")
        amianto_quant=_group_data(self.df,"amianto_quantitativa","amianto_quant")

        #merged dfs
        merged=pd.merge(matrici,profondita,on=['punto','x','y'])
        merged=pd.merge(merged,pericolosita,on=['punto','x','y'])
        merged=pd.merge(merged,destino,on=["punto","x","y"])
        merged=pd.merge(merged,amianto_qual,on=["punto","x","y"])
        merged=pd.merge(merged,amianto_quant,on=["punto","x","y"])

        #scala and max profondità 
        merged["scala"]=merged.layers.apply(max)
        self.max_profondita=merged.scala.max()
        #store output
        self.strataframe=merged

    def geodf(self):
        """
        Sets the strataframe as GeoDataFrame of the given Coordinate Reference System (crs).
        """
        self.strataframe=gp.GeoDataFrame(self.strataframe, geometry=gp.points_from_xy(self.strataframe.x,self.strataframe.y))
        self.strataframe=self.strataframe.set_crs(epsg=self.epsg)

def _group_layers(df):
    """
    group layer data in required format.

    Arguments:
        df (:obj:`pandas.DataFrame`): dataframe of stratigraphic data.
    """
    profondita=df.groupby(['punto','x','y'])[['da','a']].agg(list)
    profondita["layers"]=profondita["da"]+profondita["a"]
    profondita=profondita.drop(["da","a"],axis=1)
    profondita['layers'] = profondita['layers'].apply(lambda x: np.unique(x))
    return profondita

def _group_data(df,colname1,colname2):
    """
    group data in required format.

    Arguments:
        df (:obj:`pandas.DataFrame`): dataframe of stratigraphic data.
        colname1,colname2 (str, :obj:`list` of :obj:`str`): column names for `pandas.groupBy`
    """
    #df con lista data
    data=df.groupby(['punto','x','y'])[colname1].apply(list).reset_index(name=colname2)
    #duplicazione ultimo elemento per pareggiare i conti
    for i in range(len(data)):
            temp=data.loc[i,colname2]
            temp.append(temp[-1])
            data.at[i,colname2]=temp
    return data