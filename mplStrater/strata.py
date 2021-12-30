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
    
    Arguments:
        d (dict): dict, containing a pair (key,progressive_unique_index). Must start from 1. ::

            example_dict={
                "soil":1,
                "sand":2,
                "clay":3
            }

        fill (list): list of fill values
        hatches (list): list of hatch values
    
    Attributes:
        d (dict): encoded dictionary of string values.
        fill (list): list of fill values
        cmap (:obj:`matplotlib.colors.ListedColormap`): cmap
        hatches (list): list of hatch values

    """
    def __init__(self,d=None,fill=None,hatches=None):
        self.d=d
        if fill is not None and hatches is None:
            self.fill=fill
            self.cmap = ListedColormap(self.fill)
        elif hatches is not None and fill is None:
            self.hatches=hatches
        else:
            raise ValueError("This symbology profile is not implemented.")

class Legend:
    """
    This sets the color-hatches profiles of the `mplStrater.strata.Column` object.
    Must be feed with `fill_dict` and `hatch_dict` dictionary, consisting of *(key,value)* pair.
    Defines two separate `mplStrater.strata.Symbology` objects accessible from the `fill` or `hatch` attribute.

    Used for plotting `mplStrater.strata.Columns` both independently and in the `mplStrater.StratigraphicMap` context.

    `Hatch` and `fill` values must be string-encoded matplotlib colors and hatches.

    Arguments:
        fill_dict (dict): dictionary of fill *(key,value)* pair.
        hatch_dict (dict): dictionary of hatch *(key,value)* pair.
    """

    def __init__(self,fill_dict,hatch_dict):
        self.set_fill(fill_dict)
        self.set_hatches(hatch_dict)
        pass

    def set_fill(self,dict):
        """
        Set layer fill symbology.
        """
        d,values=self._unpack_dict(dict)
        self.fill=Symbology(d,fill=values)

    def set_hatches(self,dict):
        """
        Set layer hatch symbology.
        """
        d,values=self._unpack_dict(dict)
        self.hatches=Symbology(d,hatches=values)
    
    def _unpack_dict(self,d):
        """
        sets dictionary passed to `mpl.Strater` in a format required by the plotting methods.
        """
        values=list(d.values())
        return dict(zip(d.keys(),range(1,len(d)+1))),values
    
    # def return_handles(self):
    #     """
    #     return handles to specified legend elements.
    #     """
    #     #legenda matrix
    #     matrix_h = [Patch(facecolor=col, label=k,linewidth=0.4,edgecolor="black") for k, col in zip(self.fill.d.keys(), self.hatches.d.colors)]
    #     #legenda hatch
    #     #override legend due to temporary definition
    #     d3={"Non pericoloso":1, "Pericoloso":2}
    #     hatches=["","xxxxxxxxx"]
    #     hatches_h=[Patch(hatch=hatch,facecolor="red",linewidth=0.4,edgecolor="k",label=k) for k, hatch in zip(d3.keys(), hatches)]
        
    #     return matrix_h,hatches_h

class Column:
    """
    This objects is the single stratigraphic column.

    Attributes:
        ax (:obj:`matplotlib.axes`): axes in which plot column
        legend(:obj:`mplStrater.strata.Legend`): legend object
        id (str): id of the point
        coord (:obj:`tuple`): coords (x,y)
        scale (float): scale of column
        max_scale (float): scale of most deep column (for scaling)
        layers (list): list of layers interfaces 
        fill_list (list): ordered list of layers
        hatch_list (list): ordered list of hatches
        lbl1 (str): label 1
        lbl2 (str): label 2
        lbl3 (str): label 3
    """

    def __init__(self,
            ax,legend,
            id,
            coord,
            scale,
            max_scale,
            layers,
            fill_list,
            hatch_list,
            lbl1_list,lbl2_list,lbl3_list
            ):
        
        #default anchor it upper left
        loc=1

        #PROPRIETIES
        self.legend=legend
        self.id=id

        #INSET AXES
        self.inset = inset_axes(ax,
                    width=0.1,                     # inch
                    height=0.6*(scale/max_scale),                    # inch
                    bbox_transform=ax.transData, # data coordinates
                    bbox_to_anchor=coord,    # data coordinates
                    loc=loc)  # loc=lower left corner
        #DATAFRAME
        self.df=pd.DataFrame({
            'layers': layers,#list
            'fill': fill_list,
            "hatch":hatch_list,
            "lbl1":lbl1_list,
            "lbl2":lbl2_list,
            "lbl3":lbl3_list
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
        up_lim=self.df.layers.iat[0]
        down_lim=self.df.layers.iat[-1]
        self.inset.set_yticks([up_lim,down_lim])
        self.inset.invert_yaxis() 


    def fill_column(self):
        """
        prints the single `mplStrater.strata.Column` object onto a `mplStrater.StratigraphicMap`.
        """
        #matrici
        polycollection=self.inset.pcolormesh(
            [0, 1], self.df['layers'],
            self.df['fill'][:-1].map(self.legend.fill.d).to_numpy().reshape(-1, 1),
            cmap=self.legend.fill.cmap,
            vmin=1,
            vmax=len(self.legend.fill.fill),linewidth=0.01,edgecolor="k"
        )

        #hatches
        pericolosita_val=self.df["hatch"][:-1].map(self.legend.hatches.d).to_numpy()
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
            if self.id in hardcoding:
                #move labels up or down
                for key in hardcoding[self.id]["movetext"]:
                    locations[int(key)]=locations[int(key)]+float(hardcoding[self.id]["movetext"][key])
                if hardcoding[self.id]["side"]!="":
                    side=hardcoding[self.id]["side"]
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
        lbl1=self.df["lbl1"].to_list()[0:-1]
        lbl2=self.df["lbl2"].to_list()[0:-1]
        lbl3=self.df["lbl3"].to_list()[0:-1]

        #get positions
        label_positions=np.array(self.df["layers"].to_list())
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

        for pos,l1,l2,l3 in zip(label_positions,lbl1,lbl2,lbl3):
            if l1!="_":
                #complex label
                l1 = self._compose_label(l1, l2, l3)
                #draw label
                self.inset.annotate(
                    l1,
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

    def _compose_label(self, l1, l2, l3):
        """
        compose complex labels from three strings.
        """
        if l2=="non rilevato":
            l1=l1+" (Am: ass.)"
        if l2=="rilevato" and l3==0:
            l1=l1+" (Am: <LR)"
        elif l2=="rilevato" and l3>0:
            l1=l1+f" (Am: {l3} mg/kg)"
        return l1
