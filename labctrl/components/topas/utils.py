import requests

def ignore_connection_error(func):
    def ret():
        try:
            func()
        except requests.exceptions.ConnectionError as e:
            print("Connection failed")
    return ret


def eval_float(f):
    try:
        f = float(f)
        return f
    except Exception as e:
        print("Non-float number inputed")
        return 0.0
