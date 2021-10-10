# -*- coding: utf-8 -*-

"""USB1020emu.py:
This module provides web API for
development emulation of USB1020svr.py

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real enviroment, and that they return fabricated
data
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

from flask import Flask

app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] The USB1020 Server is ONLINE"


@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)
    return "[OK] Moving to {pos}".format(pos=pos)
