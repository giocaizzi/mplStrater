import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gp
import numpy as np
import rasterio 
from rasterio.plot import show
import rio_color.operations as rio
from rio_color.colorspace import ColorSpace as cs
from rio_color.colorspace import convert_arr
from mplStrater.strata import *
import matplotlib.patheffects as pe
from matplotlib.gridspec import GridSpec

__version__="v0.0.1"

class StratigraphicMap:
    """
    This class is the core of mplStrater package.

    Arguments:
        path_to_data (str): path to stratigraphic information stored in csv file
        basemap_path (str): path to georeferenced raster to use as basemap.

    Attributes:
        df (:obj:`pandas.DataFrame`): dataframe with stratigrafic information. No gaps are allowed.
        f (:obj:`matplotlib.Figure`): matplotlib figure with stratigraphic map
        ax (:obj:`matplotlib.Axes`): matplotlib axes with stratigraphic map
        fig_kwd (dict): keywords to pass to `matplotlib.pyplot.subplots()`
        img_rgb (:obj:`numpy.array`): 3D array formed by R,G,B numpy 2D arrays
        img_alpha (:obj:`numpy.array`): 2D array of alpha channel
    """

    def __init__(self,path_to_data=None,basemap_path=None,fig_kwd=None,label_hardcoding=None):

        #handle path_to_data values
        if path_to_data is not None and isinstance(path_to_data,str):
            self.df=pd.read_csv(path_to_data)
            self.set_df()
        else:
            raise ValueError("Must specify string path to a csv file containing stratigraphic information.")

        #handle label_hardcoding
        self.label_hardcoding=label_hardcoding
        
        #handle fig_kwd
        if fig_kwd is None:
            self.fig_kwd={
                "figsize":(10,10),
                "dpi":300
            }
        elif isinstance(fig_kwd,dict):
            self.fig_kwd=fig_kwd
        else:
            raise ValueError("Incorrect fig_kwd argument. Must be None or dict.")

        #handle basemap
        if basemap_path is not None and isinstance(basemap_path,str):
            with rasterio.open(basemap_path) as basemap:
                self.img_rgb=basemap.read((1,2,3))
                self.img_alpha=basemap.read(4)
                self.img_transform=basemap.transform
            self.normalize_raster()
        elif basemap_path is None:
            self.img_rgb=None
            self.img_alpha=None
        else:
            raise ValueError("Must specify string path to a georeferenced raster.")


    def set_df(self,epsg=32633):
        """
        process the dataframe to get the desired information to plot the data.
        Sets the dataframe as GeoDataFrame of the given Coordinate Reference System (crs).

        Arguments:
            epsg (str) : EPSG code string of GeoDataFrame CRS
        """
        #df con lista matrici
        matrici=self.df.groupby(['punto','x','y'])['matrice'].apply(list).reset_index(name="lista_matrici")
        #duplicazione ultimo elemento per pareggiare i conti
        for i in range(len(matrici)):
                temp=matrici.loc[i,"lista_matrici"]
                temp.append(temp[-1])
                matrici.at[i,"lista_matrici"]=temp

        #df con pericolosità
        pericolosita=self.df.groupby(['punto','x','y'])['pericolosita'].apply(list).reset_index(name="lista_pericolo")
        for i in range(len(pericolosita)):
                temp=pericolosita.loc[i,"lista_pericolo"]
                temp.append(temp[-1])
                pericolosita.at[i,"lista_pericolo"]=temp

        # #df profondità
        profondita=self.df.groupby(['punto','x','y'])[['da','a']].agg(list)
        profondita["layers"]=profondita["da"]+profondita["a"]
        profondita=profondita.drop(["da","a"],axis=1)
        profondita['layers'] = profondita['layers'].apply(lambda x: np.unique(x))

        #destino
        destino=self.df.groupby(["punto","x","y"])["smaltibilità_riutilizzo"].apply(list).reset_index(name="destino")
        for i in range(len(pericolosita)):
                temp=destino.loc[i,"destino"]
                temp.append(temp[-1])
                destino.at[i,"destino"]=temp

        # # amianto
        amianto_qual=self.df.groupby(["punto","x","y"])["amianto_qualitativa"].apply(list).reset_index(name="amianto_qual")
        for i in range(len(pericolosita)):
                temp=amianto_qual.loc[i,"amianto_qual"]
                temp.append(temp[-1])
                amianto_qual.at[i,"amianto_qual"]=temp

        amianto_quant=self.df.groupby(["punto","x","y"])["amianto_quantitativa"].apply(list).reset_index(name="amianto_quant")
        for i in range(len(pericolosita)):
                temp=amianto_quant.loc[i,"amianto_quant"]
                temp.append(temp[-1])
                amianto_quant.at[i,"amianto_quant"]=temp
        
        #merged dfs
        merged=pd.merge(matrici,profondita,on=['punto','x','y'])
        merged=pd.merge(merged,pericolosita,on=['punto','x','y'])
        merged=pd.merge(merged,destino,on=["punto","x","y"])
        merged=pd.merge(merged,amianto_qual,on=["punto","x","y"])
        merged=pd.merge(merged,amianto_quant,on=["punto","x","y"])

        merged["scala"]=merged.layers.apply(max)
        self.max_profondita=merged.scala.max()

        self.merged_df=merged
        self.merged_df=gp.GeoDataFrame(self.merged_df, geometry=gp.points_from_xy(self.merged_df.x,self.merged_df.y))
        self.merged_df=self.merged_df.set_crs(epsg=epsg)
    

    def plot(self,legend):
        """
        creates figure and plots the data.
        """
        self.f,self.ax=plt.subplots(
            1,1,
            figsize=self.fig_kwd["figsize"],
            dpi=self.fig_kwd["dpi"],
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.tick_params(
            axis="both",
            which="both",
            left=False,
            bottom=False
        )
        self.plot_basemap()
        self.plot_points()
        self.plot_strata_columns(legend=legend)

    def plot_basemap(self,color_correction=True):
        """
        sets basemap if this has been correctly specified.

        Arguments:
            color_correction (bool): execute color correction with `rio-color` package.
        """
        if self.img_alpha is not None and self.img_rgb is not None and self.img_transform is not None :
            if color_correction is True:
                convert_arr(self.img_rgb, src=cs.rgb, dst=cs.lch)
                self.img_rgb=rio.saturation(self.img_rgb, 0.5)
            
            #ci riattacco alpha channel
            desaturated=np.concatenate((self.img_rgb,self.img_alpha),axis=0)

            #plotto
            show(desaturated,transform=self.img_transform,ax=self.ax)
        return 

    def normalize_raster(self):
        """
        Normalize content of georeferenced RGBA raster to to 0.0-1.0 format.
        """
        r=self.img_rgb[0,:,:].copy()
        g=self.img_rgb[1,:,:].copy()
        b=self.img_rgb[2,:,:].copy()

        r=(r-np.amin(r))/(np.amax(r)-np.amin(r))
        g=(g-np.amin(g))/(np.amax(g)-np.amin(g))
        b=(b-np.amin(b))/(np.amax(b)-np.amin(b))

        self.img_rgb=np.stack((r,g,b),axis=0)

        alpha=self.img_alpha.copy()
        self.img_alpha=(alpha-np.amin(alpha))/(np.amax(alpha)-np.amin(alpha))
        self.img_alpha=self.img_alpha[np.newaxis,:,:]

    def plot_points(self):
        """
        plot points
        """
        ####punti
        self.merged_df.plot(ax=self.ax,color="black",markersize=8)

        #labels
        for x, y, label in zip(self.merged_df.geometry.x, self.merged_df.geometry.y, self.merged_df.punto):
            if any(label in s for s in ["TI01","TI03","TI15","TI13","SI04","TI06","SI05","SI01","SI02","TI08","SI03","TI10"]):
                #destra
                # ax.annotate(label, xy=(x, y), xytext=(+5, 0), fontsize=5, textcoords="offset points",bbox=dict(facecolor='white', linewidth=0.5,edgecolor='k',pad=1))
                self.ax.annotate(label, xy=(x, y), xytext=(+5, 0), fontsize=5, textcoords="offset points",path_effects=[pe.withStroke(linewidth=2, foreground="white")])
            
            elif label == "SI07":
                self.ax.annotate(label, xy=(x, y), xytext=(+10, 0), fontsize=5, textcoords="offset points",path_effects=[pe.withStroke(linewidth=2, foreground="white")])

            
            elif any(label in s for s in ["TI14","TI18","TI07","TI17"]):
                #sinistra
                # ax.annotate(label, xy=(x, y), xytext=(-15, 0), fontsize=5, textcoords="offset points",bbox=dict(facecolor='white', linewidth=0.5,edgecolor='k',pad=1))
                self.ax.annotate(label, xy=(x, y), xytext=(-15, 0), fontsize=5, textcoords="offset points",path_effects=[pe.withStroke(linewidth=2, foreground="white")])

            else:
                # ax.annotate(label, xy=(x, y), xytext=(-5, 5), fontsize=5, textcoords="offset points",bbox=dict(facecolor='white',linewidth=0.5, edgecolor='k',pad=1))
                self.ax.annotate(label, xy=(x, y), xytext=(-5, 5), fontsize=5, textcoords="offset points",path_effects=[pe.withStroke(linewidth=2, foreground="white")])

    def savefig(self,path):
        """
        save figure

        Arguments:
            path (str): string path to save location.
        """
        return self.f.savefig(path)

    def plot_strata_columns(self,legend):
        """
        plot all stratigraphic columns in df.
        """
        #stratigraphy columns
        for i in range(len(self.merged_df)):
            c=Column(self.ax,legend,
                self.merged_df.loc[i,"punto"],
                (self.merged_df.loc[i,"x"],self.merged_df.loc[i,"y"]),
                self.merged_df.loc[i,"layers"],
                self.merged_df.loc[i,"lista_matrici"],
                self.merged_df.loc[i,"lista_pericolo"],
                self.merged_df.loc[i,"destino"],
                self.merged_df.loc[i,"scala"],
                self.merged_df.loc[i,"amianto_qual"],
                self.merged_df.loc[i,"amianto_quant"],
                self.max_profondita
            )
            c.plot_column()
            c.set_inset_params()
            c.label_column(hardcoding=self.label_hardcoding)
            