import requests
from functools import wraps


def ignore_connection_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            print("Connection failed")
    return wrapper

def eval_float(f):
    try:
        f = float(f)
        return f
    except Exception as e:
        print("Non-float number inputed")
        return 0.0
