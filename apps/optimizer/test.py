
import requests
import numpy as np
import json
import base64
import sys
import matplotlib.pyplot as plt


pm400_base_address = "http://127.0.0.1:5029/"
grbl1_base_address = "http://127.0.0.1:5049/"
grbl2_base_address = "http://127.0.0.1:5050/"


def get_sample():
    """Get data from PM400"""
    r = requests.get(pm400_base_address + "getSample/20")
    j = json.loads(r.content)
    sample = np.frombuffer(base64.b64decode(j['sample']), dtype=np.float64)
    return sample, j['average'], j['sample standard deviation']


print(requests.get(grbl1_base_address + "g/G90").content)
print(requests.get(grbl1_base_address + "g/G1 F500").content)

print(requests.get(grbl2_base_address + "g/G90").content)
print(requests.get(grbl2_base_address + "g/G1 F500").content)

def moveabs_M1(x, y):
    res = requests.get(grbl1_base_address + "g1blocking/G1 X{} Y{}".format(x, y)).content
    print(res)

def moveabs_M2(x, y):
    res = requests.get(grbl2_base_address + "g1blocking/G1 X{} Y{}".format(x, y)).content
    print(res)

def moveabs(a, b, c, d):
    moveabs_M1(a, b)
    moveabs_M2(c, d)



def construct_line(start_point, direction_vector, searchlimit):
    a, b, c, d = start_point
    i, j, k, l = direction_vector
    points = []
    for q in range(-100, 100):
        if searchlimit[0] > i * q or i * q > searchlimit[1]:
            continue
        if searchlimit[0] > j * q or j * q > searchlimit[1]:
            continue
        if searchlimit[0] > k * q or k * q > searchlimit[1]:
            continue
        if searchlimit[0] > l * q or l * q > searchlimit[1]:
            continue
        points.append((a + i * q, b + j * q, c + k * q, d + l * q))
    return points

def linear_search(line):
    vals = np.zeros(len(line), dtype=np.float64)
    for i in range(len(line)):
        a, b, c, d = line[i]
        moveabs(a, b, c, d)
        res, average, stddev = get_sample()
        print(res[0:3], average, stddev)
        vals[i] = average
    return vals

# initguess = (0.28, 0.04, 0.12, 0.14)
# initguess = (0.28, 0.02, 0.12, 0.12000000000000001)
# initguess = (0.405, 0.039999999999999994, 0.12, 0.17500000000000002)
# initguess = (0.38, 0.04500000000000001, 0.095, 0.10500000000000001)

initguess = (0.31000000000000005, 0.21500000000000002, 0.0050000000000000044, -0.035)
spacer = 0.005

directions = [
    (spacer, 0, 0, 0),
    (0, spacer, 0, 0),
    (spacer, 0, spacer, 0),
    (0, -spacer, 0, spacer)
]


searchlimit = (-0.1, 0.1)


print("Init iterate")
line = construct_line(initguess, directions[3], searchlimit)
print(line)
vals = linear_search(line)
max = np.amax(vals)
max_i = np.where(vals == max)[0][0]
print("Init:", max, max_i)
prevmax_p = line[max_i]
globalmax = max
globalmax_p = prevmax_p

try:
    for i in range(5):
        print("Iteration #{}".format(i))
        line = construct_line(prevmax_p, directions[i%4], searchlimit)
        print(line)
        vals = linear_search(line)
        max = np.amax(vals)
        max_i = np.where(vals == max)[0][0]
        print("Iter max, max_i: ", max, max_i)
        prevmax_p = line[max_i]
        if max > globalmax:
            globalmax = max
            globalmax_p = prevmax_p
except KeyboardInterrupt:
    print("Keyboard Interrupted, backing to best yet")

print("Optimize halted. Max find at")
print(globalmax_p)
print("Max value is ", globalmax)
moveabs(*globalmax_p)



# np.savetxt('data.txt', scandata)
# np.savetxt('scanlist.txt', scanlist)


# fig, ax = plt.subplots(constrained_layout=True)
# X, Y = np.meshgrid(scanlist, scanlist)
# CS = ax.contourf(X, Y, np.transpose(scandata), 64, cmap=plt.cm.bone, origin='lower')
# # add lines
# CS2 = ax.contour(CS, levels=CS.levels[::16], colors='r', origin='lower')

# ax.set_title('Optimize Scan Raw')
# ax.set_xlabel('Axis 1 Offset')
# ax.set_ylabel('Axis 2 Offset')
# # ax.set_xlim(-100, 100)
# # ax.set_ylim(400, 420)

# # Make a colorbar for the ContourSet returned by the contourf call.
# cbar = fig.colorbar(CS)
# cbar.ax.set_ylabel('Intensity')

# plt.show()