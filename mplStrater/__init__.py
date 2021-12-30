import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gp
import numpy as np
import rasterio 
from rasterio.plot import show
import rio_color.operations as rio
from rio_color.colorspace import ColorSpace as cs
from rio_color.colorspace import convert_arr
from mplStrater.strata import Column
import matplotlib.patheffects as pe
from matplotlib.gridspec import GridSpec

__version__="0.0.5"

class StratigraphicMap:
    """
    This class is the core of mplStrater package.

    Arguments:
        strataframe (:obj:`mplStrater.data.StrataFrame`): a StrataFrame object containing data to be plotted.
        path_to_data (str): path to stratigraphic information stored in csv file
        basemap_path (str): path to georeferenced raster to use as basemap.

    Attributes:
        strataframe (:obj:`mplStrater.data.StrataFrame`): the linked StrataFrame object
        df (:obj:`pandas.DataFrame`): dataframe with stratigrafic information grouped by point. 
        f (:obj:`matplotlib.Figure`): matplotlib figure with stratigraphic map
        ax (:obj:`matplotlib.Axes`): matplotlib axes with stratigraphic map
        fig_kwd (dict): keywords to pass to `matplotlib.pyplot.subplots()`
        img_rgb (:obj:`numpy.array`): 3D array formed by R,G,B numpy 2D arrays
        img_alpha (:obj:`numpy.array`): 2D array of alpha channel
    """

    def __init__(self,strataframe,basemap_path=None,fig_kwd=None,label_hardcoding=None):
        #strataframe
        self.strataframe=strataframe
        self.df=strataframe.strataframe
        
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
        self.plot_basemap(self.ax)
        self.plot_points(self.ax)
        self.plot_strata_columns(legend=legend,ax=self.ax)

    def plot_basemap(self,ax,color_correction=True):
        """
        sets basemap if this has been correctly specified.

        Arguments:
            ax (:obj:`matplotlib.axes`) ax on which to plot the points.
            color_correction (bool): execute color correction with `rio-color` package.

        """
        if self.img_alpha is not None and self.img_rgb is not None and self.img_transform is not None :
            if color_correction is True:
                convert_arr(self.img_rgb, src=cs.rgb, dst=cs.lch)
                self.img_rgb=rio.saturation(self.img_rgb, 0.5)
            
            #ci riattacco alpha channel
            desaturated=np.concatenate((self.img_rgb,self.img_alpha),axis=0)

            #plotto
            show(desaturated,transform=self.img_transform,ax=ax)
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

    def plot_points(self,ax):
        """
        plot points

        Arguments:
            ax (:obj:`matplotlib.axes`) ax on which to plot the points.
        """
        ####punti
        self.df.plot(ax=ax,color="black",markersize=8)
        #labels
        for x, y, label in zip(self.df.geometry.x, self.df.geometry.y, self.df.ID):
            ax.annotate(
                label,
                xy=(x, y),
                xytext=(-5, 0),
                ha="right",
                fontsize=5,
                textcoords="offset points",
                path_effects=[
                    pe.withStroke(
                        linewidth=2,
                        foreground="white"
                    )])

    def savefig(self,path):
        """
        save figure

        Arguments:
            path (str): string path to save location.
        """
        return self.f.savefig(path)

    def plot_strata_columns(self,legend,ax):
        """
        plot all stratigraphic columns in strataframe.
        Arguments:
            ax (:obj:`matplotlib.axes`) ax on which to plot the points.
        """
        #stratigraphy columns
        for i in range(len(self.df)):
            c=Column(
                #figure
                ax,legend,
                #id
                self.df.loc[i,"ID"],
                #coords
                (0.9,0.9),
                #scale
                self.df.loc[i,"scale"],
                3,
                #stratigraphic data
                self.df.loc[i,"layers"],
                self.df.loc[i,"fill_list"],
                self.df.loc[i,"hatch_list"],
                #labels
                self.df.loc[i,"lbl1_list"],
                self.df.loc[i,"lbl2_list"],
                self.df.loc[i,"lbl3_list"])
            c.fill_column()
            c.set_inset_params()
            c.label_column(hardcoding=self.label_hardcoding)
            