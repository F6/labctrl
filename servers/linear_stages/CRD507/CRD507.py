# -*- coding: utf-8 -*-

"""CRD507.py:
This module provides simple controlling class for
the 5-phase stepper motor driver CRD507-KD from Oriental Motor
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220105"

import time
import pymodbus
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.exceptions import ModbusIOException


class CRD507ConnectionFail(Exception):
    pass


class CRD507:
    def __init__(self) -> None:
        self.address = 0x2
        # for rotators
        self.steps_per_degree = 2000
        # for linear stages
        self.steps_per_mm = 2000
        # try to connect to device
        self.client = ModbusClient(
            method='rtu',
            port="COM6",
            baudrate=115200,
            parity='E',
            timeout=0.1
        )
        connection = self.client.connect()
        if connection:
            pass
        else:
            raise CRD507ConnectionFail
        # try to load previous position record since last power off
        try:
            with open('curr_pos.txt', 'r') as f:
                self.curr_pos = int(f.read())
        except (FileNotFoundError, ValueError) as e:
            print("Init Warning: No previous position record find, or data is corrupted. Did the device or program shut down gracefully last time? The position information cannot be resumed because it operates in open loop mode, autohome is required for the program to find zero position again.")
            print("I'm automatically autohoming for you, if this is not desired, you can manually create the curr_pos.txt file, be aware of potentially corrupting other people's experiment configurations since this sets the device zero to arbitrary position.")
            self.autohome()

        self.__init_params()

    def retry_for_modbus_io_exception(func):
        def ret(*args, **kwargs):
            for i in range(10):
                time.sleep(0.1)
                result = func(*args, **kwargs)
                if type(result) is ModbusIOException:
                    print(
                        "Modbus IO Exception raised during command, retrying command again")
                else:
                    break
            return result
        return ret

    @retry_for_modbus_io_exception
    def __init_params(self):
        # 0x0204 = C-ON logic configuration, always reset this to make sure start command exec correctly
        result = self.client.write_register(0x0204, 0, unit=self.address)

    # the original CRD507-KD can store up to 63 sets of data for contineous
    # opearation or simple programmed operations, but because we are always online,
    # only the first registers are used
    @retry_for_modbus_io_exception
    def set_deceleration(self, pos: int):
        # 1 - 1000000, default = 30000
        upper = (pos & 0xFFFF0000) >> 16
        lower = pos & 0x0000FFFF
        return self.client.write_registers(0x0A02, (upper, lower), unit=self.address)

    @retry_for_modbus_io_exception
    def set_acceleration(self, pos: int):
        # 1 - 1000000, default = 30000
        upper = (pos & 0xFFFF0000) >> 16
        lower = pos & 0x0000FFFF
        return self.client.write_registers(0x0902, (upper, lower), unit=self.address)

    @retry_for_modbus_io_exception
    def set_speed(self, pos: int):
        # 1 - 500000, default = 1000
        upper = (pos & 0xFFFF0000) >> 16
        lower = pos & 0x0000FFFF
        return self.client.write_registers(0x0502, (upper, lower), unit=self.address)

    @retry_for_modbus_io_exception
    def __set_position(self, pos: int):
        # incremental, not absolute position (the driver cannot remember current position, we have to keep track of if by ourselves)
        # -2^23 ~ 2^23-1 (8388607)
        upper = (pos & 0xFFFF0000) >> 16
        lower = pos & 0x0000FFFF
        return self.client.write_registers(0x0402, (upper, lower), unit=self.address)

    def __start(self):
        """
        COMMAND1 address is 0x001E, 2 bytes to write

        Byte    Bit7    Bit6    Bit5    Bit4    Bit3    Bit2    Bit1    Bit0
        Upper    -       -      C-ON    STOP    HOME    RVS     FWD     START
        Lower    -       -      M5      M4      M3      M2      M1      M0

        Signal name     Description                         Setting range               Initial value

        M0 to M5        Specify the operation da
                        ta number using six bits.           0 to 63: Operation data     No. 0

        START           Perform positioning operation.      0: No action
                                                            1: Start operation          0

        FWD             Perform continuous operation        0: Deceleration stop
                        in the forward direction.           1: Operation                0

        RVS             Perform continuous operation 
                        in the reverse direction.                                       0

        HOME            Perform return-to-home operation.   0: No action
                                                            1: Start operation          0

        STOP            Stop the motor.                     0: No action
                                                            1: Stop                     0

        C-ON            Switch the motor excitation         0: Motor is not excited *
                        setting (excited/not excited).      1: Motor is excited *       0

            *: When the "C-ON logic configuration" parameter is set to "0"
        """
        self.__set_start()
        self.__reset_start()

    @retry_for_modbus_io_exception
    def __set_start(self):
        # set C-ON=1, START=1, M0=1, after this, START_R should read 1.
        command = 0b0010000100000001
        return self.client.write_register(0x001E, command, unit=self.address)

    @retry_for_modbus_io_exception
    def __reset_start(self):
        # reset START register for next operation. This does not stop the motor, if stop is needed, set STOP
        command = 0b0010000000000001
        result = self.client.write_register(0x001E, command, unit=self.address)

    def __log_position(self, pos: int):
        """log current position so that the open loop system can roughly know the current pos"""
        self.curr_pos = pos
        with open('curr_pos.txt', 'w') as f:
            f.write(str(self.curr_pos))

    def __wait_for_moving(self):
        """read register until MOVE is reset"""
        while True:
            status = self.parse_status(self.get_status())
            if not status["MOVE"]:
                break
            time.sleep(0.1)

    @retry_for_modbus_io_exception
    def get_status(self):
        return self.client.read_holding_registers(0x0133, 2, unit=self.address)

    def parse_status(self, status_result):
        status = dict()
        # result.registers[0]
        status["MOVE"] = status_result.registers[1] & 0b0000000000000001
        return status

    def setpos(self, pos: int):
        inc = int(pos - self.curr_pos)
        dir = 1 if inc >= 0 else -1
        # the driver supports only 2^23 steps for a single start
        self.__set_position(8388607 * dir)
        while abs(inc) > 8388607:
            self.__start()
            self.__wait_for_moving()
            self.__log_position(pos)
            inc -= 8388607 * dir
        self.__set_position(inc)
        self.__start()
        self.__wait_for_moving()
        self.__log_position(pos)

    def clear_fault(self):
        self.client.write_register(0x0040, 1, unit=self.address)
        time.sleep(0.1)
        self.client.write_register(0x0040, 0, unit=self.address)
        time.sleep(0.1)

    def autohome(self):
        """[TODO]"""
        self.curr_pos = 0

    def moveabs(self, pos_mm):
        target = int(pos_mm * self.steps_per_mm)
        self.setpos(target)

    def rotateabs(self, pos_deg, backlash_compensation=0.2):
        target = int(pos_deg * self.steps_per_degree)
        if backlash_compensation:
            if target >= self.curr_pos: # rotating forward, no need to compensate
                self.setpos(target)
            else:
                # Rotators, especially worm drive type rotators, suffer from backlash when rotate backwards.
                # A simple way to compesate is when rotating backwords, rotate a bit more, then rotate back 
                target = int((pos_deg-backlash_compensation) * self.steps_per_degree)
                self.setpos(target)
                target = int(pos_deg * self.steps_per_degree)
                self.setpos(target)
        else:
            self.setpos(target)

stage = CRD507()