# -*- coding: utf-8 -*-

"""shutter_controller.py:
This module provides the ShutterController class to control a shutter connected via a serial port.
the shutter controller is the self-made one (gray aluminum box)
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20231009"

import logging

from enum import Enum

from serial_helper import SerialManager

# set up logging
lg = logging.getLogger(__name__)

# Meta parameters
MAX_CHANNEL_NUMBER = 16
DEFALUT_SHUTTER_NAMES = ["1", "2"]


class ShutterState(Enum):
    OFF = "OFF"
    ON = "ON"


class ShutterAction(Enum):
    TURN_ON = "ON"
    TURN_OFF = "OFF"
    SWITCH = "SWITCH"


class ShutterActionResult(Enum):
    OK = "OK"
    SERIAL_RW_FAILURE = "serial_RW_failure"
    SHUTTER_NOT_FOUND = "shutter_not_found"
    INVALID_ACTION = "invalid_action"
    RESPONSE_VALIDATION_FAILURE = "response_validation_failure"


class ShutterController:
    def __init__(
            self, ser_mgr: SerialManager,
            shutter_names: list[str] = DEFALUT_SHUTTER_NAMES) -> None:
        self.ser_mgr = ser_mgr
        self.shutter_names = shutter_names.copy()
        self.shutter_states: dict[str, ShutterState] = dict()
        self.command_id: int = 0
        assert len(shutter_names) < MAX_CHANNEL_NUMBER
        for name in shutter_names:
            self.shutter_states[name] = ShutterState.OFF
        lg.debug("ShutterController initialzed.")

    def start(self):
        lg.info("Starting ShutterController")
        self.ser_mgr.start()
        lg.info("ShutterController started.")

    def stop(self):
        lg.info("Gracefully shutting down ShutterController")
        self.ser_mgr.stop()
        lg.info("ShutterController stopped.")

    def command(self, s: str):
        lg.debug("Sending command {}".format(s))
        self.command_id += 1
        self.ser_mgr.send(s.encode('ascii'), sent_id=self.command_id)
        # wait for sending confirmation
        t_send, sid_returned = self.ser_mgr.sent_id_queue.get()
        # wait for response
        t_receive, response = self.ser_mgr.receive()
        # check for matching
        # [TODO]
        return response.decode()

    def shutter_off(self, shutter_name: str) -> ShutterActionResult:
        if shutter_name not in self.shutter_names:
            lg.error("Shutter {} is not bound to this ShutterController! ")
            return ShutterActionResult.SHUTTER_NOT_FOUND
        if self.shutter_states[shutter_name] is ShutterState.OFF:
            lg.warning(
                "shutter_off called when ShutterController believes that the shutter is already in OFF state.")
            lg.warning(
                "Check if the physical device is out of sync with ShutterController.")
            lg.warning("Sending the shutter_off command to device shutter {} anyway.".format(
                shutter_name))
        lg.debug("Turning OFF shutter {}".format(shutter_name))
        r = self.command('SHT{i}:OFF\n'.format(i=shutter_name))
        self.shutter_states[shutter_name] = ShutterState.OFF
        lg.debug("Reponse from device: {}".format(r))
        # [TODO]: validate if r is the same as defined in protocol
        return ShutterActionResult.OK

    def shutter_on(self, shutter_name: str) -> ShutterActionResult:
        if shutter_name not in self.shutter_names:
            lg.error("Shutter {} is not bound to this ShutterController! ")
            return ShutterActionResult.SHUTTER_NOT_FOUND
        if self.shutter_states[shutter_name] is ShutterState.ON:
            lg.warning(
                "shutter_on called when ShutterController believes that the shutter is already in ON state.")
            lg.warning(
                "Check if the physical device is out of sync with ShutterController.")
            lg.warning("Sending the shutter_on command to device shutter {} anyway.".format(
                shutter_name))
        lg.debug("Turning ON shutter {}".format(shutter_name))
        r = self.command('SHT{i}:ON\n'.format(i=shutter_name))
        self.shutter_states[shutter_name] = ShutterState.ON
        # [TODO]: validate if r is the same as defined in protocol
        return ShutterActionResult.OK

    def switch_shutter(self, shutter_name: str) -> ShutterActionResult:
        if self.shutter_states[shutter_name] is ShutterState.ON:
            r = self.shutter_off(shutter_name)
        else:
            r = self.shutter_on(shutter_name)
        return r

    def shutter_action(self, shutter_name: str, action: ShutterAction) -> ShutterActionResult:
        if action is ShutterAction.TURN_OFF:
            self.shutter_off(shutter_name)
        elif action is ShutterAction.TURN_ON:
            self.shutter_on(shutter_name)
        elif action is ShutterAction.SWITCH:
            self.switch_shutter(shutter_name)
        else:
            return ShutterActionResult.SHUTTER_NOT_FOUND
        return ShutterActionResult.OK
