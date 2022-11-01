# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling the linear stage parameters
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211109"


from .utils import ignore_connection_error
from functools import wraps
from bokeh.models.widgets import RadioButtonGroup, Button, Div
from bokeh.layouts import column

from .remote import RemoteShutter
from .utils import ignore_connection_error


class BundleShutter:
    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.shutter_mode = RadioButtonGroup(labels=[init_str, init_str])
        self.take_background = None


class BundleShutterController:
    """
    This class is responsible for holding references to the Bokeh UI Widgets
    of a single shutter controller.

    Note that a single shutter controller can control multiple shutters at the
    same time, so some of the buttons are reused for different shutters. This also
    requires us to know how many shutters are controlled before constructing the
    bundle
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.test_online = Button(label="Test shutter controller online")
        self.select_shutter = RadioButtonGroup(labels=[init_str, init_str])
        self.manual_on = Button(label='Turn ON Shutter', button_type='warning')
        self.manual_off = Button(
            label='Turn OFF Shutter', button_type='warning')
        self.manual_switch = Button(
            label='Switch Shutter', button_type='warning')
        self.shutters = dict()

    def quick_control_group(self):
        widget_list = [
            Div(text="<h4>Shutter Controller</h4>"),
            self.test_online,
            Div(text="Select shutter to control"),
            self.select_shutter,
            self.manual_on,
            self.manual_off,
            self.manual_switch,
        ]
        for shutter in self.shutters:
            widget_list.append(Div(text="Shutter {}".format(shutter)),)
            widget_list.append(self.shutters[shutter].shutter_mode)
        return column(*widget_list)


class FactoryShutter:
    def __init__(self) -> None:
        pass

    def generate_bundle(self, shutter_name, config, remote, lcfg, lstat):

        scfg = config["Shutters"][shutter_name]
        controller_name = config["Name"]

        bundle = BundleShutter()

        update_config = lcfg.update_config

        @update_config
        def __callback_shutter_mode(attr, old, new):
            scfg["UseShutterBackground"] = [
                True, False][int(shutter_mode.active)]

        shutter_mode = RadioButtonGroup(
            labels=['Use shutter to take background', 'Do not use'], active=(0 if scfg["UseShutterBackground"] else 1))
        shutter_mode.on_change('active', __callback_shutter_mode)
        bundle.shutter_mode = shutter_mode

        def take_background(func):
            """if use shutter background, then the same thing is done twice with
            shutter open and closed. If do not use shutter background, then
            just leave the shutter status as is.
            """
            def iterate(meta=dict()):
                if controller_name not in lstat.stat:
                    lstat.stat[controller_name] = dict()
                if scfg["UseShutterBackground"]:
                    lstat.expmsg("Background is required, turning OFF shutter")
                    response = remote.shutter_off(shutter_name)
                    lstat.fmtmsg(response)
                    lstat.stat[controller_name][shutter_name] = "ShutterOff"
                    func(meta=meta)
                    lstat.expmsg("Background is taken, turning ON shutter")
                    response = remote.shutter_on(shutter_name)
                    lstat.fmtmsg(response)
                    lstat.stat[controller_name][shutter_name] = "ShutterOn"
                    func(meta=meta)
                else:
                    # this is wrong, because the shutter can be manually closed
                    #  and we did not varify that before this assertion.
                    # But this is fine because if the shutter is closed manually,
                    #  then it is intentional for optical component tweaking.
                    # The main task will always make sure that shutter is open
                    #  before the experiment begins.
                    lstat.stat[controller_name][shutter_name] = "ShutterManual"
                    func(meta=meta)

            return iterate

        bundle.take_background = take_background
        return bundle


class FactoryShutterController:
    def __init__(self) -> None:
        pass

    def generate_bundle(self, name, lcfg, lstat):
        """
        actually generates the bundle
            name: the name of the shutter controller
            lcfg:   the configure object to bind to
            lstat:  the stat object to bind to
        """

        config = lcfg.config["shutter_controllers"][name]
        update_config = lcfg.update_config
        bundle = BundleShutterController()
        remote = RemoteShutter(config)

        def __callback_test_online():
            try:
                lstat.fmtmsg(remote.online())
            except Exception as inst:
                print(type(inst), inst.args)
                lstat.expmsg(
                    "[Error] Nothing from remote, server is probably down.")

        bundle.test_online.on_click(__callback_test_online)

        shutter_list = list(config["Shutters"].keys())

        @update_config
        def __callback_select_shutter(attr, old, new):
            config["SelectedShutter"] = shutter_list[select_shutter.active]

        select_shutter = RadioButtonGroup(
            labels=shutter_list,
            active=shutter_list.index(config["SelectedShutter"])
        )
        select_shutter.on_change('active', __callback_select_shutter)
        bundle.select_shutter = select_shutter

        @ignore_connection_error
        def __callback_manual_on():
            lstat.fmtmsg(remote.shutter_on(config["SelectedShutter"]))

        bundle.manual_on.on_click(__callback_manual_on)

        @ignore_connection_error
        def __callback_manual_off():
            lstat.fmtmsg(remote.shutter_off(config["SelectedShutter"]))

        bundle.manual_off.on_click(__callback_manual_off)

        @ignore_connection_error
        def __callback_manual_switch():
            lstat.fmtmsg(remote.switch_shutter(config["SelectedShutter"]))

        bundle.manual_switch.on_click(__callback_manual_switch)

        factory = FactoryShutter()
        for shutter in shutter_list:
            bundle.shutters[shutter] = factory.generate_bundle(
                shutter, config, remote, lcfg, lstat)

        return bundle
