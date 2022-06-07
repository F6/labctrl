import ctypes
from ctypes import Structure, c_double, c_short
import time
from MultiCard import TrapPrm

gas = ctypes.CDLL("GAS.dll")


class ETHGASN:
    def __init__(self) -> None:
        self.pos = 0 # TEMPORARY!!!!! update this
        # self.pulse_per_mm = 640 # For LEISAI leadscrew
        self.pulse_per_mm = 3200
        self.ip = '192.168.0.1'
        print("Opening ETHGASN Card...")
        res = 0
        res += gas.GA_SetCardNo(1)
        res += gas.GA_Open(0, self.ip)
        # res += gas.GA_Reset()
        print("Return Code: ", res)
        print("Enabling Axis 1...")
        res += gas.GA_AxisOn(1)
        print("Return Code: ", res)
        print("Setting up Axis 1 params...")
        res += gas.GA_PrfTrap(1)

        self.tpm = TrapPrm()
        self.tpm.acc = 0.5
        self.tpm.dec = 0.5
        self.tpm.velStart = 0
        self.tpm.smoothTime = 0

        res += gas.GA_SetTrapPrm(1, self.tpm)
        res += gas.GA_SetVel(1, c_double(200.0))

        print("Return Code: ", res)

    def setpos(self, pos):
        delta = self.pos - pos
        self.pos = pos
        res = 0
        # res += gas.GA_SetTrapPrm(1, self.tpm)
        # res += gas.GA_SetVel(1, 10)
        res += gas.GA_SetPos(1, pos)
        res += gas.GA_Update(0xFF)
        print("Moving, ETHGASN Return: ", res)
        tts = abs(delta/(200.0 * 1000))
        time.sleep(tts)
    
    def moveabs(self, pos):
        pos = float(pos)
        tpos = int(pos * self.pulse_per_mm)
        self.setpos(tpos)

    def autohome(self):
        self.setpos(0)


stage = ETHGASN()
# for i in range(3):
#     stage.setpos(1000)
#     stage.setpos(0)