# -*- coding: utf-8 -*-

"""USB1020svr.py:
This module provides web API for
a remote linear servo stage

the servo is the silver one now installed at A304, the driver
for the servo is Autonics KR-55MC and the controller is Beijing
ART Technology USB1020.

for manual tweaking and param adjustments, use the official
ART software.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"

from flask import Flask
from USB1020 import USB1020

stage = USB1020()
# the device is never released! but this is ok because when the
#  user shuts down the server, the resources are automatically
#  released by the os
# this can interfere with other programs trying to
#  control the device, so just close the server before tweaking
stage.createDevice()

app = Flask(__name__)


@app.route("/")
def online():
    return "[OK] The USB1020 Server is ONLINE"


@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)
    stage.moveabs(pos)
    return "[OK] Moving to {pos}".format(pos=pos)
