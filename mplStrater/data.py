import pandas as pd
import numpy as np
import geopandas as gp

class StrataFrame:
    """

    StrataFrame is a `pandas.DataFrame` object with some added methods
    functional to stratigraphic column plotting.

    Arguments:
        epsg (str) : EPSG code string of GeoDataFrame CRS

    """

    def __init__(self,path_to_data=None,epsg=None):
        
        #geodf
        self.epsg=epsg

        #handle path_to_data values
        if path_to_data is not None and isinstance(path_to_data,str):
            self.df=pd.read_csv(path_to_data)
            self.set_df()
            self.geodf()
        else:
            raise ValueError("Must specify string path to a csv file containing stratigraphic information.")
        pass

    def set_df(self):
        """
        process the dataframe to get the desired information to plot the data.
        """
        profondita = self._group_layers()
        matrici = self._group_data("matrice","lista_matrici")
        pericolosita = self._group_data('pericolosita',"lista_pericolo")
        destino = self._group_data("smaltibilità_riutilizzo","destino")
        amianto_qual=self._group_data("amianto_qualitativa","amianto_qual")
        amianto_quant=self._group_data("amianto_quantitativa","amianto_quant")

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

    def _group_layers(self):
        """
        group layer data in required format.
        """
        profondita=self.df.groupby(['punto','x','y'])[['da','a']].agg(list)
        profondita["layers"]=profondita["da"]+profondita["a"]
        profondita=profondita.drop(["da","a"],axis=1)
        profondita['layers'] = profondita['layers'].apply(lambda x: np.unique(x))
        return profondita

    def _group_data(self,colname1,colname2):
        """
        group data in required format.

        Arguments:
            colname1,colname2 (str, :obj:`list` of :obj:`str`): column names for `pandas.groupBy`
        """
        #df con lista data
        data=self.df.groupby(['punto','x','y'])[colname1].apply(list).reset_index(name=colname2)
        #duplicazione ultimo elemento per pareggiare i conti
        for i in range(len(data)):
                temp=data.loc[i,colname2]
                temp.append(temp[-1])
                data.at[i,colname2]=temp
        return data