import serial
import time

com = 'COM7'

instr_set = dict()
instr_set["Query"] = dict()
instr_set["Set"] = dict()
instr_set["TestComm"] = "$HP\r"
instr_set["Version"] = "$VE\r"
instr_set["Reset"] = "$RE\r"

instr_set["Query"]["IntegrationTime"] = "$PE\r"
instr_set["Set"]["IntegrationTime1ms"] = "$PE1\r"

instr_set["Query"]["Signal"] = "$SP\r"

instr_set["Query"]["ContinuousRead"] = "$SC\r"
instr_set["Set"]["ContinuousReadEnable"] = "$SC1\r"
instr_set["Set"]["ContinuousReadDisable"] = "$SC0\r"

instr_set["Query"]["ContinuousMeasure"] = "$CW\r"
instr_set["Set"]["ContinuousMeasureEnable"] = "$CW1\r"
instr_set["Set"]["ContinuousMeasureDisable"] = "$CW0\r"

instr_set["Oneshot"] = "$MS\r"

instr_set["Query"]["Sensitivity"] = "$VS\r"
instr_set["Set"]["Sensitivity28000"] = "$VS28000\r"


# def it(instr_set):
#     for k in instr_set:
#         if type(instr_set[k]) is not dict:
#             instr_set[k] = instr_set[k].encode('ascii')
#         else:
#             it(instr_set[k])

# def it(instr_set):
for k in instr_set:
    if type(instr_set[k]) is not dict:
        instr_set[k] = instr_set[k].encode('ascii')
    else:
        for k2 in instr_set[k]:
            instr_set[k][k2] = instr_set[k][k2].encode('ascii')

# it(instr_set)

ser = serial.Serial(com, baudrate=115200, timeout=0.1)

ser.write(instr_set["TestComm"])
a = ser.readall().decode()
ser.close()

assert(a == '*\r\n')

def cmd(s):
    ser = serial.Serial(com, baudrate=115200, timeout=0.1)

    ser.write(s)
    a = ser.readline().decode()
    ser.close()

    return a

cmd(instr_set["Reset"])
cmd(instr_set["Set"]["ContinuousMeasureDisable"])
cmd(instr_set["Set"]["Sensitivity28000"])
cmd(instr_set["Set"]["IntegrationTime1ms"])
cmd(instr_set["Oneshot"])
a = cmd(instr_set["Query"]["Signal"])
print(a)

l = []
now = time.time()
for i in range(10):
    cmd(instr_set["Oneshot"])
    a = cmd(instr_set["Query"]["Signal"])
    l.append(a)
    # print(a)
print(l)
final = time.time()

print(now, final, final-now)