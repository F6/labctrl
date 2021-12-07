# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling the ziUHF lock-in amplifier
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"



from functools import wraps
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput
from bokeh.layouts import column
from .remote import ProxiedUHF
from .utils import ignore_connection_error

class BundleZiUHF:
    """
    This class is responsible for holding references to the Bokeh UI Widgets
    of a single ziUHF lock-in amplifier.
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.test_online = Button(label="Test ziUHF online")
        # self.select_mode = RadioButtonGroup(labels=[init_str, init_str])
        # self.sample_size = TextInput(title=init_str)
        self.manual_take_sample = Button(label='Take Sample', button_type='warning')
        self.get_value = None


    def quick_control_group(self):
        widget_list = [
            self.test_online,
            # self.select_mode,
            # self.sample_size,
            self.manual_take_sample,
        ]
        return column(*widget_list)


class FactoryZiUHF:
    def __init__(self) -> None:
        pass

    def generate_bundle(self, lcfg, lstat):
        bundle = BundleZiUHF()

        config = lcfg.config["lockin_and_boxcars"]["ziUHF"]
        remote = ProxiedUHF(config)

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
            lstat.fmtmsg(remote.get_value())
        
        bundle.manual_take_sample.on_click(__callback_manual_take_sample)

        def __get_value():
            value = remote.get_value()
            value = value["value"]
            return float(value)

        bundle.get_value = __get_value

        return bundle