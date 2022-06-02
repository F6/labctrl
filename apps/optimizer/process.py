import numpy as np

np.savetxt('data.txt',np.array([[float(i.split()[1]) for i in l[j].split('\n')[1:-1]] for j in range(len(l))]))

np.savetxt('wl.txt', np.array([float(i.split()[0]) for i in l[0].split('\n')[1:-1]]))