# -*- coding: utf-8 -*-

"""PMC48MT6_server.py:
This module provides web API for
a remote stepper motor stage

The controller is from Ningbo Adhon, no document or information
of their product can be found online, so not sure if the driver
works for all their devices.

The company seems to be closed years ago, so this will probably
be replaced soon.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211020"

from flask import Flask
from PMC48MT6 import PMC48MT6


# on creation of the server, the serial port is open and then never
# released, not sure if this will cause any strange behaviour, so be
# cautious for this
stage = PMC48MT6()

app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] The PMC48MT6 Server is ONLINE"


@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)
    stage.moveabs(pos)
    return "[OK] Moving to {pos}".format(pos=pos)

@app.route("/autohome")
def autohome():
    stage.autohome()
    return "[OK] Moving to home"

