# -*- coding: utf-8 -*-

"""remote.py:
This module provides methods to communicate with a remote 
multiaxis stage server.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221109"


import requests
import json

class RemoteMultiaxisStage():
    def __init__(self, config:dict, max_retry=3) -> None:
        self.host = config["Host"]
        self.port = config["Port"]
        self.max_retry = max_retry
        self.api_url = 'http://{host}:{port}/'.format(host=self.host, port=self.port)

    def apicall(self, command:str):
        for i in range(self.max_retry):
            try:
                apicall = self.api_url + command
                response = requests.get(apicall)
                rc = response.content.decode()
                return json.loads(rc)
            except requests.exceptions.ConnectionError as err:
                print(err)
        print("Error: Cannot connect to remote stage, exceeded max retry {mr}".format(
            mr=self.max_retry))
        raise requests.exceptions.ConnectionError

    def online(self):
        """Tests if the remote stage server is online.
        Does not test if the remote server actually works, however."""
        return self.apicall('')


class RemoteThreeAxesStage(RemoteMultiaxisStage):
    def moveabs(self, x, y, z):
        return self.apicall('moveabs/{x:.3f},{y:.3f},{z:.3f}'.format(x=x, y=y, z=z))



# class RemoteTwoAxesStage(RemoteMultiaxisStage):
#     def moveabs(self, x, y):
#         return self.apicall('moveabs/{x:.3f},{y:.3f}'.format(x=x, y=y))


class RemoteHandlerThreeAxes:
    """
    To keep consistency between axes, only remote handler should have
    access to remote. This class implements methods to interact with
    remote for other components.
    """

    def __init__(self, config: dict, init_pos: list) -> None:
        self.config = config
        self.remote = RemoteThreeAxesStage(config)
        self.current_position = init_pos

    def online(self):
        return self.remote.online()

    def switch_remote(self, config: dict) -> None:
        self.remote = RemoteThreeAxesStage(config)

    def axis_moveabs(self, axis_name: str, pos: float):
        for i, axis_config in enumerate(self.config["Axes"]):
            if axis_config["Name"] == axis_name:
                self.current_position[i] = pos
                break
        return self.remote.moveabs(*self.current_position)
