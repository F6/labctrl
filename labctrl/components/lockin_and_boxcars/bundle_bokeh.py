# -*- coding: utf-8 -*-

"""
bundle_bokeh.py:

This module implements widgets with Bokeh package, according to abstract bundle
definations.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221116"

import base64

import numpy as np
from bokeh.models.widgets import Button, FileInput, RadioButtonGroup, TextInput

from labctrl.widgets.figure import FactoryFigure
from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from labctrl.utilities import (ignore_connection_error,
                               eval_float,
                               eval_int)

from .abstract import AbstractBundleBoxcar
from .remote import RemoteBoxcarController
from .utils import calculate_dt


class BundleBokehBoxcar(AbstractBundleBoxcar):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat) -> None:
        super().__init__()

        self.config: dict = bundle_config["Config"]  # Axis Config
        self.name: str = self.config["Name"]
        self.lcfg = lcfg
        self.lstat = lstat
        update_config = lcfg.update_config
        config = self.config  # Alias for easier access
        name = self.name  # Alias for easier access

        lstat.stat[name] = dict() # register at lstat to keep track of working mode states, etc.

        self.remote = RemoteBoxcarController(config)

        # ======== Param Configs ========
        self.host = TextInput(title="Host", value=config["Host"])
        self.port = TextInput(title="Port", value=str(config["Port"]))
        self.working_unit = RadioButtonGroup(
            labels=config["WorkingUnits"],
            active=(config["WorkingUnits"].index(config["WorkingUnit"]))
        )
        self.delay_background_sampling = TextInput(
            title="Background Sampling Delay",
            value=str(config["DelayBackgroundSampling"]))
        self.delay_integrate = TextInput(
            title="Boxcar Integration Delay", value=str(config["DelayIntegrate"]))
        self.delay_hold = TextInput(
            title="Boxcar Hold Delay", value=str(config["DelayHold"]))
        self.delay_signal_sampling = TextInput(
            title="Signal Sampling Delay", value=str(config["DelaySignalSampling"]))
        self.delay_reset = TextInput(
            title="Boxcar Reset Delay", value=str(config["DelayReset"]))
        self.working_mode = RadioButtonGroup(labels=config["WorkingModes"], active=(
            config["WorkingModes"].index(config["WorkingMode"])))
        # ======== Interactive Elements ========
        self.test_online = Button(label="Test Boxcar Controller Online")
        self.submit_config = Button(
            label='Submit Config to Boxcar', button_type="warning")
        self.set_working_mode = Button(
            label='Set Boxcar Working Mode', button_type="warning")
        self.manual_get_boxcar_data = Button(
            label='Manually Get Boxcar Data')
        self.manual_get_PWA_data = Button(
            label='Manuall Get PWA Data')
        self.start_PWA = Button(
            label='Start Periodic Waveform Analyzer', button_type="success")
        self.stop_PWA = Button(
            label='Stop Periodic Waveform Analyzer', button_type="warning")
        # ======== Composites ========
        factory = FactoryFigure(lcfg, lstat)
        figure_bundle_config = dict()
        figure_bundle_config["BundleType"] = "Bokeh"
        figure_bundle_config["Config"] = config["BoxcarPreview"]
        self.boxcar_preview = factory.generate_bundle(figure_bundle_config)
        figure_bundle_config = dict()
        figure_bundle_config["BundleType"] = "Bokeh"
        figure_bundle_config["Config"] = config["PWAFigure"]
        self.PWA_figure = factory.generate_bundle(figure_bundle_config)

        # region host
        @update_config
        def __callback_host(attr, old, new):
            # no validation here because host can be literally anything,
            # it is just a param passed to remote API
            config["Host"] = self.host.value
            # regenerate remote when config updated
            self.remote = RemoteBoxcarController(config)

        self.host.on_change('value', __callback_host)
        # endregion host

        # region port
        @update_config
        def __callback_port(attr, old, new):
            # no validation here because port can be literally anything,
            # it is just a param passed to remote API
            config["Port"] = eval_int(self.port.value)
            # regenerate remote when config updated
            self.remote = RemoteBoxcarController(config)

        self.port.on_change('value', __callback_port)
        # endregion port

        # region working_unit
        @update_config
        def __callback_working_unit(attr, old, new):
            unit_index = int(self.working_unit.active)
            config["WorkingUnit"] = config["WorkingUnits"][unit_index]

        self.working_unit.on_change('active', __callback_working_unit)
        # endregion working_unit

        # region delay_background_sampling
        @update_config
        def __callback_delay_background_sampling(attr, old, new):
            delay = eval_float(self.delay_background_sampling.value)
            config["DelayBackgroundSampling"] = calculate_dt(
                delay, config["WorkingUnit"])

        self.delay_background_sampling.on_change(
            'value', __callback_delay_background_sampling)
        # endregion delay_background_sampling

        # region delay_integrate
        @update_config
        def __callback_delay_integrate(attr, old, new):
            delay = eval_float(self.delay_integrate.value)
            config["DelayIntegrate"] = calculate_dt(
                delay, config["WorkingUnit"])

        self.delay_integrate.on_change('value', __callback_delay_integrate)
        # endregion delay_integrate

        # region delay_hold
        @update_config
        def __callback_delay_hold(attr, old, new):
            delay = eval_float(self.delay_hold.value)
            config["DelayHold"] = calculate_dt(
                delay, config["WorkingUnit"])

        self.delay_hold.on_change('value', __callback_delay_hold)
        # endregion delay_hold

        # region delay_signal_sampling
        @update_config
        def __callback_delay_signal_sampling(attr, old, new):
            delay = eval_float(self.delay_signal_sampling.value)
            config["DelaySignalSampling"] = calculate_dt(
                delay, config["WorkingUnit"])

        self.delay_signal_sampling.on_change(
            'value', __callback_delay_signal_sampling)
        # endregion delay_signal_sampling

        # region delay_reset
        @update_config
        def __callback_delay_reset(attr, old, new):
            delay = eval_float(self.delay_reset.value)
            config["DelayReset"] = calculate_dt(
                delay, config["WorkingUnit"])

        self.delay_reset.on_change('value', __callback_delay_reset)
        # endregion delay_reset

        # region working_mode
        @update_config
        def __callback_working_mode(attr, old, new):
            mode_index = int(self.working_mode.active)
            config["WorkingMode"] = config["WorkingModes"][mode_index]

        self.working_mode.on_change('active', __callback_working_mode)
        # endregion working_mode

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
            response = self.remote.set_delay_background_sampling(
                config["DelayBackgroundSampling"])
            lstat.fmtmsg(response)
            response = self.remote.set_delay_integrate(
                config["DelayIntegrate"])
            lstat.fmtmsg(response)
            response = self.remote.set_delay_hold(config["DelayHold"])
            lstat.fmtmsg(response)
            response = self.remote.set_delay_signal_sampling(
                config["DelaySignalSampling"])
            lstat.fmtmsg(response)
            response = self.remote.set_delay_reset(config["DelayReset"])
            lstat.fmtmsg(response)

        self.submit_config.on_click(__callback_submit_config)
        # endregion submit_config

        # region set_working_mode
        @ignore_connection_error
        def __callback_set_working_mode():
            response = self.remote.set_working_mode(config["WorkingMode"])
            lstat.stat[name]["WorkingMode"] = config["WorkingMode"]
            lstat.fmtmsg(response)

        self.set_working_mode.on_click(__callback_set_working_mode)
        # endregion set_working_mode

        # region manual_get_boxcar_data
        @ignore_connection_error
        def __callback_manual_get_boxcar_data():
            # [TODO] replace this fixed constant to user adjustable widget
            PREVIEW_DATA_SIZE = 512
            preview_data = self.remote.get_new_data(PREVIEW_DATA_SIZE)
            x = np.arange(PREVIEW_DATA_SIZE)
            self.boxcar_preview.update(x=x, y=preview_data, lstat=lstat)

        self.manual_get_boxcar_data.on_click(__callback_manual_get_boxcar_data)
        # endregion manual_get_boxcar_data

        # region manual_get_PWA_data
        # [TODO] Implementation of PWA manual test
        # endregion manual_get_PWA_data

        # region start_PWA
        # [TODO] Implementation of PWA manual start
        # endregion start_PWA

        # region stop_PWA
        # [TODO] Implementation of PWA manual stop
        # endregion stop_PWA

    def get_boxcar_data(self, n_samples: int):
        return self.remote.get_new_data(n_samples=n_samples)

    def get_PWA_data(self, n_samples: int):
        # [TODO] Implementation of PWA
        pass
