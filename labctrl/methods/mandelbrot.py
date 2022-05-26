import numpy as np

MAX_ITER = 80

# def calculation range

RE_START = -2
RE_END = 1
IM_START = -1.5
IM_END = 1.5

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n

def mandelbrot_image(width=100, height=100):
    m = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            c = complex(RE_START + (x / width) * (RE_END - RE_START),
                        IM_START + (y / height) * (IM_END - IM_START))
            m[y, x] = mandelbrot(c)
    return m

