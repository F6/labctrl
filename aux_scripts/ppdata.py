import numpy as np
target = 'Oh-570-Round29-Nonenm'
rounds = 30
sigbgfile = 'bg-Round49-Nonenm-Sum-Signal.csv'
bgrounds = 50
refbgfile = 'bg-Round49-Nonenm-Sum-Reference.csv'

sig = np.loadtxt(target + '-Sum-Signal.csv', delimiter=',')
ref = np.loadtxt(target + '-Sum-Reference.csv', delimiter=',')
sigbg = np.loadtxt(sigbgfile, delimiter=',')
refbg = np.loadtxt(refbgfile, delimiter=',')
sigbg = sigbg/bgrounds
refbg = refbg/bgrounds
sig = sig - sigbg * rounds
ref = ref - refbg * rounds
s = sig/ref
od = -np.log10(s)
od = od.transpose()
dod = np.zeros(od.shape)
for i, line in enumerate(od):
    dod[i,:] = od[i,:] - np.sum(od[i,-5:-1])/4

dod = dod.transpose()

np.savetxt('result.csv', dod, delimiter=',')