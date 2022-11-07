import requests


def ps_to_mm(ps:float) -> float:
    """v = 1.0003 in air, so
    speed of light = 299,702,547 meters per second in air.
    For a retroreflector delay line setup, the light travels
    forth and back so the optical path difference is twice
    the distance traveled by mirror, thus the division by 2
    """
    return ps*0.299702547*0.5


def mm_to_ps(mm:float) -> float:
    """the above function reversed"""
    return 2*mm/0.299702547


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
