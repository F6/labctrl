# -*- coding: utf-8 -*-

"""Aerotech_proxy.py:
This module provides web RESTful API for
a remote linear stage

The linear stage is now installed at A304 for TR experiment
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

import requests
import json
from flask import Flask

proxied_url = 'http://192.168.2.2:5004'

app = Flask(__name__)


@app.route("/")
def online():
    return requests.get(proxied_url + '/').content.decode()


@app.route("/moveabs/<pos>")
def moveabs(pos):
    return requests.get(proxied_url + '/moveabs/{pos}'.format(pos)).content.decode()


@app.route("/autohome")
def autohome():
    return requests.get(proxied_url + '/autohome').content.decode()

@app.route("/absolute")
def absolute():
    return requests.get(proxied_url + '/absolute').content.decode()
