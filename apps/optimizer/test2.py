
import requests
import numpy as np
import json
import base64
import sys
import matplotlib.pyplot as plt
import random
import time

pm400_base_address = "http://127.0.0.1:5029/"
grbl1_base_address = "http://127.0.0.1:5049/"
grbl2_base_address = "http://127.0.0.1:5050/"


def get_sample(n):
    """Get data from PM400"""
    r = requests.get(pm400_base_address + "getSample/{}".format(n))
    j = json.loads(r.content)
    sample = np.frombuffer(base64.b64decode(j['sample']), dtype=np.float64)
    return j["median"]
    # return sample, j['average'], j['sample standard deviation']


print(requests.get(grbl1_base_address + "g/G90").content)
print(requests.get(grbl1_base_address + "g/G1 F1000").content)

print(requests.get(grbl2_base_address + "g/G90").content)
print(requests.get(grbl2_base_address + "g/G1 F1000").content)

def moveabs_M1(x, y):
    res = requests.get(grbl1_base_address + "g1blocking/G1 X{} Y{}".format(x, y)).content
    # print(res)

def moveabs_M2(x, y):
    res = requests.get(grbl2_base_address + "g1blocking/G1 X{} Y{}".format(x, y)).content
    # print(res)

def moveabs(a, b, c, d):
    moveabs_M1(-3, -3)
    moveabs_M2(-3, -3)
    moveabs_M1(a, b)    
    moveabs_M2(c, d)

# initguess = [0, 0, 0, 0]
# initguess = [-0.1, 0, 0, 0]
# initguess = [0, 0, 0.1, 0]
initguess = [0.05275255410666818, -0.09692879939291221, 0.05748747102072012, -0.1698501372961476]
# initguess = [-0.08190694210531461, -0.20615079837464811, -0.08383404927495994, -0.022710019452864293]
# initguess = [-0.05212043258230441, -0.16081564061736503, -0.0913586483754273, 0.01072877412515754]
moveabs(*initguess)
time.sleep(1)
sample_size = 40
step_max = 0.1
n_steps = 100
# init
print("Init Value")
prev_val = get_sample(sample_size)
prev_point = initguess
now_point = [0.0, 0.0, 0.0, 0.0]
valid_threshold = 0.000010
try:
    for i in range(n_steps):        
        for j in range(4):
            now_point[j] = prev_point[j] + step_max * (random.random()-0.5) * 2
        moveabs(*now_point)
        print("Try Point:", now_point)
        now_val = get_sample(sample_size)
        if now_val < prev_val:
            print("Step Rejected! ", now_val, prev_val)
        else:
            print("Suspect! ", now_val, prev_val)
            moveabs(*prev_point)
            valid_val = get_sample(sample_size)
            if valid_val - now_val > - valid_threshold:
                print("False Positive! ", valid_val, now_val, prev_val)
            else:
                print("Step Accepted!", valid_val, now_val, prev_val)
                for j in range(4):
                    prev_point[j] = now_point[j]
                prev_val = now_val
                print("Next Point:", now_point)
    print("Best Point: ", prev_point)
    moveabs(*prev_point)
except KeyboardInterrupt:
    print("Keyboard Interrupt! Best Point: ", prev_point)
    moveabs(*prev_point)

