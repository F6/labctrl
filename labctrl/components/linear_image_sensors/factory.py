# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling linear image sensors
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220525"



from functools import wraps
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput
from bokeh.layouts import column
from .remote import RemoteLinearImageSensor
from .utils import ignore_connection_error

class BundleLinearImageSensor:
    """
    This class is responsible for holding references to the Bokeh UI Widgets
    of a single linear image sensor.
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.test_online = Button(label="Test sensor online")
        # self.select_mode = RadioButtonGroup(labels=[init_str, init_str])
        # self.sample_size = TextInput(title=init_str)
        self.manual_take_sample = Button(label='Take Sample', button_type='warning')
        self.get_image = None


    def quick_control_group(self):
        widget_list = [
            self.test_online,
            # self.select_mode,
            # self.sample_size,
            self.manual_take_sample,
        ]
        return column(*widget_list)


class FactoryLinearImageSensor:
    def __init__(self) -> None:
        pass

    def generate_bundle(self, name, lcfg, lstat):
        bundle = BundleLinearImageSensor()

        config = lcfg.config["linear_image_sensors"][name]
        remote = RemoteLinearImageSensor(config)

        def __callback_test_online():
            try:
                lstat.fmtmsg(remote.online())
            except Exception as inst:
                print(type(inst), inst.args)
                lstat.expmsg(
                    "[Error] Nothing from remote, server is probably down.")

        bundle.test_online.on_click(__callback_test_online)

        @ignore_connection_error
        def __callback_manual_take_sample():
            lstat.fmtmsg(remote.get_image())
        
        bundle.manual_take_sample.on_click(__callback_manual_take_sample)

        def __get_image():
            result = remote.get_image()
            return result

        bundle.get_image = __get_image

        return bundle