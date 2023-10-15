# -*- coding: utf-8 -*-

"""ws.py:
Websocket connection manager, parser and authenticator.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231009"

# std libs
import logging
# third-party libs
from fastapi import WebSocket
# own package
from .auth import validate_token_ws, TokenData

lg = logging.getLogger(__name__)


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, TokenData | None] = {}

    async def connect(self, websocket: WebSocket):
        """
        Connect to a websocket and wait for authentication message.
        If authentication fails, closes connection with WebSocket 1008 Policy Violation
        """
        await websocket.accept()
        # register at manager, but not authorized yet.
        self.active_connections[websocket] = None
        # After connection established, the first message must be an authentication message.
        # If user sent non-JSON data, the error is not caught here. Instead, all errors except validation error are
        # caught in the outer infinite loop of the endpoint.
        auth_data: dict = await websocket.receive_json()
        token_data = validate_token_ws(auth_data.get("token"))
        self.active_connections[websocket] = token_data
        await websocket.send_json({"auth_result": "success"})

    def disconnect(self, websocket: WebSocket):
        """
        When a websocket closes, remove it from manager.
        Please note that this function is intended to be called when connection is closed. 
        But this function does NOT close the connection.
        """
        if websocket in self.active_connections:
            self.active_connections.pop(websocket)
        else:
            lg.info(
                "Cannot disconnect ws:{} from manager because it is not connected to this manager.".format(websocket))

    async def broadcast(self, message: dict):
        """
        Send a message to all authenticated connections.
        """
        for connection, token_data in self.active_connections.items():
            if token_data:
                # only send message to authenticated clients
                await connection.send_json(message)
