# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling the linear stage parameters
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211109"

import base64
from functools import wraps
from datetime import datetime
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput, Div
from bokeh.layouts import column, row

from .remote import RemoteLinearStage
from .utils import ps_to_mm, eval_float, ignore_connection_error


class BundleLinearStage:
    """
    This class is responsible for holding references to the Bokeh UI Widgets
    of a single linear stage.
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.test_online = Button(label="Test linear stage online")
        self.manual_position = TextInput(
            title='Manually set delay to (ps)', value="")
        self.manual_move = Button(label='Move stage', button_type='warning')
        self.manual_step = TextInput(
            title='Manually step delay (ps)', value="")
        self.manual_step_forward = Button(
            label="Step forward", button_type='warning')
        self.manual_step_backward = Button(
            label="Step backward", button_type='warning')
        self.scan_mode = RadioButtonGroup(labels=[init_str, init_str])
        self.scan_zero = TextInput(title=init_str)
        self.scan_start = TextInput(title=init_str)
        self.scan_stop = TextInput(title=init_str)
        self.scan_step = TextInput(title=init_str)
        self.scan_file = FileInput(accept=".txt")
        self.scan_delay = None

    def quick_control_group(self):
        return column(
            self.test_online,
            self.manual_position,
            self.manual_move,
            self.manual_step,
            self.manual_step_forward,
            self.manual_step_backward,
            Div(text="<h4>Scan Mode:</h4>"),
            self.scan_mode,
            self.scan_zero,
            self.scan_start,
            self.scan_stop,
            self.scan_step,
            self.scan_file,
        )


class FactoryLinearStage:
    """
    This class is responsible for generating BundleLinearStage objects from given params
    """

    def __init__(self) -> None:
        pass

    def generate_bundle(self, config, lcfg, lstat):
        """
        actually generates the bundle
            config: the config for the linear stage
            lcfg:   the global configure object to bind to
            lstat:  the stat object to bind to
        """

        remote = RemoteLinearStage(config)

        update_config = lcfg.update_config

        name = config["Name"]

        bundle = BundleLinearStage()

        def __callback_test_online():
            try:
                lstat.fmtmsg(remote.online())
            except Exception as inst:
                print(type(inst), inst.args)
                lstat.expmsg(
                    "[Error] Nothing from remote, server is probably down.")

        bundle.test_online.on_click(__callback_test_online)

        @update_config
        def __callback_manual_position(attr, old, new):
            delay = eval_float(bundle.manual_position.value)
            config["ManualPos"] = config["ZeroAbsPos"] + ps_to_mm(delay)

        bundle.manual_position.on_change('value', __callback_manual_position)

        @ignore_connection_error
        @update_config
        def __callback_manual_move():
            """before actual movement, make sure it's sync with what is at the front panel"""
            delay = eval_float(bundle.manual_position.value)
            config["ManualPos"] = config["ZeroAbsPos"] + ps_to_mm(delay)
            response = remote.moveabs(config["ManualPos"])
            lstat.fmtmsg(response)

        bundle.manual_move.on_click(__callback_manual_move)

        @update_config
        def __callback_manual_step(attr, old, new):
            step = eval_float(bundle.manual_step.value)
            config["ManualStep"] = step

        bundle.manual_step.on_change('value', __callback_manual_step)

        @ignore_connection_error
        @update_config
        def __callback_manual_step_forward():
            config["ManualPos"] += ps_to_mm(config["ManualStep"])
            response = remote.moveabs(config["ManualPos"])
            lstat.fmtmsg(response)

        bundle.manual_step_forward.on_click(__callback_manual_step_forward)

        @ignore_connection_error
        @update_config
        def __callback_manual_step_backward():
            config["ManualPos"] -= ps_to_mm(config["ManualStep"])
            response = remote.moveabs(config["ManualPos"])
            lstat.fmtmsg(response)

        bundle.manual_step_backward.on_click(__callback_manual_step_backward)

        @update_config
        def __callback_scan_mode(attr, old, new):
            mode = int(bundle.scan_mode.active)
            config["Mode"] = config["ScanModes"][mode]
            if mode == 0:
                bundle.scan_start.visible = False
                bundle.scan_step.visible = False
                bundle.scan_stop.visible = False
                bundle.scan_file.visible = False
            elif mode == 1:
                bundle.scan_start.visible = True
                bundle.scan_step.visible = True
                bundle.scan_stop.visible = True
                bundle.scan_file.visible = False
            elif mode == 2:
                bundle.scan_start.visible = False
                bundle.scan_step.visible = False
                bundle.scan_stop.visible = False
                bundle.scan_file.visible = True

        scan_mode = RadioButtonGroup(
            labels=config["ScanModes"], active=(config["ScanModes"].index(config["Mode"])))
        scan_mode.on_change('active', __callback_scan_mode)
        bundle.scan_mode = scan_mode

        @update_config
        def __callback_scan_zero(attr, old, new):
            config["ZeroAbsPos"] = eval_float(bundle.scan_zero.value)

        scan_zero = TextInput(
            title='Zero delay position (mm)', value=str(config["ZeroAbsPos"]))
        scan_zero.on_change('value', __callback_scan_zero)
        bundle.scan_zero = scan_zero

        @update_config
        def __callback_scan_start(attr, old, new):
            config["Start"] = eval_float(scan_start.value)

        scan_start = TextInput(
            title='Scan range: Start (ps)', value=str(config["Start"]))
        scan_start.on_change('value', __callback_scan_start)
        bundle.scan_start = scan_start

        @update_config
        def __callback_scan_stop(attr, old, new):
            config["Stop"] = eval_float(scan_stop.value)

        scan_stop = TextInput(
            title='Scan range: Stop (ps)', value=str(config["Stop"]))
        scan_stop.on_change('value', __callback_scan_stop)
        bundle.scan_stop = scan_stop

        @update_config
        def __callback_scan_step(attr, old, new):
            config["Step"] = float(scan_step.value)

        scan_step = TextInput(
            title='Scan range: Step (ps)', value=str(config["Step"]))
        scan_step.on_change('value', __callback_scan_step)
        bundle.scan_step = scan_step

        @update_config
        def __callback_scan_file(attr, old, new):
            lstat.expmsg("Delay list inputed")
            fcontent = base64.b64decode(bundle.scan_file.value).decode()
            # print(fcontent)
            config["Mode"] = "ExternalFile"
            bundle.scan_mode.active = config["ScanModes"].index(
                config["Mode"])
            config["ExternalList"] = list(
                map(float, fcontent.split()))

        bundle.scan_file.on_change('value', __callback_scan_file)

        def scan_delay(func, meta=''):
            """decorator, when applied to fun, scan delays for func"""
            def iterate(meta=dict()):
                if config["Mode"] == "Range" or config["Mode"] == "ExternalFile":
                    for i, dl in enumerate(lstat.stat[name]["ScanList"]):
                        if meta["TERMINATE"]:
                            lstat.expmsg(
                                "scan_delay received signal TERMINATE, trying graceful Thread exit")
                            break
                        lstat.expmsg("Setting delay to {dl} ps".format(dl=dl))
                        target_abs_pos = config["ZeroAbsPos"] + ps_to_mm(dl)
                        response = remote.moveabs(target_abs_pos)
                        lstat.fmtmsg(response)
                        lstat.stat[name]["Delay"] = dl
                        lstat.stat[name]["iDelay"] = i
                        func(meta=meta)
                else:
                    lstat.expmsg(
                        "Delay is set manually, so no action has been taken")
                    lstat.stat[name]["Delay"] = "ManualDelay"
                    lstat.stat[name]["iDelay"] = 0
                    func(meta=meta)
            return iterate

        bundle.scan_delay = scan_delay
        return bundle
