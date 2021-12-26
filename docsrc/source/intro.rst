This package allows to plot stratigraphic columns with python.

.. note ::
    This is project is under developement and it has not been yet released.

Passing to :code:`mplStrater`:

* some stratigraphic data **without missing layers** stored in a CSV file
* a :code:`mplStrater.Legend` object in which 

the package creates a :code:`matplotlib.axes` object in which a
series of :code:`mplStrater.strata.Columns` are plotted. Strata columns are inset axes of a main
:code:`matplotlib.figure` called with the package initialization.

Packaged from a hardcoded script in quarantine in december 2021, by `@giocaizzi <https://github.com/giocaizzi>`_.