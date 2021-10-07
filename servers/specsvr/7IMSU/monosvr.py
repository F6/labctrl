# -*- coding: utf-8 -*-

"""monosvr.py:
This module provides web API for
a remote monochromer 7IMSU
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


from flask import Flask
from mono import MonoController

com = 'COM3'
mono = MonoController(com)

app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] The Monochromer Server is ONLINE"


@app.route("/getpos")
def getpos():
    pos = mono.getpos()
    return "{:.0f}".format(pos)


@app.route("/moveto/<tpos>")
def moveto(tpos):
    res = mono.moveto(int(tpos))
    return "[OK] Monochromer moving to abspos {}".format(res)


@app.route("/stop")
def stop():
    mono.stopmoving()
    return "[OK] Monochromer stopped moving"
