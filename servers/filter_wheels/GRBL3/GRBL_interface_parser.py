# -*- coding: utf-8 -*-

"""
======== GRBL V1.1 Parser Ported From bCNC ========
Original File: bCNC/bCNC/controllers/GRBL1.py 
Original Author: vlachoudis/bCNC
Original File License: GNU General Public License v2.0

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Please see https://github.com/vlachoudis/bCNC for more information
======== End of Copyright Notice ========

Major changes:
    - Disconnected the parser from CNC class for independent usage
    - Now parsed results are stored in the parser object field obj.vars as a dict
    - Renamed parsed fields from shorthands to full names
    - Not actually used by now, but I've kept the _updated flags in the class in case needed
    - Added a parse method to detect what method to use to parse current msg

Please see https://github.com/gnea/grbl/wiki/Grbl-v1.1-Interface for detailed GRBL protocol 

"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221108"

import re


# This is used for GRBL V0.9 output, obsolete now
# re_str_GRBL_0_9 = r"<(?P<State>Idle|Run|Hold|Home|Alarm|Check|Door)(?:,MPos:(?P<MX>[0-9\.]*),(?P<MY>[0-9\.]*),(?P<MZ>[0-9\.]*))?(?:,WPos:(?P<WX>[0-9\.]*),(?P<WY>[0-9\.]*),(?P<WZ>[0-9\.]*))?(?:,Buf:(?P<Buf>[0-9]*))?(?:,RX:(?P<RX>[0-9]*))?(?:,Ln:(?P<L>[0-9]*))?(?:,F:(?P<F>[0-9\.]*))?(?:,Lim:(?P<Lim>[0-1]*))?(?:,Ctl:(?P<Ctl>[0-1]*))?>"


SPLITPAT = re.compile(r"[:,]")


class GRBLParser:
    def __init__(self) -> None:
        self.digits = 6  # original default CNC.digits = 4 in bCNC
        self._state_updated = False
        self._previous_state = ""
        self._pos_update = False
        self._probe_update = False
        self._g_update = False
        self.vars = dict()
        self.vars["State"] = "Initialize"
        """ Fields:
            Original    Ported to
            ======================
            state       State
            pins        Pins
            mx          MachineX
            my          MachineY
            mz          MachineZ
            wx          WorkingX
            wy          WorkingY
            wz          WorkingZ
            wcox        WorkingCoordinateOffsetX
            wcoy        WorkingCoordinateOffsetY
            wcoz        WorkingCoordinateOffsetZ
            ma          MachineA
            wa          WorkingA
            wcoa        WorkingCoordinateOffsetA
            mb          MachineB
            wb          WorkingB
            wcob        WorkingCoordinateOffsetB
            mc          MachineC
            wc          WorkingC
            wcoc        WorkingCoordinateOffsetC
            curfeed     CurrentFeedRate
            curspindle  CurrentSpindleSpeed
            planner     PlannerBufferAvailableBlocks
            rxbytes     RXBufferAvailableBytes
            OvFeed      OverrideFeed
            OvRapid     OverrideRapid
            OvSpindle   OverrideSpindle

            prbx        ProbeX
            prby        ProbeY
            prbz        ProbeZ
        """

    def log_msg(self, msg):
        # print("[LOG]: ", msg)
        pass

    def parse_push_message(self, message: str):
        message = message.strip('\r\n') # removes trailing \r or \n, no matter what order
        # message = message.strip('\n')
        # message = message.strip('\r')
        if message.startswith('<'):
            # status report data
            self.parseBracketAngle(message)
        elif message.startswith('Grbl'):
            # Welcome message; indicates initialization.
            self.log_msg(message)
        elif message.startswith('ALARM'):
            # Indicates an alarm has been thrown. Grbl is now in an alarm state.
            self.log_msg(message)
        elif message.startswith('$'):
            # $x=val and $Nx=line indicate a settings printout from a $ and $N user query, respectively.
            self.log_msg(message)
        elif message.startswith('['):
            # handle all square bracket messages, see interface doc
            self.parseBracketSquare(message)
        elif message.startswith('>'):
            # open chevron indicates startup line execution.
            self.log_msg(message)
        elif message.startswith('ok'):
            # just simple verification message, no action needed
            self.log_msg(message)
        elif message == '':
            # empty message, do nothing
            pass
        else:
            self.log_msg(
                "[ERROR]: Malformed data received! Original Message: {}".format(message))

    def parseBracketAngle(self, line: str):
        line = line.strip('\n')
        fields = line[1:-1].split("|")
        self.vars["Pins"] = ""

        self._previous_state = self.vars["State"]
        self.vars["State"] = fields[0]

        for field in fields[1:]:
            word = SPLITPAT.split(field)
            if word[0] == "MPos":
                try:
                    self.vars["MachineX"] = float(word[1])
                    self.vars["MachineY"] = float(word[2])
                    self.vars["MachineZ"] = float(word[3])
                    # self.vars["WorkingX"] = round(
                    #     self.vars["MachineX"] - self.vars["WorkingCoordinateOffsetX"], self.digits
                    # )
                    # self.vars["WorkingY"] = round(
                    #     self.vars["MachineY"] - self.vars["WorkingCoordinateOffsetY"], self.digits
                    # )
                    # self.vars["WorkingZ"] = round(
                    #     self.vars["MachineZ"] - self.vars["WorkingCoordinateOffsetZ"], self.digits
                    # )
                    if len(word) > 4:
                        self.vars["MachineA"] = float(word[4])
                        # self.vars["WorkingA"] = round(
                        #     self.vars["MachineA"] - self.vars["WorkingCoordinateOffsetA"], self.digits
                        # )
                    if len(word) > 5:
                        self.vars["MachineB"] = float(word[5])
                        # self.vars["WorkingB"] = round(
                        #     self.vars["MachineB"] - self.vars["WorkingCoordinateOffsetB"], self.digits
                        # )
                    if len(word) > 6:
                        self.vars["MachineC"] = float(word[6])
                        # self.vars["WorkingC"] = round(
                        #     self.vars["MachineC"] - self.vars["WorkingCoordinateOffsetC"], self.digits
                        # )
                    self._pos_update = True
                except (ValueError, IndexError):
                    self.vars["State"] = f"Garbage receive {word[0]}: {line}"
                    self.log_msg(self.vars["State"])
                    break
            elif word[0] == "F":
                try:
                    self.vars["CurrentFeedRate"] = float(word[1])
                except (ValueError, IndexError):
                    self.vars["State"] = f"Garbage receive {word[0]}: {line}"
                    self.log_msg(self.vars["State"])
                    break
            elif word[0] == "FS":
                try:
                    self.vars["CurrentFeedRate"] = float(word[1])
                    self.vars["CurrentSpindleSpeed"] = float(word[2])
                except (ValueError, IndexError):
                    self.vars["State"] = f"Garbage receive {word[0]}: {line}"
                    self.log_msg(self.vars["State"])
                    break
            elif word[0] == "Bf":
                try:
                    self.vars["PlannerBufferAvailableBlocks"] = int(word[1])
                    self.vars["RXBufferAvailableBytes"] = int(word[2])
                except (ValueError, IndexError):
                    self.vars["State"] = f"Garbage receive {word[0]}: {line}"
                    self.log_msg(self.vars["State"])
                    break
            elif word[0] == "Ov":
                try:
                    self.vars["OverrideFeed"] = int(word[1])
                    self.vars["OverrideRapid"] = int(word[2])
                    self.vars["OverrideSpindle"] = int(word[3])
                except (ValueError, IndexError):
                    self.vars["State"] = f"Garbage receive {word[0]}: {line}"
                    self.log_msg(self.vars["State"])
                    break
            elif word[0] == "WCO":
                try:
                    self.vars["WorkingCoordinateOffsetX"] = float(word[1])
                    self.vars["WorkingCoordinateOffsetY"] = float(word[2])
                    self.vars["WorkingCoordinateOffsetZ"] = float(word[3])

                    if len(word) > 4:
                        self.vars["WorkingCoordinateOffsetA"] = float(word[4])
                    if len(word) > 5:
                        self.vars["WorkingCoordinateOffsetB"] = float(word[5])
                    if len(word) > 6:
                        self.vars["WorkingCoordinateOffsetC"] = float(word[6])
                except (ValueError, IndexError):
                    self.vars["State"] = f"Garbage receive {word[0]}: {line}"
                    self.log_msg(self.vars["State"])
                    break
            elif word[0] == "Pn":
                try:
                    # Possible pins:
                    # X Y Z XYZ limit pins, respectively
                    # P the probe pin.
                    # D H R S the door, hold, soft-reset, and cycle-start pins, respectively.
                    # Example: Pn:PZ indicates the probe and z-limit pins are 'triggered'.
                    # Note: A may be added in later versions for an A-axis limit pin.
                    self.vars["Pins"] = word[1]
                except (ValueError, IndexError):
                    break

    def parseBracketSquare(self, line):
        word = SPLITPAT.split(line[1:-1])
        if word[0] == "PRB":
            self.vars["ProbeX"] = float(word[1])
            self.vars["ProbeY"] = float(word[2])
            self.vars["ProbeZ"] = float(word[3])
            self._probe_update = True
            self.vars[word[0]] = word[1:]
        if word[0] == "G92":
            self.vars["G92X"] = float(word[1])
            self.vars["G92Y"] = float(word[2])
            self.vars["G92Z"] = float(word[3])
            if len(word) > 4:
                self.vars["G92A"] = float(word[4])
            if len(word) > 5:
                self.vars["G92B"] = float(word[5])
            if len(word) > 6:
                self.vars["G92C"] = float(word[6])
            self.vars[word[0]] = word[1:]
            self._g_update = True
        if word[0] == "G28":
            self.vars["G28X"] = float(word[1])
            self.vars["G28Y"] = float(word[2])
            self.vars["G28Z"] = float(word[3])
            self.vars[word[0]] = word[1:]
            self._g_update = True
        if word[0] == "G30":
            self.vars["G30X"] = float(word[1])
            self.vars["G30Y"] = float(word[2])
            self.vars["G30Z"] = float(word[3])
            self.vars[word[0]] = word[1:]
            self._g_update = True
        elif word[0] == "GC":
            self.vars["G"] = word[1].split()
            self.updateG()
            self._g_update = True
        elif word[0] == "TLO":
            self.vars[word[0]] = word[1]
            self._probe_update = True
            self._g_update = True
        else:
            self.vars[word[0]] = word[1:]


# test_strings = [
#     "<Idle|MPos:0.000,0.000,0.000|FS:0,0|Pn:P|WCO:0.000,0.000,0.000>\n",
#     "<Idle|MPos:1.000,0.000,0.000|FS:0,0|Pn:P>\n",
#     "<Idle|MPos:0.000,0.000,0.000|FS:0,0|Pn:P|Ov:100,100,100>\n",
#     "<Hold:0|MPos:0.000,0.000,0.000|FS:0,0|Pn:P|WCO:0.000,0.000,0.000>\n",
#     "<Run|MPos:1.788,0.000,0.000|FS:0,0|Pn:P|Ov:100,100,100>\n",
#     "<Run|MPos:11.000,12.600,0.000|FS:1585,0|Pn:P>\n",
# ]

# parser = GRBLParser()

# for i in test_strings:
#     print("[]Parsing {}".format(i))
#     parser.parseBracketAngle(i)
#     print(parser.vars)
