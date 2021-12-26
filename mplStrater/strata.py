from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd
import matplotlib
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch, PathPatch
import numpy as np

matplotlib.rcParams['hatch.linewidth'] = 0.4


class Symbology:
    """
    This is the symbology definition object for layers of the `mplStrater.strata.Column` object

    Can have either a fill color or a hatch.
    
    Arguments:
        d (dict): dict
        colors (list): list
        hatches (list): list
    
    Attributes:
        d (dict): number coded dictionary of string values.
        colors (list): list of colors
        cmap (:obj:`matplotlib.colors.ListedColormap`): cmap

    """
    def __init__(self,d=None,colors=None,hatches=None):
        self.d=d
        if colors is not None and hatches is None:
            self.colors=colors
            self.cmap = ListedColormap(self.colors)
        elif hatches is not None and colors is None:
            self.hatches=hatches
        else:
            ValueError("This symbology profile is not implemented.")

class Legend:
    """
    This sets the color-hatches profiles of the `mplStrater.strata.Column` object.
    """

    def __init__(self):
        self._set_matrix()
        self._set_hatch()
        pass

    def _set_matrix(self):
        """
        Set layer matrix symbology.
        """
        d={'Terreno conforme': 1, 'Riporto conforme': 2, 'Riporto non conforme': 3, 'Rifiuto': 4, 'Assenza campione':5}
        colors = ['lightgreen', 'darkgreen', 'orange', 'red',"white"]
        self.matrix=Symbology(d,colors=colors)

    def _set_hatch(self):
        """
        Set layer hatch symbology.
        """
        d={"Non pericoloso":1, "Pericoloso":2, "_":3}
        hatches=["","xxxxxxxxx",""]
        self.hatches=Symbology(d,hatches=hatches)
    
    def return_handles(self):
        """
        return handles to specified legend elements.
        """
        #legenda matrix
        matrix_h = [Patch(facecolor=col, label=k,linewidth=0.4,edgecolor="black") for k, col in zip(self.matrix.d.keys(), self.hatches.d.colors)]
        #legenda hatch
        #override legend due to temporary definition
        d3={"Non pericoloso":1, "Pericoloso":2}
        hatches=["","xxxxxxxxx"]
        hatches_h=[Patch(hatch=hatch,facecolor="red",linewidth=0.4,edgecolor="k",label=k) for k, hatch in zip(d3.keys(), hatches)]
        
        return matrix_h,hatches_h

class Column:
    """
    This objects is the single stratigraphic column.

    Attributes:
        name (str): name of the point
        legend(:obj:`mplStrater.strata.Legend`): legend object
        coord (:obj:`tuple`): coords (x,y)
        layers (list): ordered list of layers, encoded
        danger (list): ordered list of danger, encoded
        dest (str): label 1
        am_qual (str): label 2
        am_quant (str): label 3
    """

    def __init__(
            self,
            ax,legend,
            name,
            coord,
            prof,
            layers,
            danger,
            dest,scale,am_qual,am_quant,
            max_scale
            ):
        
        #default anchor it upper left
        loc=1

        #PROPRIETIES
        self.legend=legend
        self.name=name

        #INSET AXES
        self.inset = inset_axes(ax,
                    width=0.1,                     # inch
                    height=0.6*(scale/max_scale),                    # inch
                    bbox_transform=ax.transData, # data coordinates
                    bbox_to_anchor=coord,    # data coordinates
                    loc=loc)  # loc=lower left corner
        #DATAFRAME
        self.df=pd.DataFrame({'profondita': prof,#list
            'matrice': layers,
            "pericolo":danger,
            "destino":dest,
            "am_qual":am_qual,
            "am_quant":am_quant
        })

    def set_inset_params(self):
        """
        set inset parameters.
        """
        #linewidth of inset axes
        for axis in ['top','bottom','left','right']:
            self.inset.spines[axis].set_linewidth(0.4)
        
        self.inset.tick_params(length=0,labelsize=3,pad=1)
        self.inset.set_xticks([])  # hide ticks on the x-axis
        up_lim=self.df.profondita.iat[0]
        down_lim=self.df.profondita.iat[-1]
        self.inset.set_yticks([up_lim,down_lim])
        self.inset.invert_yaxis() 


    def fill_column(self):
        """
        prints the single `mplStrater.strata.Column` object onto a `mplStrater.StratigraphicMap`.
        """
        #matrici
        polycollection=self.inset.pcolormesh(
            [0, 1], self.df['profondita'],
            self.df['matrice'][:-1].map(self.legend.matrix.d).to_numpy().reshape(-1, 1),
            cmap=self.legend.matrix.cmap,
            vmin=1,
            vmax=len(self.legend.matrix.colors),linewidth=0.01,edgecolor="k"
        )

        #hatches
        pericolosita_val=self.df["pericolo"][:-1].map(self.legend.hatches.d).to_numpy()
        # print(pericolosita_val)
        for path, d3_val in zip(polycollection.get_paths(),pericolosita_val):
            hatch=self.legend.hatches.hatches[d3_val-1]
            if hatch!="":
                self.inset.add_patch(
                    PathPatch(
                        path,
                        hatch=hatch,
                        facecolor="none",
                        linewidth=0,
                        edgecolor="black")
                    )
    
    def hardcode_labels(self,hardcoding,locations,side):
        """
        hardcode labels.

        Arguments:
            hardcoding (dict): dictionary containing hardcoding parameters.
            locations (list): list of position of labels
            side (str): string `left` or `right`
        """
        #check if 
        if hardcoding is not None:
            if self.name in hardcoding:
                #move labels up or down
                for key in hardcoding[self.name]["movetext"]:
                    locations[int(key)]=locations[int(key)]+float(hardcoding[self.name]["movetext"][key])
                if hardcoding[self.name]["side"]!="":
                    side=hardcoding[self.name]["side"]
        return locations,side

    def _set_oppside(self,side):
        """
        set opposite side of a given side.
        """
        if side=="left":
            oppside="right"
        elif side=="right":
            oppside="left"
        else:
            raise ValueError("side not recognized.")
        return oppside
        
    def label_column(self,hardcoding):
        """
        labels single layers of stratigraphic column
        """
        #default side
        side="left"

        #get labels
        label_destino=self.df["destino"].to_list()[0:-1]
        label_am_qual=self.df["am_qual"].to_list()[0:-1]
        label_am_quant=self.df["am_quant"].to_list()[0:-1]

        #get positions
        label_positions=np.array(self.df["profondita"].to_list())
        label_positions=np.convolve(label_positions,np.ones(2),"valid")/2
        label_positions=label_positions.tolist()

        #hardcode labels
        label_positions,side=self.hardcode_labels(hardcoding,label_positions,side)

        #xy text
        if side=="right":
            xytext=(+12, 0)
        elif side=="left":
            xytext=(-7, 0)
        else:
            raise ValueError("side not recognized.")

        for pos,lbl,am1,am2 in zip(label_positions,label_destino,label_am_qual,label_am_quant):
            if lbl!="_":
                #complex label
                lbl = self._compose_label(lbl, am1, am2)
                #draw label
                self.inset.annotate(
                    lbl,
                    xy=(0, pos),
                    xytext=xytext,
                    fontsize=4,
                    textcoords="offset points",
                    ha=self._set_oppside(side),
                    va="center",
                    bbox=dict(
                        facecolor='white',
                        linewidth=0,
                        alpha=0.7,
                        pad=0.2
                    )
                )

    def _compose_label(self, lbl, am1, am2):
        """
        compose complex labels from three strings.
        """
        if am1=="non rilevato":
            lbl=lbl+" (Am: ass.)"
        if am1=="rilevato" and am2==0:
            lbl=lbl+" (Am: <LR)"
        elif am1=="rilevato" and am2>0:
            lbl=lbl+f" (Am: {am2} mg/kg)"
        return lbl
