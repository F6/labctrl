from threading import Thread

from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
import TLPM
import time
import serial
import sys

M1 = serial.Serial("COM5", baudrate=115200, timeout=1)
M2 = serial.Serial("COM6", baudrate=115200, timeout=1)


def get_status_M1():
    M1.write('?\n'.encode())
    s = M1.readline()
    while len(s) < 10:
        time.sleep(0.1)
        M1.write('?\n'.encode())
        s = M1.readline()
    status = parse_status(s)
    return status 

def get_status_M2():
    M2.write('?\n'.encode())
    s = M2.readline()
    while len(s) < 10:
        time.sleep(0.1)
        M2.write('?\n'.encode())
        s = M2.readline()
    status = parse_status(s)
    return status 

def setM1pos(x, y):
    M1.write("G1 F500 X{} Y{}".format(x, y).encode())
    M1.readline()
    while True:
        time.sleep(0.1)
        s = get_status_M1()
        myd.at = s['pos'][0]
        myd.bt = s['pos'][1]
        if s['status'] == 'Idle':
            break

def setM2pos(x, y):
    M2.write("G1 F500 X{} Y{}".format(x, y).encode())
    M2.readline()
    while True:
        time.sleep(0.1)
        s = get_status_M2()
        myd.ct = s['pos'][0]
        myd.dt = s['pos'][1]
        if s['status'] == 'Idle':
            break



tlPM = TLPM.TLPM()
deviceCount = c_uint32()
tlPM.findRsrc(byref(deviceCount))

print("devices found: " + str(deviceCount.value))

resourceName = create_string_buffer(1024)

for i in range(0, deviceCount.value):
    tlPM.getRsrcName(c_int(i), resourceName)
    print(c_char_p(resourceName.raw).value)
    break

tlPM.close()

tlPM = TLPM.TLPM()
#resourceName = create_string_buffer(b"COM1::115200")
#print(c_char_p(resourceName.raw).value)
tlPM.open(resourceName, c_bool(True), c_bool(True))

message = create_string_buffer(1024)
tlPM.getCalibrationMsg(message)
print(c_char_p(message.raw).value)

tlPM.setWavelength(c_double(400.0))
tlPM.setCurrentRange(c_double(0.2))
tlPM.setCurrentAutoRange(TLPM.TLPM_AUTORANGE_CURRENT_OFF)

time.sleep(3)

def parse_status(s):
    try:
        s = s.decode()
        # print(s)
        sys.stdout.flush()
        s1 = s.strip()
        s2 = s1[1:-1]
        s3 = s2.split('|')
        d = dict()
        d["status"] = s3[0]
        pos = s3[1]
        pos = pos[5:]
        pos = pos.split(',')
        pos = list(map(float, pos))
        d["pos"] = pos
        return d
    except Exception as e:
        print(s)
        raise Exception




class MyData:
    def __init__(self) -> None:
        self.data = 0.00
        self.max = 0.00
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.at = 0
        self.bt = 0
        self.ct = 0
        self.dt = 0
        self.halt = False

myd = MyData()

def reading_task():
    while not myd.halt:
        try:
            power = c_double()
            tlPM.measPower(byref(power))
            # print(power.value)
            myd.data = power.value
            if myd.data > myd.max:
                max_handler()
            time.sleep(0.01)
            # print(myd.data)
        except NameError as e:
            print(e, e.args)
            tlPM.open(resourceName, c_bool(True), c_bool(True))            
            tlPM.setWavelength(c_double(400.0))
            tlPM.setCurrentRange(c_double(0.2))
            tlPM.setCurrentAutoRange(TLPM.TLPM_AUTORANGE_CURRENT_OFF)


def max_handler():
    myd.max = myd.data
    myd.a = myd.at
    myd.b = myd.bt
    myd.c = myd.ct
    myd.d = myd.dt
    print(myd.a, myd.b, myd.c, myd.d, myd.max)
    sys.stdout.flush()

data_thread = Thread(target=reading_task)
data_thread.start()

arange = (-50, 50)
brange = (-50, 50)
crange = (-50, 50)
drange = (-50, 50)


# setM1pos(0, 0)
# setM2pos(-10, 27)

SR = 10

for i in range(1):
    # move M1 axis 1
    print("Scan M1 A")
    sys.stdout.flush()
    setM1pos(SR, myd.b)
    setM1pos(myd.a, myd.b)
    time.sleep(2)
    print("Scan M1 B")
    sys.stdout.flush()
    setM1pos(myd.a, SR)
    setM1pos(myd.a, myd.b)
    time.sleep(2)
    print("Scan M2 C")
    sys.stdout.flush()
    setM2pos(SR, myd.d)
    setM2pos(myd.c, myd.d)
    time.sleep(2)
    print("Scan M2 D")
    sys.stdout.flush()
    setM2pos(myd.c, SR)
    setM2pos(myd.c, myd.d)
    time.sleep(2)
    print("Scan M1 A Rev")
    sys.stdout.flush()
    setM1pos(-SR, myd.b)
    setM1pos(myd.a, myd.b)
    time.sleep(2)
    print("Scan M1 B Rev")
    sys.stdout.flush()
    setM1pos(myd.a, -SR)
    setM1pos(myd.a, myd.b)
    time.sleep(2)
    print("Scan M2 C Rev")
    sys.stdout.flush()
    setM2pos(-SR, myd.d)
    setM2pos(myd.c, myd.d)
    time.sleep(2)
    print("Scan M2 D Rev")
    sys.stdout.flush()
    setM2pos(myd.c, -SR)
    setM2pos(myd.c, myd.d)
    time.sleep(2)

# time.sleep(60)
myd.halt = True

tlPM.close()

print('End program')
