# -*- coding: utf-8 -*-

"""bundle_bokeh.py:
This module provides the Bundle class for Bokeh UI widgets for 
testing and controlling 1D signal generators
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221208"

import base64
import numpy as np

from bokeh.models.widgets import TextInput, Button, RadioButtonGroup, FileInput
from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from labctrl.widgets.figure import FactoryFigure
from labctrl.utilities import ignore_connection_error, eval_float, eval_int
from .abstract import AbstractBundleSignalGenerator
from .remote import RemoteSignalGenerator


class BundleBokehSignalGenerator(AbstractBundleSignalGenerator):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat) -> None:
        super().__init__()
        self.lcfg = lcfg
        self.lstat = lstat
        self.config = bundle_config["Config"]
        self.name = self.config["Name"]
        self.remote = RemoteSignalGenerator(self.config)

        config = self.config  # Convenient alias
        name = self.name  # Convenient alias
        update_config = self.lcfg.update_config  # Convenient alias

        self.host = TextInput(title="Host", value=config["Host"])
        self.port = TextInput(title="Port", value=str(config["Port"]))
        self.working_mode = RadioButtonGroup(
            labels=config["WorkingModes"],
            active=(config["WorkingModes"].index(config["WorkingMode"]))
        )
        self.change_working_mode = Button(label="Change Working Mode")

        self.test_online = Button(label="Test Signal Generator Online")
        self.waveform_file = FileInput(accept=".txt")

        self.update_waveform_button = Button(
            label="Update Waveform", button_type='success')

        factory = FactoryFigure(lcfg, lstat)
        figure_bundle_config = dict()
        figure_bundle_config["Config"] = config["WaveformFigure"]
        self.waveform_figure = factory.generate_bundle(figure_bundle_config)

        # region host
        @update_config
        def __callback_host(attr, old, new):
            # no validation here because host can be literally anything,
            # it is just a param passed to remote API
            config["Host"] = self.host.value
            # regenerate remote when config updated
            self.remote = RemoteSignalGenerator(config)

        self.host.on_change('value', __callback_host)
        # endregion host

        # region port
        @update_config
        def __callback_port(attr, old, new):
            # no validation here because port can be literally anything,
            # it is just a param passed to remote API
            config["Port"] = eval_int(self.port.value)
            # regenerate remote when config updated
            self.remote = RemoteSignalGenerator(config)

        self.port.on_change('value', __callback_port)
        # endregion port

        # region working_mode
        @update_config
        def __callback_working_mode(attr, old, new):
            unit_index = int(self.working_mode.active)
            config["WorkingMode"] = config["WorkingModes"][unit_index]

        self.working_mode.on_change('active', __callback_working_mode)
        # endregion working_mode

        # region change_working_mode
        @ignore_connection_error
        def __callback_change_working_mode():
            response = self.remote.set_working_mode(config["WorkingMode"])
            self.lstat.fmtmsg(response)

        self.change_working_mode.on_click(__callback_change_working_mode)
        # endregion change_working_mode

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

        # region waveform_file
        @update_config
        def __callback_waveform_file(attr, old, new):
            self.lstat.expmsg("Loaded External Waveform")
            fcontent = base64.b64decode(
                self.waveform_file.value).decode()
            # print(fcontent)
            new_waveform = list(map(int, fcontent.split()))
            config["Waveform"] = new_waveform
            self.lstat.expmsg("New waveform: {}".format(config["Waveform"]))
            self.waveform_figure.update(
                np.arange(np.size(new_waveform)), np.array(new_waveform), self.lstat)

        self.waveform_file.on_change(
            'value', __callback_waveform_file)
        # endregion waveform_file

        # region update_waveform_button
        @ignore_connection_error
        def __callback_update_waveform_button():
            self.update_waveform(config["Waveform"])

        self.update_waveform_button.on_click(__callback_update_waveform_button)
        # endregion update_waveform_button

    def update_waveform(self, waveform: list[int]):
        self.remote.update_waveform(waveform)
