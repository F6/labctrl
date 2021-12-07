# -*- coding: utf-8 -*-

"""main_doc.py:
This module saves the bokeh app document so that all
other components see the same doc.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

from bokeh.plotting import curdoc

doc = curdoc()
