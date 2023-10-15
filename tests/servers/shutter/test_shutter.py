import unittest
import os
import json
import logging

from serial_helper import SerialManager, SerialMocker
from logging_helper import TestingLogFormatter

from servers.shutter import ShutterController
from servers.shutter.shutter import ShutterState

# configure root logger to output all logs to stdout
lg = logging.getLogger()
lg.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(TestingLogFormatter())
lg.addHandler(ch)
# configure logger for this module.
lg = logging.getLogger(__name__)


class TestShutter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        lg.info("Setting up SerialManager of ShutterController with a SerialMocker.")
        # create ShutterController that all threads shares according to config.json
        CONFIG_PATH = os.path.join(os.path.dirname(
            __file__), 'test_shutter_config.json')
        with open(CONFIG_PATH, 'r') as f:
            cfg = json.load(f)
            ser_cfg = cfg["serial"]

        ser_mgr = SerialManager(
            ser_cfg["port"], baudrate=ser_cfg["baudrate"], timeout=ser_cfg["timeout"])

        # mocked response according to our protocol
        response_map = {
            b"SHT1:OFF\n": b"OK, SHT1OFF\n",
            b"SHT1:ON\n": b"OK, SHT1ON\n",
            b"SHT2:OFF\n": b"OK, SHT2OFF\n",
            b"SHT2:ON\n": b"OK, SHT2ON\n",
        }

        # Replace serial object of ser_mgr with mocked one
        ser_mgr.ser = SerialMocker(
            ser_cfg["port"], baudrate=ser_cfg["baudrate"], timeout=ser_cfg["timeout"],
            response_map=response_map
        )

        lg.info("Starting up ShutterController")
        cls.sc = ShutterController(ser_mgr, shutter_names=cfg["shutter_names"])
        cls.sc.start()

    @classmethod
    def tearDownClass(cls):
        lg.info("Shutting down ShutterController")
        cls.sc.stop()

    def test_shutter_on_and_off(self):
        lg.debug("==== Testing shutter_on and shutter_off ====")
        lg.info("Initial state of shutters: {}".format(self.sc.shutter_states))
        lg.info("Testing shutter_on and shutter_off for 10 rounds")
        for _ in range(10):
            for shutter_name in self.sc.shutter_names:
                if self.sc.shutter_states[shutter_name] is ShutterState.OFF:
                    lg.info("Turning ON shutter {}".format(shutter_name))
                    self.sc.shutter_on(shutter_name)
                elif self.sc.shutter_states[shutter_name] is ShutterState.ON:
                    lg.info("Turning OFF shutter {}".format(shutter_name))
                    self.sc.shutter_off(shutter_name)
                else:
                    lg.error("Unknown shutter state {} for shutter {}!".format(
                        self.sc.shutter_states[shutter_name], shutter_name))
                lg.info("State of shutters: {}".format(self.sc.shutter_states))
        
    def test_switch_shutter(self):
        lg.debug("==== Testing switch_shutter ====")
        lg.info("Initial state of shutters: {}".format(self.sc.shutter_states))
        lg.info("Testing switch_shutter for 10 rounds")
        for _ in range(10):
            for shutter_name in self.sc.shutter_names:
                lg.info("Switching shutter {}".format(shutter_name))
                self.sc.switch_shutter(shutter_name)
                lg.info("State of shutters: {}".format(self.sc.shutter_states))



