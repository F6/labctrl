
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
    r = requests.get(pm400_base_address + "getSample/20")
    j = json.loads(r.content)
    sample = np.frombuffer(base64.b64decode(j['sample']), dtype=np.float64)
    return sample, j['average'], j['sample standard deviation']


nsp = 40

scanlist = np.linspace(-10, 10, nsp)

scandata = np.zeros((nsp, nsp))

print(requests.get(grbl1_base_address + "g/G90").content)

for i in range(len(scanlist)):
    for j in range(len(scanlist)):
        print(requests.get(grbl1_base_address + "g1blocking/G1 X{} Y{}".format(scanlist[i], scanlist[j])).content)
        res, average, stddev = get_sample()
        print(res, average, stddev)
        scandata[i, j] = average


np.savetxt('data.txt', scandata)
np.savetxt('scanlist.txt', scanlist)


fig, ax = plt.subplots(constrained_layout=True)
X, Y = np.meshgrid(scanlist, scanlist)
CS = ax.contourf(X, Y, np.transpose(scandata), 64, cmap=plt.cm.bone, origin='lower')
# add lines
CS2 = ax.contour(CS, levels=CS.levels[::16], colors='r', origin='lower')

ax.set_title('Optimize Scan Raw')
ax.set_xlabel('Axis 1 Offset')
ax.set_ylabel('Axis 2 Offset')
# ax.set_xlim(-100, 100)
# ax.set_ylim(400, 420)

# Make a colorbar for the ContourSet returned by the contourf call.
cbar = fig.colorbar(CS)
cbar.ax.set_ylabel('Intensity')

plt.show()