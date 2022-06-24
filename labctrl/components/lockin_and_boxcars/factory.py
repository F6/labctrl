# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling generic boxcar controllers
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220624"


from functools import wraps
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput
from bokeh.layouts import column
from .remote import RemoteBoxcarController
from .utils import ignore_connection_error, eval_float


class BundleBoxcarController:
    """
    This class is responsible for holding references to the Bokeh UI Widgets
    of a single generic boxcar controller.
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.test_online = Button(label="Test Boxcar Online")
        self.delay_background_sampling = TextInput(title=init_str)
        self.delay_integrate = TextInput(title=init_str)
        self.delay_hold = TextInput(title=init_str)
        self.delay_signal_sampling = TextInput(title=init_str)
        self.delay_reset = TextInput(title=init_str)
        self.submit_config = Button(
            label='Submit Config to Boxcar', button_type='warning')

        self.working_mode = RadioButtonGroup(labels=[init_str, init_str])
        self.get_boxcar_data = None
        self.get_PWA_data = None

    def quick_control_group(self):
        widget_list = [
            self.test_online,
            self.delay_background_sampling,
            self.delay_integrate,
            self.delay_hold,
            self.delay_signal_sampling,
            self.delay_reset,
            self.submit_config,
            self.working_mode,
        ]
        return column(*widget_list)


class FactoryBoxcarController:
    def __init__(self) -> None:
        pass

    def generate_bundle(self, name, lcfg, lstat):
        update_config = lcfg.update_config # convenient alias for decorator
        bundle = BundleBoxcarController() # init new instance
        config = lcfg.config["lockin_and_boxcars"][name] # retrive previous config according to name
        remote = RemoteBoxcarController(config) # init api instance
        lstat.stat[name] = dict() # register component at labstat

        def __callback_test_online():
            try:
                lstat.fmtmsg(remote.online())
            except Exception as inst:
                print(type(inst), inst.args)
                lstat.expmsg(
                    "[Error] Nothing from remote, server is probably down.")

        bundle.test_online.on_click(__callback_test_online)

        @update_config
        def __callback_delay_background_sampling(attr, old, new):
            delay = eval_float(bundle.delay_background_sampling.value)
            config["DelayBackgroundSampling"] = delay

        delay_background_sampling = TextInput(
            title='Background Sampling Delay (us)', value=str(config["DelayBackgroundSampling"]))
        delay_background_sampling.on_change(
            'value', __callback_delay_background_sampling)
        bundle.delay_background_sampling = delay_background_sampling

        @update_config
        def __callback_delay_integrate(attr, old, new):
            delay = eval_float(bundle.delay_integrate.value)
            config["DelayIntegrate"] = delay

        delay_integrate = TextInput(
            title='Boxcar Integration Delay (us)', value=str(config["DelayIntegrate"]))
        delay_integrate.on_change('value', __callback_delay_integrate)
        bundle.delay_integrate = delay_integrate

        @update_config
        def __callback_delay_hold(attr, old, new):
            delay = eval_float(bundle.delay_hold.value)
            config["DelayHold"] = delay

        delay_hold = TextInput(
            title='Boxcar Hold Delay (us)', value=str(config["DelayHold"]))
        delay_hold.on_change('value', __callback_delay_hold)
        bundle.delay_hold = delay_hold

        @update_config
        def __callback_delay_signal_sampling(attr, old, new):
            delay = eval_float(bundle.delay_signal_sampling.value)
            config["DelaySignalSampling"] = delay

        delay_signal_sampling = TextInput(
            title='Signal Sampling Delay (us)', value=str(config["DelaySignalSampling"]))
        delay_signal_sampling.on_change(
            'value', __callback_delay_signal_sampling)
        bundle.delay_signal_sampling = delay_signal_sampling

        @update_config
        def __callback_delay_reset(attr, old, new):
            delay = eval_float(bundle.delay_reset.value)
            config["DelayReset"] = delay

        delay_reset = TextInput(
            title='Boxcar Reset Delay (us)', value=str(config["DelayReset"]))
        delay_reset.on_change('value', __callback_delay_reset)
        bundle.delay_reset = delay_reset

        @ignore_connection_error
        def __callback_submit_config():
            response = remote.set_delay_background_sampling(config["DelayBackgroundSampling"])
            lstat.fmtmsg(response)
            response = remote.set_delay_integrate(config["DelayIntegrate"])
            lstat.fmtmsg(response)
            response = remote.set_delay_hold(config["DelayHold"])
            lstat.fmtmsg(response)
            response = remote.set_delay_signal_sampling(config["DelaySignalSampling"])
            lstat.fmtmsg(response)
            response = remote.set_delay_reset(config["DelayReset"])
            lstat.fmtmsg(response)

        bundle.submit_config.on_click(__callback_submit_config)
        # sync once at spawn
        __callback_submit_config()

        @ignore_connection_error
        @update_config
        def __callback_working_mode(attr, old, new):
            mode = int(bundle.working_mode.active)
            config["Mode"] = config["WorkingModes"][mode]
            lstat.stat[name]["Mode"] = config["WorkingModes"][mode]
            response = remote.set_working_mode(config["Mode"])
            lstat.fmtmsg(response)

        working_mode = RadioButtonGroup(
            labels=config["WorkingModes"], active=(config["WorkingModes"].index(config["Mode"])))
        working_mode.on_change('active', __callback_working_mode)
        bundle.working_mode = working_mode
        # sync once at spawn
        lstat.stat[name]["Mode"] = config["Mode"]
        response = remote.set_working_mode(config["Mode"])
        lstat.fmtmsg(response)


        def __get_boxcar_data():
            result = remote.get_boxcar_data()
            return result

        bundle.get_boxcar_data = __get_boxcar_data

        def __get_PWA_data():
            result = remote.get_PWA_data()
            return result

        bundle.get_PWA_data = __get_PWA_data

        return bundle
