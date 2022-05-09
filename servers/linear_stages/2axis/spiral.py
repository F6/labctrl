import numpy as np
import matplotlib.pyplot as plt

def rt_xy(r,t):
    x = np.cos(t)*r
    y = np.sin(t)*r
    return x, y

def spiral(theta, pitch=0.1):
    r = theta * pitch
    return r

theta = np.linspace((10*np.pi)**2, (50*np.pi)**2, 1000)
theta2 = np.sqrt(theta)
r = np.zeros(theta.shape)

for i in range(len(theta2)):
    r[i] = spiral(theta2[i])

x = np.zeros(theta.shape)
y = np.zeros(theta.shape)

for i in range(len(theta2)):
    x[i], y[i] = rt_xy(r[i],theta2[i])

x2 = np.zeros(theta.shape)
y2 = np.zeros(theta.shape)
for i in range(len(y)):
    x2[i] = x[-i-1]
    y2[i] = -y[-i-1]

xf = np.concatenate((x, x2))
yf = np.concatenate((y, y2))


# plt.plot(xf, yf, '-')
# plt.show()

s = []

for i in range(len(xf)):
    s.append('G1 X{x:.4f} Y{y:.4f}'.format(x=xf[i], y=yf[i]))

with open('spiral.gcode', 'w') as f:
    f.write('\n'.join(s))