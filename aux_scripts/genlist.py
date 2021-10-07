import numpy as np

a = np.arange(1300, 3501, 2)
a = map(str, a)
b = np.arange(3500, 1299, -2)
b = map(str, b)
s = ' '.join(a) + '\n'  + ' '.join(b)


with open('irlist.txt', 'w') as f:
    f.write(s)
