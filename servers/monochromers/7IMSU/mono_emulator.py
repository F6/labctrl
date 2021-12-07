# -*- coding: utf-8 -*-

"""mono_emulator.py:
This module provides web API for
development emulation of monosvr.py

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real environment, and that they return fabricated
data
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


from flask import Flask


app = Flask(__name__)

pos = 0


@app.route("/")
def online():
    return "[OK] The Monochromer Server is ONLINE"


@app.route("/getpos")
def getpos():
    global pos
    return "{:.0f}".format(pos + 1680)


@app.route("/moveto/<tpos>")
def moveto(tpos):
    global pos
    pos = int(tpos)
    return "[OK] Monochromer moving to abspos {}".format(pos)


@app.route("/stop")
def stop():
    return "[OK] Monochromer stopped moving"
