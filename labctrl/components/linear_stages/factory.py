# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling the linear stage parameters

Breaking change: 
    ver 20221106: 
        * change factory init params, moved lcfg and lstat to factory init instead of bundle gen
        * change bundle gen params to require dict format
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221106"

import base64
import numpy as np
from functools import wraps
from datetime import datetime
from bokeh.models.widgets import RadioButtonGroup, Button, TextInput, FileInput, Div
from bokeh.layouts import column, row

from .remote import RemoteLinearStage
from .utils import eval_float, ignore_connection_error, eval_int, dt_to_mm


class BundleBokehLinearStage:
    """
    This class is responsible for holding references to the Bokeh UI Widgets
    and basic functions
    of a single linear stage.
    """

    def __init__(self) -> None:
        """
        One to one maps to config, and other utils needed for application
        """
        init_str = 'Initialize at {}'.format(self)
        # ======== Configuration Inputs and Placeholders ========
        #  Placeholders are replaced by real widgets when generating bundle,
        #   they are here just for the intelisense and human to know what a bundle has.
        #  Placeholders are generated with init_str as parameter. At application level
        #   no init_str should be visible. If witnessed, check the generation process
        #  - Why not just generate the widgets here and reuse it when generating bundle?
        #  - Because the bundle is generated at run-time according to config, we have
        #    no idea what to fill in the widgets by now
        #  - Then why use new instance to replace placeholder, rather than just change
        #    the content of the the placeholder?
        #  - I'd like to but bokeh won't allow me to...
        self.host = TextInput(title="Host", value="")
        self.port = TextInput(title="Port", value="")
        self.working_unit = RadioButtonGroup(labels=[init_str, init_str])
        self.scan_mode = RadioButtonGroup(labels=[init_str, init_str])
        self.range_scan_start = TextInput(title="Range Scan Start", value="")
        self.range_scan_stop = TextInput(title="Range Scan Stop", value="")
        self.range_scan_step = TextInput(title="Range Scan Step", value="")
        self.external_scan_list_file = FileInput(accept=".txt")
        self.position_unit = RadioButtonGroup(labels=[init_str, init_str])
        self.zero_delay_absolute_position = TextInput(
            title="Zero Delay Absolute Position", value="")
        self.manual_unit = RadioButtonGroup(labels=[init_str, init_str])
        self.manual_position = TextInput(
            title="Manually set delay to", value="")
        self.manual_step = TextInput(title="Manually step delay", value="")
        self.multiples = TextInput(title="Multiples", value="")
        self.soft_limit_min = TextInput(title="Soft Limit Min", value="")
        self.soft_limit_max = TextInput(title="Soft Limit Max", value="")
        self.working_direction = RadioButtonGroup(labels=[init_str, init_str])
        self.driving_speed_unit = RadioButtonGroup(labels=[init_str, init_str])
        self.driving_speed = TextInput(title="Driving Speed", value="")
        self.driving_acceleration_unit = RadioButtonGroup(
            labels=[init_str, init_str])
        self.driving_acceleration = TextInput(
            title="Driving Acceleration", value="")
        # ======== Interactive Elements ========
        self.test_online = Button(label="Test Linear Stage Online")
        self.manual_move = Button(label='Move Stage', button_type='warning')
        self.manual_step_forward = Button(
            label="Step forward", button_type='warning')
        self.manual_step_backward = Button(
            label="Step backward", button_type='warning')
        # ======== Other Stuff to attach ========
        self.scan_delay = None
        self.set_delay = None
        self.remote = None


class FactoryLinearStage:
    """
    This class is responsible for generating BundleLinearStage objects 
    from given params
    """

    def __init__(self, lcfg, lstat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat
        self.generated = []

    def update_scanlist(self, config) -> list:
        """
        After linear stage scan settings are changed or loaded, scanlists need to be 
        automatically regenerated in labstat.
        """
        name = config["Name"]

        if name not in self.lstat.stat:
            self.lstat.stat[name] = dict()

        if config["ScanMode"] == 'ExternalFile':
            # if the flag is set to Ext, then the ext list is set by external program so just copy it
            self.lstat.stat[name]["ScanList"] = config["LoadedExternalScanList"]
        elif config["ScanMode"] == 'Range':
            # if the flag is set to True, then we need to construct scan lists by given parameter
            self.lstat.stat[name]["ScanList"] = np.arange(
                config["RangeScanStart"], config["RangeScanStop"], config["RangeScanStep"]).tolist()
        else:
            # this sets the len of the list to 1 for our convenience when dealing with for loops,
            #  while preventing accidentally set wavelengths or delays if we have a bug elsewhere
            self.lstat.stat[name]["ScanList"] = [None]

        self.lstat.expmsg("Generated Scan List: {}".format(
            self.lstat.stat[name]["ScanList"]))
        self.lstat.dump_stat("last_stat.json")
        return self.lstat.stat[name]["ScanList"]

    def generate_bundle(self, bundle_config: dict):
        """
        actually generates the bundle
            bundle_config:  dict that contains all information needed to generate
                             the bundle
                            required fields: 
                                "Config" : config dict of linear stage

        for now only bokeh bundle is used, so direct generation, 
        if more are required, then the fork goes here
        """
        # sanity check
        name = bundle_config["Config"]["Name"]
        if name in self.generated:
            print(
                "FactoryLinearStage: SANITY: Linear Stage with name {} \
                    already generated before!".format(name))
        self.generated.append(name)
        return self.generate_bundle_bokeh(bundle_config)

    def generate_bundle_bokeh(self, bundle_config):
        """
        Implementation of all bokeh element callbacks, callback bindings,
         and other utils in bundle
        """
        update_config = self.lcfg.update_config
        config = bundle_config["Config"]
        name = config["Name"]
        bundle = BundleBokehLinearStage()
        bundle.remote = RemoteLinearStage(config)

        self.update_scanlist(config)

        # region host
        @update_config
        def __callback_host(attr, old, new):
            # no validation here because host can be literally anything,
            # it is just a param passed to remote API
            config["Host"] = bundle.host.value
            # regenerate remote when config updated
            bundle.remote = RemoteLinearStage(config)

        bundle.host.value = config["Host"]
        bundle.host.on_change('value', __callback_host)
        # endregion host

        # region port
        @update_config
        def __callback_port(attr, old, new):
            # no validation here because port can be literally anything,
            # it is just a param passed to remote API
            config["Port"] = eval_int(bundle.port.value)
            # regenerate remote when config updated
            bundle.remote = RemoteLinearStage(config)

        bundle.port.value = str(config["Port"])
        bundle.port.on_change('value', __callback_port)
        # endregion port

        # region working_unit
        @update_config
        def __callback_working_unit(attr, old, new):
            unit_index = int(bundle.working_unit.active)
            config["WorkingUnit"] = config["WorkingUnits"][unit_index]

        working_unit = RadioButtonGroup(
            labels=config["WorkingUnits"],
            active=(config["WorkingUnits"].index(config["WorkingUnit"]))
        )
        working_unit.on_change('active', __callback_working_unit)
        bundle.working_unit = working_unit
        # endregion working_unit

        # region scan_mode
        @update_config
        def __callback_scan_mode(attr, old, new):
            mode_index = int(bundle.scan_mode.active)
            config["ScanMode"] = config["ScanModes"][mode_index]
            if mode_index == 0:
                bundle.range_scan_start.visible = False
                bundle.range_scan_step.visible = False
                bundle.range_scan_stop.visible = False
                bundle.external_scan_list_file.visible = False
            elif mode_index == 1:
                bundle.range_scan_start.visible = True
                bundle.range_scan_step.visible = True
                bundle.range_scan_stop.visible = True
                bundle.external_scan_list_file.visible = False
            elif mode_index == 2:
                bundle.range_scan_start.visible = False
                bundle.range_scan_step.visible = False
                bundle.range_scan_stop.visible = False
                bundle.external_scan_list_file.visible = True
            self.update_scanlist(config)

        scan_mode = RadioButtonGroup(
            labels=config["ScanModes"], active=(config["ScanModes"].index(config["ScanMode"])))
        scan_mode.on_change('active', __callback_scan_mode)
        bundle.scan_mode = scan_mode
        # endregion scan_mode

        # region range_scan_start
        @update_config
        def __callback_range_scan_start(attr, old, new):
            config["RangeScanStart"] = eval_float(
                bundle.range_scan_start.value)
            self.update_scanlist(config)

        bundle.range_scan_start.value = str(config["RangeScanStart"])
        bundle.range_scan_start.on_change('value', __callback_range_scan_start)
        # endregion range_scan_start

        # region range_scan_stop
        @update_config
        def __callback_range_scan_stop(attr, old, new):
            config["RangeScanStop"] = eval_float(bundle.range_scan_stop.value)
            self.update_scanlist(config)

        bundle.range_scan_stop.value = str(config["RangeScanStop"])
        bundle.range_scan_stop.on_change('value', __callback_range_scan_stop)
        # endregion range_scan_stop

        # region range_scan_step
        @update_config
        def __callback_range_scan_step(attr, old, new):
            config["RangeScanStep"] = eval_float(bundle.range_scan_step.value)
            self.update_scanlist(config)

        bundle.range_scan_step.value = str(config["RangeScanStep"])
        bundle.range_scan_step.on_change('value', __callback_range_scan_step)
        # endregion range_scan_stop

        # region external_scan_list_file
        @update_config
        def __callback_external_scan_list_file(attr, old, new):
            self.lstat.expmsg("Loaded External Delay List")
            fcontent = base64.b64decode(
                bundle.external_scan_list_file.value).decode()
            # print(fcontent)
            config["Mode"] = "ExternalFile"
            bundle.scan_mode.active = config["ScanModes"].index(config["Mode"])
            config["LoadedExternalScanList"] = list(
                map(float, fcontent.split()))
            self.update_scanlist(config)

        bundle.external_scan_list_file.on_change(
            'value', __callback_external_scan_list_file)
        # endregion external_scan_list_file

        # region position_unit
        @update_config
        def __callback_position_unit(attr, old, new):
            unit_index = int(bundle.position_unit.active)
            config["PositionUnit"] = config["PositionUnits"][unit_index]

        position_unit = RadioButtonGroup(
            labels=config["PositionUnits"],
            active=(config["PositionUnits"].index(config["PositionUnit"]))
        )
        position_unit.on_change('active', __callback_position_unit)
        # Disabled because no actual implementation is available
        position_unit.disabled = True
        bundle.position_unit = position_unit
        # endregion position_unit

        # region zero_delay_absolute_position
        @update_config
        def __callback_zero_delay_absolute_position(attr, old, new):
            config["ZeroDelayAbsolutePosition"] = eval_float(
                bundle.zero_delay_absolute_position.value)

        bundle.zero_delay_absolute_position.value = str(
            config["ZeroDelayAbsolutePosition"])
        bundle.zero_delay_absolute_position.on_change(
            'value', __callback_zero_delay_absolute_position)
        # endregion zero_delay_absolute_position

        # region manual_unit
        @update_config
        def __callback_manual_unit(attr, old, new):
            unit_index = int(bundle.manual_unit.active)
            config["ManualUnit"] = config["ManualUnits"][unit_index]

        manual_unit = RadioButtonGroup(
            labels=config["ManualUnits"],
            active=(config["ManualUnits"].index(config["WorkingUnit"]))
        )
        manual_unit.on_change('active', __callback_manual_unit)
        bundle.manual_unit = manual_unit
        # endregion manual_unit

        # region manual_position
        @update_config
        def __callback_manual_position(attr, old, new):
            delay = eval_float(bundle.manual_position.value)
            config["ManualPosition"] = config["ZeroDelayAbsolutePosition"] + \
                dt_to_mm(
                    delay, config["ManualUnit"], config["Multiples"], config["WorkingDirection"])

        bundle.manual_position.value = str(config["ManualPosition"])
        bundle.manual_position.on_change('value', __callback_manual_position)
        # endregion manual_position

        # region manual_step
        @update_config
        def __callback_manual_step(attr, old, new):
            step = eval_float(bundle.manual_step.value)
            config["ManualStep"] = step

        bundle.manual_step.value = str(config["ManualStep"])
        bundle.manual_step.on_change('value', __callback_manual_step)
        # endregion manual_step

        # region multiples
        @update_config
        def __callback_multiples(attr, old, new):
            multiples = eval_float(bundle.multiples.value)
            config["Multiples"] = multiples

        bundle.multiples.value = str(config["Multiples"])
        bundle.multiples.on_change('value', __callback_multiples)
        # endregion multiples

        # region soft_limit_min
        @update_config
        def __callback_soft_limit_min(attr, old, new):
            soft_limit_min = eval_float(bundle.soft_limit_min.value)
            config["SoftLimitMin"] = soft_limit_min

        bundle.soft_limit_min.value = str(config["SoftLimitMin"])
        bundle.soft_limit_min.on_change('value', __callback_soft_limit_min)
        # endregion soft_limit_min

        # region soft_limit_max
        @update_config
        def __callback_soft_limit_max(attr, old, new):
            soft_limit_max = eval_float(bundle.soft_limit_max.value)
            config["SoftLimitMax"] = soft_limit_max

        bundle.soft_limit_max.value = str(config["SoftLimitMax"])
        bundle.soft_limit_max.on_change('value', __callback_soft_limit_max)
        # endregion soft_limit_max

        # region working_direction
        @update_config
        def __callback_working_direction(attr, old, new):
            _index = int(bundle.working_direction.active)
            config["WorkingDirection"] = config["WorkingDirections"][_index]

        working_direction = RadioButtonGroup(
            labels=config["WorkingDirections"],
            active=(config["WorkingDirections"].index(
                config["WorkingDirection"]))
        )
        working_direction.on_change('active', __callback_working_direction)
        bundle.working_direction = working_direction
        # endregion working_direction

        # region driving_speed_unit
        @update_config
        def __callback_driving_speed_unit(attr, old, new):
            unit_index = int(bundle.driving_speed_unit.active)
            config["DrivingSpeedUnit"] = config["DrivingSpeedUnits"][unit_index]

        driving_speed_unit = RadioButtonGroup(
            labels=config["DrivingSpeedUnits"],
            active=(config["DrivingSpeedUnits"].index(
                config["DrivingSpeedUnit"]))
        )
        driving_speed_unit.on_change('active', __callback_driving_speed_unit)
        # Disabled because no actual implementation is available
        driving_speed_unit.disabled = True
        bundle.driving_speed_unit = driving_speed_unit
        # endregion driving_speed_unit

        # region driving_speed
        @update_config
        def __callback_driving_speed(attr, old, new):
            driving_speed = eval_float(bundle.driving_speed.value)
            config["DrivingSpeed"] = driving_speed

        bundle.driving_speed.value = str(config["DrivingSpeed"])
        bundle.driving_speed.on_change('value', __callback_driving_speed)
        # Disabled because no actual implementation is available
        bundle.driving_speed.disabled = True
        # endregion driving_speed

        # region driving_acceleration_unit
        @update_config
        def __callback_driving_acceleration_unit(attr, old, new):
            unit_index = int(bundle.driving_acceleration_unit.active)
            config["DrivingAccelerationUnit"] = config["DrivingAccelerationUnits"][unit_index]

        driving_acceleration_unit = RadioButtonGroup(
            labels=config["DrivingAccelerationUnits"],
            active=(config["DrivingAccelerationUnits"].index(
                config["DrivingAccelerationUnit"]))
        )
        driving_acceleration_unit.on_change(
            'active', __callback_driving_acceleration_unit)
        # Disabled because no actual implementation is available
        driving_acceleration_unit.disabled = True
        bundle.driving_acceleration_unit = driving_acceleration_unit
        # endregion driving_acceleration_unit

        # region driving_acceleration
        @update_config
        def __callback_driving_acceleration(attr, old, new):
            driving_acceleration = eval_float(
                bundle.driving_acceleration.value)
            config["DrivingAcceleration"] = driving_acceleration

        bundle.driving_acceleration.value = str(
            config["DrivingAcceleration"])
        bundle.driving_acceleration.on_change(
            'value', __callback_driving_acceleration)
        # Disabled because no actual implementation is available
        bundle.driving_acceleration.disabled = True
        # endregion driving_acceleration

        # region test_online
        def __callback_test_online():
            try:
                self.lstat.fmtmsg(bundle.remote.online())
            except Exception as inst:
                print(type(inst), inst.args)
                self.lstat.expmsg(
                    "[Error] Nothing from remote, server is probably down.")

        bundle.test_online.on_click(__callback_test_online)
        # endregion test_online

        # region manual_move
        @ignore_connection_error
        @update_config
        def __callback_manual_move():
            """before actual movement, make sure it's sync with what is at the front panel"""
            delay = eval_float(bundle.manual_position.value)
            config["ManualPosition"] = config["ZeroDelayAbsolutePosition"] + \
                dt_to_mm(
                    delay, config["ManualUnit"], config["Multiples"], config["WorkingDirection"])
            response = bundle.remote.moveabs(config["ManualPosition"])
            self.lstat.fmtmsg(response)

        bundle.manual_move.on_click(__callback_manual_move)
        # endregion manual_move

        # region manual_step_forward
        @ignore_connection_error
        @update_config
        def __callback_manual_step_forward():
            config["ManualPosition"] += dt_to_mm(
                config["ManualStep"], config["ManualUnit"], config["Multiples"], config["WorkingDirection"])
            response = bundle.remote.moveabs(config["ManualPosition"])
            self.lstat.fmtmsg(response)

        bundle.manual_step_forward.on_click(__callback_manual_step_forward)
        # endregion manual_step_forward

        # region manual_step_backward
        @ignore_connection_error
        @update_config
        def __callback_manual_step_backward():
            config["ManualPosition"] -= dt_to_mm(
                config["ManualStep"], config["ManualUnit"], config["Multiples"], config["WorkingDirection"])
            response = bundle.remote.moveabs(config["ManualPosition"])
            self.lstat.fmtmsg(response)

        bundle.manual_step_backward.on_click(__callback_manual_step_backward)
        # endregion manual_step_backward

        # region scan_delay
        def scan_delay(func, meta=''):
            """
            decorator, when applied to func, scan delays for func
            addes or alters following meta params:
                meta[name]["Delay"] : str or float, current delay
                meta[name]["iDelay"]: int, index of current delay
            """
            def iterate(meta=dict()):
                if config["Mode"] == "Range" or config["Mode"] == "ExternalFile":
                    for i, dl in enumerate(self.lstat.stat[name]["ScanList"]):
                        if meta["TERMINATE"]:
                            self.lstat.expmsg(
                                "scan_delay received signal TERMINATE, trying graceful Thread exit")
                            break
                        self.lstat.expmsg(
                            "Setting delay to {dl} ps".format(dl=dl))
                        target_abs_pos = config["ZeroDelayAbsolutePosition"] + \
                            dt_to_mm(
                                dl, config["ManualUnit"], config["Multiples"], config["WorkingDirection"])
                        response = bundle.remote.moveabs(target_abs_pos)
                        self.lstat.fmtmsg(response)
                        self.lstat.stat[name]["Delay"] = dl
                        self.lstat.stat[name]["iDelay"] = i
                        func(meta=meta)
                else:
                    self.lstat.expmsg(
                        "Delay is set manually, so no action has been taken")
                    self.lstat.stat[name]["Delay"] = "ManualDelay"
                    self.lstat.stat[name]["iDelay"] = 0
                    func(meta=meta)
            return iterate

        bundle.scan_delay = scan_delay
        # endregion scan_delay

        # region set_delay
        def set_delay(delay):
            pos = config["ZeroDelayAbsolutePosition"] + dt_to_mm(
                delay, config["ManualUnit"], config["Multiples"], config["WorkingDirection"])
            response = bundle.remote.moveabs(pos)
            self.lstat.fmtmsg(response)

        bundle.set_delay = set_delay
        # endregion set_delay

        return bundle
