import requests

def ignore_connection_error(func):
    def ret():
        try:
            func()
        except requests.exceptions.ConnectionError as e:
            print("Connection failed")
    return ret
