# -*- coding: utf-8 -*-

"""
test_interlock.py:

Tests interlock module
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221122"

import time
import random
from threading import Thread

from labctrl.interlock import Interlock, AbstractInterlockRule, InterlockError

states = {
    "ShutterLaser": "Closed",
    "ShutterCamera": "Closed",
    "ShutterEyepiece": "Closed",
    "SampleTemperature": 30.0,
    "CameraContinuousMode": True,
    "CameraTriggerMode": False,
}


interlock = Interlock(states)


class ShutterRule1(AbstractInterlockRule):
    def check(self) -> bool:
        """
        Truth Table
        =================================
        b1      b2      b3      |   False   : All shutters open, disallowed
        b1      b2      /b3     |   False   : Laser shutter and camera shutter both open
        b1      /b2     b3      |   False   : Laser shutter and eyepiece shutter both open
        b1      /b2     /b3     |   True    : Laser shutter only open if other shutters close
        /b1     b2      b3      |   True    : Laser shutter closed, other states irrelevant
        /b1     b2      /b3     |   True    : Laser shutter closed, other states irrelevant
        /b1     /b2     b3      |   True    : Laser shutter closed, other states irrelevant
        /b1     /b2     /b3     |   True    : Laser shutter closed, other states irrelevant
        =================================
        """
        states: dict = self.interlock.states
        b1 = (states["ShutterLaser"] == "Open")
        b2 = (states["ShutterCamera"] == "Open")
        b3 = (states["ShutterEyepiece"] == "Open")
        if b1 and b3:
            return False
        if b1 and b2:
            return False
        else:
            return True


class SampleTemperatureRule1(AbstractInterlockRule):
    def check(self) -> bool:
        """
        Truth Table
        ========
        b1      b2      |   True    :
        b1      /b2     |   False   : Close laser shutter if overtemperature
        /b1     b2      |   True    : 
        /b1     /b2     |   True    : No rule violation because laser shutter already closed
        """
        states: dict = self.interlock.states
        b1 = (states["ShutterLaser"] == "Open")
        b2 = (states["SampleTemperature"] < 80.0)
        if b1 and not b2:
            return False
        else:
            return True


shutter_rule_1 = ShutterRule1("ShutterRule1", interlock)
temperature_rule_1 = SampleTemperatureRule1("TemperatureRule1", interlock)


def callback_open_shutter(shutter_name: str):
    # this is the callback function for user input
    previous_shutter_state = states[shutter_name]
    states[shutter_name] = "Open"
    try:
        open_shutter(shutter_name)
    except InterlockError as e:
        # this should update frontend GUI to notify user what happend
        # because this is just a test, let's print
        print(e)
        print("callback_open_shutter did not success, restoring to previous state")
        states[shutter_name] = previous_shutter_state


@interlock.interlocked
def open_shutter(shutter_name: str):
    # in actual code this function opens remote shutter
    print("Shutter {} Opened".format(shutter_name))


def callback_close_shutter(shutter_name: str):
    # this is the callback function for user input
    previous_shutter_state = states[shutter_name]
    states[shutter_name] = "Closed"
    try:
        close_shutter(shutter_name)
    except InterlockError as e:
        # this should update frontend GUI to notify user what happend
        # because this is just a test, let's print
        print(e, e.args)
        print("callback_close_shutter did not success, restoring to previous states")
        states[shutter_name] = previous_shutter_state


@interlock.interlocked
def close_shutter(shutter_name: str):
    # in actual code this function closes remote shutter
    print("Shutter {} closed".format(shutter_name))


# ================ TEST START ================

def serial_test():
    """
    Assuming this is the backend working thread running all of the callbacks
    """
    print("================ SERIAL TEST START ================")
    print("[TEST]: Open Laser Shutter, should work")
    callback_open_shutter("ShutterLaser")
    print("[STATES]: ", states)
    print("[TEST]: Close Laser Shutter, should work")
    callback_close_shutter("ShutterLaser")
    print("[STATES]: ", states)
    print("[TEST]: Open Laser Shutter, should work")
    callback_open_shutter("ShutterLaser")
    print("[STATES]: ", states)
    print("[TEST]: Open Camera Shutter, should error and catch exception")
    callback_open_shutter("ShutterCamera")
    print("[STATES]: ", states)
    print("[TEST]: Open Eyepiece Shutter, should error and catch exception")
    callback_open_shutter("ShutterEyepiece")
    print("[STATES]: ", states)
    print("================ END OF SERIAL TEST ================")


def monitor_test():
    """
    Use an independent thread to monitor
    """
    monitoring = True

    def monitor_task():
        while monitoring:
            print("[monitor_task thread]: Checking temperature")
            passing = temperature_rule_1.check()
            if not passing:
                # Emergent stop
                print(
                    "[monitor_task thread]: Detected rule violation, turn off laser shutter")
                callback_close_shutter("ShutterLaser")
            else:
                print("Temperature rule passed, temperature: {}".format(
                    states["SampleTemperature"]))
            time.sleep(0.05)
    print("================ MONITOR TEST START ================")
    thread = Thread(target=monitor_task)
    thread.start()
    # let's fake some data here, in actual enviroment the state
    # should be updated by sensor thread
    for i in range(30, 100):
        print("Updating temperature to {}".format(i))
        states["SampleTemperature"] = float(i)
        time.sleep(0.07)

    monitoring = False
    states["SampleTemperature"] = 30.0
    print("================ END OF MONITOR TEST ================")


def multithread_test():
    """
    check thread safety
    """
    running = True
    shutters_list = ["ShutterLaser", "ShutterCamera", "ShutterEyepiece"]
    shutter_states_list = ["Open", "Closed"]

    def thread_generator(i: int):
        def task():
            while running:
                # randomly update shutter states around every 0.1s
                sleeptime = random.random() * 0.2
                time.sleep(sleeptime)
                shutter_i = random.randint(0, 2)
                shutter_name = shutters_list[shutter_i]
                shutter_state_i = random.randint(0, 1)
                shutter_state = shutter_states_list[shutter_state_i]
                print(
                    "[Thread {}]: Switch random shutter state: {} -> {}".format(
                        i, shutter_name, shutter_state
                    )
                )
                if shutter_state == "Closed":
                    callback_close_shutter(shutter_name=shutter_name)
                else:
                    callback_open_shutter(shutter_name=shutter_name)

        thread = Thread(target=task)
        thread.start()
    
    print("================ MULTITHREAD TEST START ================")

    for i in range(5):
        thread_generator(i)

    # test for 10 seconds, print current state every 1 second
    for i in range(10):
        time.sleep(1)
        print("[Multithread Test]: Current state: ", states)

    running = False
    print("================ END OF MULTITHREAD TEST ================")


def test():
    serial_test()
    monitor_test()
    multithread_test()
