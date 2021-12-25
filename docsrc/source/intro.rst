This package allows to plot stratigraphic columns with matplotlib.

.. warning ::
    This is project is under developement

Given stratigraphic data **without missing layers** sored from a CSV file,
specified during the initialization of :code:`mplStrater`, and a :code:`mplStrater.Legend` object in which 
is specified the map symbology, the package creates a :code:`matplotlib.axes` object in which a
series of :code:`mplStrater.strata.Columns` are plotted. Strata columns are inset axes of a main
:code:`matplotlib.figure` called with the package initialization.

Packaged from a hardcoded script in quarantine in december 2021, by `@giocaizzi <https://github.com/giocaizzi>`_.