
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
print(requests.get(grbl1_base_address + "g/G1 F500").content)

print(requests.get(grbl2_base_address + "g/G90").content)
print(requests.get(grbl2_base_address + "g/G1 F500").content)

def moveabs_M1(x, y):
    res = requests.get(grbl1_base_address + "g1blocking/G1 X{} Y{}".format(x, y)).content
    # print(res)

def moveabs_M2(x, y):
    res = requests.get(grbl2_base_address + "g1blocking/G1 X{} Y{}".format(x, y)).content
    # print(res)

def moveabs(a, b, c, d):
    moveabs_M1(a, b)
    moveabs_M2(c, d)


# initguess = [0.2147907173738313, -0.2092306954879298, 0.13158698787337775, 0.26677054078212065]
initguess = [0.07914668173847993, -0.32792221234184266, -0.05515883392478764, 0.18699888291033503]
moveabs(*initguess)
time.sleep(1)
sample_size = 50
step_max = 0.05
n_steps = 100
# init
print("Init Value")
prev_val = get_sample(sample_size)
prev_point = initguess
now_point = [0.0, 0.0, 0.0, 0.0]
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
            if valid_val > now_val:
                print("False Positive! ", valid_val, now_val, prev_val)
            else:
                print("Step Accepted!", valid_val, now_val, prev_val)
                for j in range(4):
                    prev_point[j] = now_point[j]
                prev_val = now_val
                print("Next Point:", now_point)
    moveabs(*prev_point)
except KeyboardInterrupt:
    print("Keyboard Interrupt!")
    moveabs(*prev_point)

