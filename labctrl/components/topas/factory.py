# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling the topas parameters
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

import base64
from functools import wraps
from datetime import datetime
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput, Div
from bokeh.layouts import column, row

from .remote import ProxiedTOPAS
from .utils import ignore_connection_error, eval_float


class BundleTOPAS:
    """
    This class is responsible for holding references to the Bokeh UI Widgets
    of a single linear stage.
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.test_online = Button(label="Test TOPAS online")
        self.unit_selection = RadioButtonGroup(labels=[init_str, init_str])
        self.manual_target = TextInput(
            title='Manually set output wavelength to', value="")
        self.manual_move = Button(label='Set TOPAS Wavelength', button_type='warning')
        self.manual_step = TextInput(
            title='Manually step output wavelength', value="")
        self.manual_step_forward = Button(
            label="Step forward", button_type='warning')
        self.manual_step_backward = Button(
            label="Step backward", button_type='warning')
        self.scan_mode = RadioButtonGroup(labels=[init_str, init_str])
        self.scan_start = TextInput(title=init_str)
        self.scan_stop = TextInput(title=init_str)
        self.scan_step = TextInput(title=init_str)
        self.scan_file = FileInput(accept=".txt")
        self.scan_topas = None

    def quick_control_group(self):
        return column(
            self.test_online,
            self.manual_target,
            self.manual_move,
            self.manual_step,
            self.manual_step_forward,
            self.manual_step_backward,
            Div(text="<h4>Scan Mode:</h4>"),
            self.scan_mode,
            self.scan_start,
            self.scan_stop,
            self.scan_step,
            self.scan_file,
        )


class FactoryTOPAS:
    """
    This class is responsible for generating BundleTOPAS objects from given params
    """

    def __init__(self) -> None:
        pass

    def generate_bundle(self, config, lcfg, lstat):
        """
        actually generates the bundle
            config: the config for the TOPAS
            lcfg:   the global configure object to bind to
            lstat:  the stat object to bind to
        """

        remote = ProxiedTOPAS(config)

        update_config = lcfg.update_config

        name = config["Name"]
        unit = config["Unit"]

        def set_wavelength(target):
            if unit == "nm":
                response = remote.set_wavelength_nm(target)
            elif unit == "cm-1":
                response = remote.set_wavelength_wn(target)
            else:
                response = {"success": False, "message": "Unknown unit!"}
            return response

        bundle = BundleTOPAS()

        def __callback_test_online():
            try:
                lstat.fmtmsg(remote.online())
            except Exception as inst:
                print(type(inst), inst.args)
                lstat.expmsg(
                    "[Error] Nothing from remote, server is probably down.")

        bundle.test_online.on_click(__callback_test_online)

        @update_config
        def __callback_unit_selection(attr, old, new):
            unit = int(bundle.unit_selection.active)
            config["Unit"] = config["Units"][unit]

        bundle.unit_selection = RadioButtonGroup(
            labels=config["Units"], active=(config["Units"].index(config["Unit"])))
        bundle.unit_selection.on_change('active', __callback_unit_selection)

        @update_config
        def __callback_manual_target(attr, old, new):
            target = eval_float(bundle.manual_target.value)
            config["ManualTarget"] = target

        bundle.manual_target.on_change('value', __callback_manual_target)

        @ignore_connection_error
        @update_config
        def __callback_manual_move():
            """before actual movement, make sure it's sync with what is at the front panel"""
            target = eval_float(bundle.manual_target.value)
            config["ManualTarget"] = target
            response = set_wavelength(config["ManualTarget"])
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
            config["ManualTarget"] += config["ManualStep"]
            response = set_wavelength(config["ManualTarget"])
            lstat.fmtmsg(response)

        bundle.manual_step_forward.on_click(__callback_manual_step_forward)

        @ignore_connection_error
        @update_config
        def __callback_manual_step_backward():
            config["ManualTarget"] -= config["ManualStep"]
            response = set_wavelength(config["ManualTarget"])
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
        def __callback_scan_start(attr, old, new):
            config["Start"] = eval_float(scan_start.value)

        scan_start = TextInput(
            title='Scan range: Start', value=str(config["Start"]))
        scan_start.on_change('value', __callback_scan_start)
        bundle.scan_start = scan_start

        @update_config
        def __callback_scan_stop(attr, old, new):
            config["Stop"] = eval_float(scan_stop.value)

        scan_stop = TextInput(
            title='Scan range: Stop', value=str(config["Stop"]))
        scan_stop.on_change('value', __callback_scan_stop)
        bundle.scan_stop = scan_stop

        @update_config
        def __callback_scan_step(attr, old, new):
            config["Step"] = float(scan_step.value)

        scan_step = TextInput(
            title='Scan range: Step', value=str(config["Step"]))
        scan_step.on_change('value', __callback_scan_step)
        bundle.scan_step = scan_step

        @update_config
        def __callback_scan_file(attr, old, new):
            lstat.expmsg("Scan list inputed")
            fcontent = base64.b64decode(bundle.scan_file.value).decode()
            # print(fcontent)
            config["Mode"] = "ExternalFile"
            bundle.scan_mode.active = config["ScanModes"].index(
                config["Mode"])
            config["ExternalList"] = list(
                map(float, fcontent.split()))

        bundle.scan_file.on_change('value', __callback_scan_file)

        def scan_topas(func, meta=''):
            """decorator, when applied to fun, scan topas wavelength for func"""
            def iterate(meta=dict()):
                if config["Mode"] == "Range" or config["Mode"] == "ExternalFile":
                    for i, target in enumerate(lstat.stat[name]["ScanList"]):
                        if meta["TERMINATE"]:
                            lstat.expmsg(
                                "scan_topas received signal TERMINATE, trying graceful Thread exit")
                            break
                        lstat.expmsg("Setting wavelength to {target} {unit}".format(target=target, unit=config["Unit"]))
                        response = set_wavelength(target)
                        lstat.fmtmsg(response)
                        lstat.stat[name]["Wavelength"] = target
                        lstat.stat[name]["iWavelength"] = i
                        func(meta=meta)
                else:
                    lstat.expmsg(
                        "Topas wavelength is set manually, so no action has been taken")
                    lstat.stat[name]["Wavelength"] = "ManualWavelength"
                    lstat.stat[name]["iWavelength"] = 0
                    func(meta=meta)
            return iterate

        bundle.scan_topas = scan_topas

        return bundle
