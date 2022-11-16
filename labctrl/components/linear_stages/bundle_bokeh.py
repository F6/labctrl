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

from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat

from .abstract import AbstractBundleLinearStage
from .remote import RemoteLinearStage
from .utils import eval_float, ignore_connection_error, eval_int, calculate_dx


class BundleBokehLinearStage(AbstractBundleLinearStage):
    def __init__(self, bundle_config: dict, lcfg: LabConfig, lstat: LabStat) -> None:
        super().__init__()

        self.config: dict = bundle_config["Config"]  # Axis Config
        self.name: str = self.config["Name"]
        self.lcfg = lcfg
        self.lstat = lstat

        update_config = self.lcfg.update_config  # Alias for easier access
        config = self.config  # Alias for easier access
        name = self.name  # Alias for easier access

        self.remote = RemoteLinearStage(config)

        self.update_scanlist(config)

        # ======== Param Configs ========
        self.host = TextInput(title="Host", value=config["Host"])
        self.port = TextInput(title="Port", value=str(config["Port"]))
        self.working_unit = RadioButtonGroup(
            labels=config["WorkingUnits"],
            active=(config["WorkingUnits"].index(config["WorkingUnit"]))
        )
        self.scan_mode = RadioButtonGroup(
            labels=config["ScanModes"], active=(config["ScanModes"].index(config["ScanMode"])))
        self.range_scan_start = TextInput(
            title="Range Scan Start", value=str(config["RangeScanStart"]))
        self.range_scan_stop = TextInput(
            title="Range Scan Stop", value=str(config["RangeScanStop"]))
        self.range_scan_step = TextInput(
            title="Range Scan Step", value=str(config["RangeScanStep"]))
        self.external_scan_list_file = FileInput(accept=".txt")
        self.position_unit = RadioButtonGroup(
            labels=config["PositionUnits"],
            active=(config["PositionUnits"].index(config["PositionUnit"]))
        )
        self.zero_point_absolute_position = TextInput(
            title="Zero Point Absolute Position", value=str(
                config["ZeroPointAbsolutePosition"]))
        self.manual_unit = RadioButtonGroup(
            labels=config["ManualUnits"],
            active=(config["ManualUnits"].index(config["WorkingUnit"]))
        )
        self.manual_position = TextInput(
            title="Manually set delay to", value=str(config["ManualPosition"]))
        self.manual_step = TextInput(
            title="Manually step delay", value=str(config["ManualStep"]))
        self.multiples = TextInput(
            title="Multiples", value=str(config["Multiples"]))
        self.soft_limit_min = TextInput(
            title="Soft Limit Min", value=str(config["SoftLimitMin"]))
        self.soft_limit_max = TextInput(
            title="Soft Limit Max", value=str(config["SoftLimitMax"]))
        self.working_direction = RadioButtonGroup(
            labels=config["WorkingDirections"],
            active=(config["WorkingDirections"].index(
                config["WorkingDirection"]))
        )
        self.driving_speed_unit = RadioButtonGroup(
            labels=config["DrivingSpeedUnits"],
            active=(config["DrivingSpeedUnits"].index(
                config["DrivingSpeedUnit"]))
        )
        self.driving_speed = TextInput(
            title="Driving Speed", value=str(config["DrivingSpeed"]))
        self.driving_acceleration_unit = RadioButtonGroup(
            labels=config["DrivingAccelerationUnits"],
            active=(config["DrivingAccelerationUnits"].index(
                config["DrivingAccelerationUnit"]))
        )
        self.driving_acceleration = TextInput(
            title="Driving Acceleration", value=str(
                config["DrivingAcceleration"]))
        # ======== Interactive Elements ========
        self.test_online = Button(label="Test Motion Controller Online")
        self.manual_move = Button(label='Move Stage', button_type='warning')
        self.manual_step_forward = Button(
            label="Step forward", button_type='warning')
        self.manual_step_backward = Button(
            label="Step backward", button_type='warning')
        # ======== Composites ========

        # region host
        @update_config
        def __callback_host(attr, old, new):
            # no validation here because host can be literally anything,
            # it is just a param passed to remote API
            config["Host"] = self.host.value
            # regenerate remote when config updated
            self.remote = RemoteLinearStage(config)

        self.host.on_change('value', __callback_host)
        # endregion host

        # region port
        @update_config
        def __callback_port(attr, old, new):
            # no validation here because port can be literally anything,
            # it is just a param passed to remote API
            config["Port"] = eval_int(self.port.value)
            # regenerate remote when config updated
            self.remote = RemoteLinearStage(config)

        self.port.on_change('value', __callback_port)
        # endregion port

        # region working_unit
        @update_config
        def __callback_working_unit(attr, old, new):
            unit_index = int(self.working_unit.active)
            config["WorkingUnit"] = config["WorkingUnits"][unit_index]

        self.working_unit.on_change('active', __callback_working_unit)
        # endregion working_unit

        # region scan_mode
        @update_config
        def __callback_scan_mode(attr, old, new):
            mode_index = int(self.scan_mode.active)
            config["ScanMode"] = config["ScanModes"][mode_index]
            if mode_index == 0:
                self.range_scan_start.visible = False
                self.range_scan_step.visible = False
                self.range_scan_stop.visible = False
                self.external_scan_list_file.visible = False
            elif mode_index == 1:
                self.range_scan_start.visible = True
                self.range_scan_step.visible = True
                self.range_scan_stop.visible = True
                self.external_scan_list_file.visible = False
            elif mode_index == 2:
                self.range_scan_start.visible = False
                self.range_scan_step.visible = False
                self.range_scan_stop.visible = False
                self.external_scan_list_file.visible = True
            self.update_scanlist(config)

        self.scan_mode.on_change('active', __callback_scan_mode)
        # endregion scan_mode

        # region range_scan_start
        @update_config
        def __callback_range_scan_start(attr, old, new):
            config["RangeScanStart"] = eval_float(
                self.range_scan_start.value)
            self.update_scanlist(config)

        self.range_scan_start.on_change('value', __callback_range_scan_start)
        # endregion range_scan_start

        # region range_scan_stop
        @update_config
        def __callback_range_scan_stop(attr, old, new):
            config["RangeScanStop"] = eval_float(self.range_scan_stop.value)
            self.update_scanlist(config)

        self.range_scan_stop.on_change('value', __callback_range_scan_stop)
        # endregion range_scan_stop

        # region range_scan_step
        @update_config
        def __callback_range_scan_step(attr, old, new):
            config["RangeScanStep"] = eval_float(self.range_scan_step.value)
            self.update_scanlist(config)

        self.range_scan_step.on_change('value', __callback_range_scan_step)
        # endregion range_scan_stop

        # region external_scan_list_file
        @update_config
        def __callback_external_scan_list_file(attr, old, new):
            self.lstat.expmsg("Loaded External Delay List")
            fcontent = base64.b64decode(
                self.external_scan_list_file.value).decode()
            # print(fcontent)
            config["Mode"] = "ExternalFile"
            self.scan_mode.active = config["ScanModes"].index(config["Mode"])
            config["LoadedExternalScanList"] = list(
                map(float, fcontent.split()))
            self.update_scanlist(config)

        self.external_scan_list_file.on_change(
            'value', __callback_external_scan_list_file)
        # endregion external_scan_list_file

        # region position_unit
        @update_config
        def __callback_position_unit(attr, old, new):
            unit_index = int(self.position_unit.active)
            config["PositionUnit"] = config["PositionUnits"][unit_index]

        self.position_unit.on_change('active', __callback_position_unit)
        # Disabled because no actual implementation is available
        self.position_unit.disabled = True
        # endregion position_unit

        # region zero_point_absolute_position
        @update_config
        def __callback_zero_point_absolute_position(attr, old, new):
            config["ZeroPointAbsolutePosition"] = eval_float(
                self.zero_point_absolute_position.value)

        self.zero_point_absolute_position.on_change(
            'value', __callback_zero_point_absolute_position)
        # endregion zero_delay_absolute_position

        # region manual_unit
        @update_config
        def __callback_manual_unit(attr, old, new):
            unit_index = int(self.manual_unit.active)
            config["ManualUnit"] = config["ManualUnits"][unit_index]

        self.manual_unit.on_change('active', __callback_manual_unit)
        # endregion manual_unit

        # region manual_position
        @update_config
        def __callback_manual_position(attr, old, new):
            offset = eval_float(self.manual_position.value)
            config["ManualPosition"] = offset + \
                config["ZeroPointAbsolutePosition"]

        self.manual_position.on_change('value', __callback_manual_position)
        # endregion manual_position

        # region manual_step
        @update_config
        def __callback_manual_step(attr, old, new):
            step = eval_float(self.manual_step.value)
            config["ManualStep"] = step

        self.manual_step.on_change('value', __callback_manual_step)
        # endregion manual_step

        # region multiples
        @update_config
        def __callback_multiples(attr, old, new):
            multiples = eval_float(self.multiples.value)
            config["Multiples"] = multiples

        self.multiples.on_change('value', __callback_multiples)
        # endregion multiples

        # region soft_limit_min
        @update_config
        def __callback_soft_limit_min(attr, old, new):
            soft_limit_min = eval_float(self.soft_limit_min.value)
            config["SoftLimitMin"] = soft_limit_min

        self.soft_limit_min.on_change('value', __callback_soft_limit_min)
        # endregion soft_limit_min

        # region soft_limit_max
        @update_config
        def __callback_soft_limit_max(attr, old, new):
            soft_limit_max = eval_float(self.soft_limit_max.value)
            config["SoftLimitMax"] = soft_limit_max

        self.soft_limit_max.on_change('value', __callback_soft_limit_max)
        # endregion soft_limit_max

        # region working_direction
        @update_config
        def __callback_working_direction(attr, old, new):
            _index = int(self.working_direction.active)
            config["WorkingDirection"] = config["WorkingDirections"][_index]

        self.working_direction.on_change(
            'active', __callback_working_direction)
        # endregion working_direction

        # region driving_speed_unit
        @update_config
        def __callback_driving_speed_unit(attr, old, new):
            unit_index = int(self.driving_speed_unit.active)
            config["DrivingSpeedUnit"] = config["DrivingSpeedUnits"][unit_index]

        self.driving_speed_unit.on_change(
            'active', __callback_driving_speed_unit)
        # Disabled because no actual implementation is available
        self.driving_speed_unit.disabled = True
        # endregion driving_speed_unit

        # region driving_speed
        @update_config
        def __callback_driving_speed(attr, old, new):
            driving_speed = eval_float(self.driving_speed.value)
            config["DrivingSpeed"] = driving_speed

        self.driving_speed.on_change('value', __callback_driving_speed)
        # Disabled because no actual implementation is available
        self.driving_speed.disabled = True
        # endregion driving_speed

        # region driving_acceleration_unit
        @update_config
        def __callback_driving_acceleration_unit(attr, old, new):
            unit_index = int(self.driving_acceleration_unit.active)
            config["DrivingAccelerationUnit"] = config["DrivingAccelerationUnits"][unit_index]

        self.driving_acceleration_unit.on_change(
            'active', __callback_driving_acceleration_unit)
        # Disabled because no actual implementation is available
        self.driving_acceleration_unit.disabled = True
        # endregion driving_acceleration_unit

        # region driving_acceleration
        @update_config
        def __callback_driving_acceleration(attr, old, new):
            driving_acceleration = eval_float(
                self.driving_acceleration.value)
            config["DrivingAcceleration"] = driving_acceleration

        self.driving_acceleration.on_change(
            'value', __callback_driving_acceleration)
        # Disabled because no actual implementation is available
        self.driving_acceleration.disabled = True
        # endregion driving_acceleration

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

        # region manual_move
        @ignore_connection_error
        @update_config
        def __callback_manual_move():
            """before actual movement, make sure it's sync with what is at the front panel"""
            offset = eval_float(self.manual_position.value)
            config["ManualPosition"] = config["ZeroPointAbsolutePosition"] + \
                calculate_dx(
                    offset, config["ManualUnit"], config["Multiples"], config["WorkingDirection"])
            response = self.remote.moveabs(config["ManualPosition"])
            self.lstat.fmtmsg(response)

        self.manual_move.on_click(__callback_manual_move)
        # endregion manual_move

        # region manual_step_forward
        @ignore_connection_error
        @update_config
        def __callback_manual_step_forward():
            config["ManualPosition"] += calculate_dx(
                config["ManualStep"], config["ManualUnit"], config["Multiples"], config["WorkingDirection"])
            response = self.remote.moveabs(config["ManualPosition"])
            self.lstat.fmtmsg(response)

        self.manual_step_forward.on_click(__callback_manual_step_forward)
        # endregion manual_step_forward

        # region manual_step_backward
        @ignore_connection_error
        @update_config
        def __callback_manual_step_backward():
            config["ManualPosition"] -= calculate_dx(
                config["ManualStep"], config["ManualUnit"], config["Multiples"], config["WorkingDirection"])
            response = self.remote.moveabs(config["ManualPosition"])
            self.lstat.fmtmsg(response)

        self.manual_step_backward.on_click(__callback_manual_step_backward)
        # endregion manual_step_backward

        def scan_range(func, meta=''):
            """
            decorator, when applied to func, scan range for func.
            adds or alters the following meta params:
                meta[name]["Delay"] : str or float, current position
                meta[name]["iDelay"]: int, index of current position
            """
            def iterate(meta=dict()):
                if config["ScanMode"] == "Range" or config["ScanMode"] == "ExternalFile":
                    for i, pos in enumerate(self.lstat.stat[name]["ScanList"]):
                        if meta["TERMINATE"]:
                            self.lstat.expmsg(
                                "[{name}][scan_range] Received signal TERMINATE, trying graceful Thread exit".format(name=name))
                            break
                        self.lstat.expmsg(
                            "[{name}][scan_range] Setting position to {pos} {unit}".format(name=name, pos=pos, unit=config["WorkingUnit"]))
                        target_abs_pos = config["ZeroPointAbsolutePosition"] + calculate_dx(
                            pos, config["WorkingUnit"], config["Multiples"], config["WorkingDirection"])
                        response = self.remote.moveabs(target_abs_pos)
                        self.lstat.fmtmsg(response)
                        self.lstat.stat[name]["Delay"] = pos
                        self.lstat.stat[name]["iDelay"] = i
                        func(meta=meta)
                else:
                    self.lstat.expmsg(
                        "[{name}][scan_range] Range is set manually, so no action has been taken".format(name=name))
                    self.lstat.stat[name]["Delay"] = "ManualDelay"
                    self.lstat.stat[name]["iDelay"] = 0
                    func(meta=meta)
            return iterate

        self.scan_range = scan_range

    def set_position(self, position: float):
        response = self.remote.moveabs(position)
        self.lstat.fmtmsg(response)
    
    def set_delay(self, delay: float):
        pos = self.config["ZeroPointAbsolutePosition"] + calculate_dx(
            delay, self.config["WorkingUnit"], self.config["Multiples"], self.config["WorkingDirection"])
        response = self.remote.moveabs(pos)
        self.lstat.fmtmsg(response)

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
