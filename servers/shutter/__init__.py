# -*- coding: utf-8 -*-

"""
labctrl/servers/shutter:

## Introduction

This package provides remote API for a shutter controller with authentication.
Several interfaces are provided:

1. RESTful API over HTTP protocol for non-blocking asynchronous operations.

2. WebSocket RPC interface for time-critical operations.

To load the server application, setup SECRET in config.json, and run at root directory of labctrl:

(fastapi) $ uvicorn servers.shutter.main:app

or use the server loader.

## Package

shutter
    - shutter.py: provides ShutterController class as an asynchronous interface to manage and operate the shutter.
    - main.py: FastAPI application for HTTP API and WebSocket endpoint.
    - auth.py: authentication module for generating and varifying JWTs.
    - config.py: data model for config.
    - ws.py: websocket message parsing and responsing module.

## Scripts

shutter
    - register.py: generates a new user config according to input and insert it into config file.

P.S.:

1. The shutter controller is the self-made one (gray aluminum box).
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231009"

from .shutter import ShutterController
