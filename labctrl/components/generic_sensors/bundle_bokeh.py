# -*- coding: utf-8 -*-

"""
bundle_bokeh.py:

This module implements widgets with Bokeh package, according to abstract bundle definations.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221227"

import base64
import json
import time
import numpy as np
from threading import Thread
from bokeh.models.widgets import Button, FileInput, RadioButtonGroup, TextInput

from labctrl.widgets.figure import FactoryFigure
from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from labctrl.utilities import (ignore_connection_error,
                               eval_float,
                               eval_int)

from .abstract import AbstractBundleGenericSensor
from .remote import RemoteSensor
from .utils import calculate_dt


class BundleSensor(AbstractBundleGenericSensor):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat) -> None:
        super().__init__()

        self.config: dict = bundle_config["Config"]  # Axis Config
        self.name: str = self.config["Name"]
        self.lcfg = lcfg
        self.lstat = lstat
        update_config = lcfg.update_config
        config = self.config  # Alias for easier access
        name = self.name  # Alias for easier access

        # register at lstat to keep track of working mode states, etc.
        lstat.stat[name] = dict()

        self.remote = RemoteSensor(config)

        # ======== Param Configs ========
        self.host = TextInput(title="Host", value=config["Host"])
        self.port = TextInput(title="Port", value=str(config["Port"]))
        self.sensor_config_file = FileInput(accept=".json")
        # ======== Interactive Elements ========
        self.test_online = Button(label="Test Sensor Online")
        self.submit_config = Button(
            label='Submit Config to Sensor', button_type="warning")
        self.manually_retrive_data = Button(
            label='Retrive Data from Sensor')
        self.start_retrive_data = Button(
            label='Start Retriving Data', button_type="success")
        self.stop_retrive_data = Button(
            label='Stop Retriving Data', button_type="warning")
        # ======== Composites ========
        # no composites required

        # region host
        @update_config
        def __callback_host(attr, old, new):
            # no validation here because host can be literally anything,
            # it is just a param passed to remote API
            config["Host"] = self.host.value
            # regenerate remote when config updated
            self.remote = RemoteSensor(config)

        self.host.on_change('value', __callback_host)
        # endregion host

        # region port
        @update_config
        def __callback_port(attr, old, new):
            # no validation here because port can be literally anything,
            # it is just a param passed to remote API
            config["Port"] = eval_int(self.port.value)
            # regenerate remote when config updated
            self.remote = RemoteSensor(config)

        self.port.on_change('value', __callback_port)
        # endregion port

        # region sensor_config_file
        @update_config
        def __callback_sensor_config_file(attr, old, new):
            self.lstat.expmsg("Loaded sensor config file.")
            fcontent = base64.b64decode(
                self.sensor_config_file.value).decode()
            # print(fcontent)
            config["SensorConfig"] = json.loads(fcontent)

        self.sensor_config_file.on_change(
            'value', __callback_sensor_config_file)
        # endregion sensor_config_file

        # region test_online
        def __callback_test_online():
            try:
                self.lstat.fmtmsg(self.remote.online())
            except Exception as inst:
                print(type(inst), inst.args)
                self.lstat.expmsg(
                    "[Error] Nothing from remote, server is probably down.")

        self.test_online.on_click(__callback_test_online)
        # endregion test_online

        # region submit_config
        @ignore_connection_error
        def __callback_submit_config():
            response = self.set_sensor_config(
                config["SensorConfig"])
            lstat.fmtmsg(response)

        self.submit_config.on_click(__callback_submit_config)
        # endregion submit_config

        # region manually_retrive_data
        @ignore_connection_error
        def __callback_manually_retrive_data():
            response = self.get_sensor_data()
            lstat.fmtmsg(response)

        self.manually_retrive_data.on_click(__callback_manually_retrive_data)
        # endregion manually_retrive_data


        self.data_retriving_task_running = False
        self.data_retriving_thread = None

        # region start_retrive_data
        @ignore_connection_error
        def __callback_start_retrive_data():
            self.data_retriving_task_running = True
            self.data_retriving_thread = Thread(target=self.data_retriving_task)
            self.data_retriving_thread.start()

        self.start_retrive_data.on_click(__callback_start_retrive_data)
        # endregion start_retrive_data

        # region stop_retrive_data
        def __callback_stop_retrive_data():
            self.data_retriving_task_running = False

        self.stop_retrive_data.on_click(__callback_stop_retrive_data)
        # endregion stop_retrive_data

    def data_retriving_task(self):
        while self.data_retriving_task_running:
            response = self.get_sensor_data()
            self.lstat.fmtmsg(response)
            time.sleep(0.1)

    def get_sensor_data(self) -> dict:
        return self.remote.get_sensor_data()

    def set_sensor_config(self, config: dict) -> dict:
        return self.remote.set_sensor_config(config)
