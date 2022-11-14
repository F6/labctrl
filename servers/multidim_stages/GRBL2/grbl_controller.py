import serial
import time
import sys
import json
import os
from threading import Thread
from GRBL_interface_parser import GRBLParser

WRITE_BUFFER_MAX_LEN = 64


class GRBLController:
    def __init__(self, com: str) -> None:
        self.com = com
        self.ser = serial.Serial(self.com, baudrate=115200, timeout=1)
        self.parser = GRBLParser()
        self.write_buffer = []
        self.running = True
        self.thread = Thread(target=self.controller_task)
        self.thread.start()
        self.position_storage_file = "last_position.json"
        self.basic_config()

    def basic_config(self):
        """
        Send basic configs to grbl board
        For efficient transmission and precision management, we will not use GRBL's
        built-in pulse-to-mm manager, instead, we use fixed 100 pulses per mm, so
        that the feedback information can be as accurate as possible.
        The actual mm to pulse count conversion is done manually at python side.
        """
        # Set pulses/mm for X axis to 100
        print("Setting pulses per step to 100")
        self.stream_gcode("$100=100")
        # Set pulses/mm for Y axis to 100
        self.stream_gcode("$101=100")
        # Set pulses/mm for Z axis to 100
        self.stream_gcode("$102=100")
        # Set basic feedrate for all axis to 100
        print("Setting basic feedrate")
        self.stream_gcode("G1 F100")
        if self.position_storage_file in os.listdir():
            print("Loading stored state...")
            with open(self.position_storage_file, 'r') as f:
                last_state = json.load(f)
            # wait for at least one state report so that the parser state dict is not empty
            self.block_until_idle()
            x_saved = last_state["MachineX"]
            y_saved = last_state["MachineY"]
            z_saved = last_state["MachineZ"]
            x_offset_changed = (
                x_saved != self.parser.vars["MachineX"])
            y_offset_changed = (
                y_saved != self.parser.vars["MachineY"])
            z_offset_changed = (
                z_saved != self.parser.vars["MachineZ"])
            if (x_offset_changed or y_offset_changed or z_offset_changed):
                print("""[WARNING]: On-board X, Y and Z positions are lost, offsets may be present in 
current system, homing is recommanded to re-establish absolute coordinates.""")
                # G92: Sets the current coordinate point, used to set an origin point of zero,
                #       commonly known as the home position.
                # self.stream_gcode("G92 X{x_saved} Y{y_saved} Z{z_saved}".format(
                #     x_saved=x_saved, y_saved=y_saved, z_saved=z_saved))

    def dump_state(self):
        """
        Because GRBL resets itself everytime disconnected from computer or powered off,
            dump parser vars to retrive working coordinate offsets when power on again
        """
        with open('./' + self.position_storage_file, 'w') as f:
            json.dump(self.parser.vars, f, indent=4)

    def parse_buf(self, buf):
        messages = buf.decode().split('\n')
        for message in messages:
            # print("[Parser]: Parsing: {}".format(message))
            self.parser.parse_push_message(message)
            # print("[Parser]: Parsed result: {}".format(self.parser.vars))
            sys.stdout.flush()
        return buf

    def controller_task(self):
        prev = time.time()
        while self.running:
            now = time.time()
            if now - prev > 0.1:
                self.stream_gcode('?')
            time.sleep(0.05)
            if self.ser.in_waiting:
                buf = self.ser.read_all()
                try:
                    self.parse_buf(buf)
                except Exception as e:
                    print(e)
                    sys.stdout.flush()
            while len(self.write_buffer) > 0:
                to_write = self.write_buffer.pop(0)
                to_write = to_write.encode('ascii')
                self.ser.write(to_write)
        print("GRBL controller thread stopped.")
        sys.stdout.flush()
        return

    def stream_gcode(self, gcode):
        if WRITE_BUFFER_MAX_LEN > len(self.write_buffer):
            # special treatment for ? because it does not need \r\n...
            if gcode == "?":
                self.write_buffer.append(gcode)
            else:
                self.write_buffer.append(gcode + '\r\n')
        else:
            timeout = 10.0
            t0 = time.time()
            while WRITE_BUFFER_MAX_LEN <= len(self.write_buffer):
                t = time.time()
                if t - t0 > timeout:
                    print(
                        "Timeout when writing g-code to buffer! Latest command is ignored")
                    return
                time.sleep(0.1)
            self.write_buffer.append(gcode)

    def block_until_idle(self, timeout=100):
        t0 = time.time()
        while True:
            if self.parser.vars["State"] == 'Idle':
                break
            t = time.time()
            if t - t0 > timeout:
                print("Timeout waiting for Idle!")
                break
            time.sleep(0.05)

    def blocking_gcode_command(self, gcode):
        """
        Send a gcode to current buffer and wait for state to become idle.
        Warning: This sometimes fails because GRBL state only turns into
                    running after some time, and the state update rate
                    is also limited, so it is possible that the waiting condition
                    evaluation happens before the state change, and the waiting 
                    will return immediately because it sees an idle state.
                 To avoid this, increase the time delay between command
                    and waiting function. But this reduces efficiency, so
                    balance the efficiency and reliability yourself...
        """
        self.stream_gcode(gcode)
        time.sleep(0.2)
        self.block_until_idle()

    def moved_to_target(self, x, y, z):
        epsilon_in_place = 0.001
        x_in_place = abs(self.parser.vars["MachineX"] - x) < epsilon_in_place
        y_in_place = abs(self.parser.vars["MachineY"] - y) < epsilon_in_place
        z_in_place = abs(self.parser.vars["MachineZ"] - z) < epsilon_in_place
        state_is_idle = (self.parser.vars["State"] == "Idle")
        return x_in_place and y_in_place and z_in_place and state_is_idle

    def blocking_moveabs(self, x:float, y:float, z:float):
        """
        Send a movement command gcode to current buffer and wait for state to become idle.
        This is more reliable than the above, because it checks both idle state and
            machine position.
        """
        gcode = "G1 X{x:.3f} Y{y:.3f} Z{z:.3f}".format(x=x, y=y, z=z)
        self.stream_gcode(gcode)
        while not self.moved_to_target(x, y, z):
            time.sleep(0.1)
        self.dump_state()

    def close(self):
        self.running = False
        time.sleep(1)  # wait for last buffers to finish
        self.ser.close()
