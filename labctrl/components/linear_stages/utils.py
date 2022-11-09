import requests


def ps_to_mm(ps:float) -> float:
    """v = 1.0003 in air, so
    speed of light = 299,702,547 meters per second in air.
    For a retroreflector delay line setup, the light travels
    forth and back so the optical path difference is twice
    the distance traveled by mirror, thus the division by 2
    """
    return ps*0.299702547*0.5


def dt_to_mm(dt:float, unit:str, multiples:float, direction:str) -> float:
    """
    accepts dt, returns dx in mm
    v = 1.0003 in air, so
    speed of light = 299,702,547 meters per second in air.
    """
    # convert dt to ps unit
    if unit == "ns":
        dt = dt * 1000
    elif unit == "ps":
        dt = dt
    elif unit == "fs":
        dt = dt / 1000

    dx = dt*0.299702547/multiples
    if direction == "Positive":
        pass
    elif direction == "Negative":
        dx = -dx
    return dx


def mm_to_ps(dx:float, multiples:float) -> float:
    return multiples*dx/0.299702547

def eval_float(f):
    try:
        f = float(f)
        return f
    except Exception as e:
        print("Non-float number inputed")
        return 0.0

def eval_int(i):
    try:
        i = int(i)
        return i
    except Exception as e:
        print("Non-integer number inputed")
        return 0


def ignore_connection_error(func):
    def ret():
        try:
            func()
        except requests.exceptions.ConnectionError as e:
            print("Connection failed")
    return ret
