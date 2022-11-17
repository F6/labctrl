# -*- coding: utf-8 -*-

"""bundle_bokeh.py:
This module provides the Bundle class for Bokeh UI widgets for 
testing and controlling 2D image sensors
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221117"

from bokeh.models.widgets import TextInput, Button, RadioButtonGroup
from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from labctrl.widgets.figure import FactoryFigure
from .abstract import AbstractBundleCamera
from .remote import RemoteCamera
from .utils import ignore_connection_error, eval_float, eval_int, calculate_dt


class BundleBokehCamera(AbstractBundleCamera):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat) -> None:
        super().__init__()
        self.lcfg = lcfg
        self.lstat = lstat
        self.config = bundle_config["Config"]
        self.name = self.config["Name"]
        self.remote = RemoteCamera(self.config)

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
        self.exposure_time_unit = RadioButtonGroup(
            labels=config["ExposureTimeUnits"],
            active=(config["ExposureTimeUnits"].index(
                config["ExposureTimeUnit"]))
        )
        self.exposure_time = TextInput(
            title="Exposure Time", value=str(config["ExposureTime"]))
        self.change_exposure_time = Button(label="Change Exposure Time")
        self.test_online = Button(label="Test Camera Online")
        self.apply_all_settings = Button(
            label="Apply All Settings to Remote", button_type='success')
        self.manual_take_sample = Button(
            label="Manually Take Image", button_type='warning')
        self.start_continuous_video_streaming = Button(
            label="Start Continuous Video Streaming", button_type='success')
        self.stop_continuous_video_streaming = Button(
            label="Stop Continuous Video Streaming", button_type='warning')

        factory = FactoryFigure(lcfg, lstat)
        figure_bundle_config = dict()
        figure_bundle_config["Config"] = config["PreviewFigure"]
        self.preview_figure = factory.generate_bundle(figure_bundle_config)

        # region host
        @update_config
        def __callback_host(attr, old, new):
            # no validation here because host can be literally anything,
            # it is just a param passed to remote API
            config["Host"] = self.host.value
            # regenerate remote when config updated
            self.remote = RemoteCamera(config)

        self.host.on_change('value', __callback_host)
        # endregion host

        # region port
        @update_config
        def __callback_port(attr, old, new):
            # no validation here because port can be literally anything,
            # it is just a param passed to remote API
            config["Port"] = eval_int(self.port.value)
            # regenerate remote when config updated
            self.remote = RemoteCamera(config)

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

        # region exposure_time_unit
        @update_config
        def __callback_exposure_time_unit(attr, old, new):
            unit_index = int(self.exposure_time_unit.active)
            config["ExposureTimeUnit"] = config["ExposureTimeUnits"][unit_index]

        self.exposure_time_unit.on_change(
            'active', __callback_exposure_time_unit)
        # endregion exposure_time_unit

        # region exposure_time
        @update_config
        def __callback_exposure_time(attr, old, new):
            config["ExposureTime"] = eval_float(self.exposure_time.value)

        self.exposure_time.on_change('value', __callback_exposure_time)
        # endregion exposure_time

        # region change_exposure_time
        @ignore_connection_error
        @update_config
        def __callback_change_exposure_time():
            """before actual change, make sure it's sync with what is at the front panel"""
            config["ExposureTime"] = eval_float(self.exposure_time.value)
            target_in_us = calculate_dt(
                config["ExposureTime"], config["ExposureTimeUnit"])
            response = self.remote.set_exposure_time(target_in_us)
            self.lstat.fmtmsg(response)

        self.change_exposure_time.on_click(__callback_change_exposure_time)
        # endregion change_exposure_time

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

        # region apply_all_settings
        @ignore_connection_error
        @update_config
        def __callback_apply_all_settings():
            # just an alias for all setting-changing callbacks
            __callback_change_working_mode()
            __callback_change_exposure_time()

        self.apply_all_settings.on_click(__callback_apply_all_settings)
        # endregion apply_all_settings

        # region manual_take_sample
        @ignore_connection_error
        def __callback_manual_take_sample():
            new_image = self.remote.get_image()
            xmin = 0
            ymin = 0
            xmax = new_image.shape[1]
            ymax = new_image.shape[0]
            self.preview_figure.update(
                new_image, xmin, xmax, ymin, ymax, lstat)

        self.manual_take_sample.on_click(__callback_manual_take_sample)
        # endregion manual_take_sample

        # region start_continuous_video_streaming
        # TODO: implement callback
        # endregion start_continuous_video_streaming

        # region stop_continuous_video_streaming
        # TODO: implement callback
        # endregion stop_continuous_video_streaming

    def get_image(self):
        return self.remote.get_image()
