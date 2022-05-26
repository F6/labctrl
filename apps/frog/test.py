zero = 26.73725

ps = 0.15
fs = ps/1000

import requests
import numpy as np
import json
import base64
import sys
import matplotlib.pyplot as plt


fx_base_address = "http://127.0.0.1:5028/"
linstage_base_address = "http://127.0.0.1:5001/"

requests.get(fx_base_address + "setIntegrationTime/10")
requests.get(fx_base_address + "setAverageTimes/3")
requests.get(fx_base_address + "setBoxcarWidth/1")
# requests.get(fx_base_address + "getspectrum")

def get_spectrum():
    r = requests.get(fx_base_address + "getspectrum")
    j = json.loads(r.content)
    wavelengths = np.frombuffer(base64.b64decode(j['wavelengths']), dtype=np.float64)
    spectrum = np.frombuffer(base64.b64decode(j['spectrum']), dtype=np.float64)
    return wavelengths, spectrum

wavelengths = get_spectrum()[0]

nsp = 40

scanlist = np.linspace(-400, 400, nsp)

frogdata = np.zeros((nsp, len(wavelengths)))

for i in range(len(scanlist)):
    tps = zero - fs * scanlist[i]
    requests.get(linstage_base_address + "moveabs/{tps}".format(tps=tps))
    frogdata[i,:] = get_spectrum()[1]
    print(i, end=',')
    sys.stdout.flush()

np.savetxt('frog.txt', frogdata)
np.savetxt('wavelengths.txt', wavelengths)
np.savetxt('delays.txt', scanlist)


fig, ax = plt.subplots(constrained_layout=True)
X, Y = np.meshgrid(scanlist, wavelengths)
CS = ax.contourf(X, Y, np.transpose(frogdata), 64, cmap=plt.cm.bone, origin='lower')
# add lines
CS2 = ax.contour(CS, levels=CS.levels[::16], colors='r', origin='lower')

ax.set_title('FROG Raw')
ax.set_xlabel('Time Delay (fs)')
ax.set_ylabel('SHG Wavelength (nm)')
ax.set_xlim(-100, 100)
ax.set_ylim(400, 420)

# Make a colorbar for the ContourSet returned by the contourf call.
cbar = fig.colorbar(CS)
cbar.ax.set_ylabel('Intensity')

plt.show()