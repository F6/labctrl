import re
import os
import numpy as np

m = re.compile(r'''450-delay-3Sum_(.+)Delay_NoneVis_Delta.csv''')

fs = list()
for i in os.listdir():
    if m.match(i):
        fs.append(i)

fs.sort(key=lambda x: float(m.match(x).groups()[0]))
print('\n'.join(fs))

dl = list()
for i in fs:
    d = np.loadtxt(i, delimiter=',')
    dl.append(d)

dl = np.array(dl)
print(dl)

nl = list()
for i in fs:
    n = float(m.match(i).groups()[0])
    nl.append(n)

nl = np.array(nl)
print(nl)

np.savetxt('Delta.csv', dl, delimiter=',')
np.savetxt('delaylist.csv', nl, delimiter=',')