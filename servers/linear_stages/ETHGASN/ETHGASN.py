import ctypes
from ctypes import Structure, c_double, c_short
import time
from MultiCard import TrapPrm

gas = ctypes.CDLL("GAS.dll")


class Axis:
    def __init__(self, axis_i, pulse_per_mm, velocity) -> None:
        self.axis_i = axis_i
        self.pulse_per_mm = pulse_per_mm
        self.pos = 0 # TEMPORARY! fix this
        self.vel = velocity
        print("Setting up axis {}".format(self.axis_i))
        self.enable()
        self.setvel(velocity)
        self.setparam()

    def enable(self):
        print("Enabling Axis {}...".format(self.axis_i))
        res = 0
        res += gas.GA_AxisOn(self.axis_i)
        return res
    
    def diasble(self):
        print("Disabling Axis {}...".format(self.axis_i))
        res = 0
        res += gas.GA_AxisOff(self.axis_i)
        return res

    def setvel(self, vel):
        vel = float(vel)
        print("Setting axis {} velocity to {} pulses per ms".format(self.axis_i, vel))
        res = 0
        self.vel = vel
        res += gas.GA_SetVel(1, c_double(vel))
        return res

    def setparam(self, acceleration=1.0, deceleration=1.0, velocity_start=0, smooth_time=0):        
        print("Setting up Axis {} params...".format(self.axis_i))
        res = 0
        res += gas.GA_PrfTrap(self.axis_i)
        self.tpm = TrapPrm()
        self.tpm.acc = acceleration
        self.tpm.dec = deceleration
        self.tpm.velStart = velocity_start
        self.tpm.smoothTime = smooth_time
        res += gas.GA_SetTrapPrm(self.axis_i, self.tpm)
        return res
        # print("Return Code: ", res)

    def setpos(self, pos):
        delta = self.pos - pos
        self.pos = pos
        res = 0
        res += gas.GA_SetPos(self.axis_i, pos)
        res += gas.GA_Update(0xFF)
        print("Moving, ETHGASN Return: ", res)
        tts = abs(delta/(self.vel * 1000))
        time.sleep(tts)

    def moveabs(self, pos):
        pos = float(pos)
        tpos = int(pos * self.pulse_per_mm)
        self.setpos(tpos)

    def autohome(self):
        self.setpos(0)
    



class ETHGASN:
    def __init__(self) -> None:
        self.ip = '192.168.0.1'
        print("Opening ETHGASN Card...")
        res = 0
        res += gas.GA_SetCardNo(1)
        res += gas.GA_Open(0, self.ip)

        print("Return Code: ", res)
        
        """The yaskawa controller and linear stage on axis 1. 3200 pulses per mm (measured with ruler)"""
        self.yaskawa = Axis(1, 3200, 200)
        """The leadscrew linear stage, connected to LeiSai driver, 640 pulses per mm (measured with ruler)"""
        self.leisai = Axis(4, 640, 200)

        self.linear_stages = [self.yaskawa, self.leisai]


    def reset(self):
        print("Resetting controller! All stored position info will be lost!")
        res = 0
        res += gas.GA_Reset()
        return res





controller = ETHGASN()
# for i in range(3):
#     stage.setpos(1000)
#     stage.setpos(0)