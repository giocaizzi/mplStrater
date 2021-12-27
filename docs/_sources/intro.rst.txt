This package allows to plot stratigraphic columns with python.

Passing to :code:`mplStrater`:

* some stratigraphic data stored in a ``pandas.DataFrame``
* a :code:`mplStrater.Legend` object

the package creates a series of :code:`mplStrater.strata.Columns` objects
that can be plotted, all together or singularly, on :code:`matplotlib.axes`. The columns
are plotted with the color and hatch scheme defined providing the legend object.

Packaged from a hardcoded script in quarantine in december 2021, by `@giocaizzi <https://github.com/giocaizzi>`_.