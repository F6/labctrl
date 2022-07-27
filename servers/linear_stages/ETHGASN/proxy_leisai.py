# -*- coding: utf-8 -*-

"""proxy.py:
This module provides proxied API for
a remote linear stage
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220727"


import json
import requests
from flask import Flask, Response

# some black magic here: always use 127.0.0.1 instead of localhost! (prevents ipv6)
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 5048
PROXY_NAME = "leisai"

app = Flask(__name__)



@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The proxy is ONLINE"
    res['name'] = "ETHGASN.leisai"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/moveabs/<command>")
def proxy_moveabs(command):
    # print(command)
    res = dict()
    res['success'] = True
    res['message'] = "The proxy has delivered request to server"
    res['name'] = "ETHGASN.leisai"
    apicall = "http://{PROXY_HOST}:{PROXY_PORT}/{PROXY_NAME}/moveabs/{command}".format(PROXY_HOST=PROXY_HOST, PROXY_PORT=PROXY_PORT, PROXY_NAME=PROXY_NAME, command=command)
    proxied_result = requests.get(apicall).content.decode()
    # proxied_result = json.loads(proxied_result)
    res['proxied'] = proxied_result
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

