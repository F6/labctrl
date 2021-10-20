import re
import os
import numpy as np

targets = ['Background', 'IR', 'Delta']
rounds = range(50)


def addspec(round, target):
    m = re.compile('''OMe-1608-delay-3Round{r}_(.+)Delay_NoneVis_{target}.csv'''.format(r=round, target=target))

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

    np.savetxt('Round{r}_{target}.csv'.format(r=round, target=target), dl, delimiter=',')
    np.savetxt('delaylist.csv', nl, delimiter=',')


for t in targets:
    for i in rounds:
        addspec(i,t)



for t in targets:
    d = np.loadtxt('Round{r}_{target}.csv'.format(r=rounds[0], target=t), delimiter=',')
    for i in rounds[1:]:
        d += np.loadtxt('Round{r}_{target}.csv'.format(r=i, target=t), delimiter=',')
    np.savetxt('Sum_{t}.csv'.format(t=t), d, delimiter=',')