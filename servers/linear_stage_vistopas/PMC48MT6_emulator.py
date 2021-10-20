# -*- coding: utf-8 -*-

"""PMC48MT6_emulator.py:
This module provides web API for
development emulation of PMC48MT6_server.py

The behaviour of these APIs should be identical
to the corresponding server app, except that they don't do
anything in real enviroment, and that they return fabricated
data
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211020"

from flask import Flask
import time

app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] The USB1020 Server is ONLINE"


@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)
    # time.sleep(0.1)
    return "[OK] Moving to {pos}".format(pos=pos)
