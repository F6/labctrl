# -*- coding: utf-8 -*-

"""
utils.py:
auxiliary functions, temporarily collected here, probably moving to other modules later.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221115"

import requests
import ast
import operator as op
import numpy as np


"""
Safely evaluate input formula to float or int, modified from
https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
"""
# supported operators
allowed_operators = {
    ast.Add: op.add, 
    ast.Sub: op.sub, 
    ast.Mult: op.mul,
    ast.Div: op.truediv, 
    # ast.Pow: op.pow, 
    ast.BitXor: op.xor,
    ast.USub: op.neg
}

allowed_names = {
    'pi': np.pi,
    'e': np.e
}

def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)


def eval_(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.Name):
        return allowed_names[node.id]
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return allowed_operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return allowed_operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)


def eval_float(f):
    try:
        f = eval_expr(f)
        f = float(f)
        return f
    except TypeError as e:
        print("Non-float number inputed")
        return 0.0


def eval_int(i):
    try:
        i = eval_expr(i)
        i = int(i)
        return i
    except Exception as e:
        print("Non-integer number inputed")
        return 0


def calculate_dx(dt: float, unit: str, multiples: float, direction: str) -> float:
    """
    accepts dt, returns dx in mm
    v = 1.0003 in air, so
    speed of light = 299,702,547 meters per second in air.
    """
    # coefficient: speed of light in mm/ps
    c = 0.299702547
    # convert dt to ps unit
    if unit == "ns":
        dt = dt * 1000
    elif unit == "ps":
        dt = dt
    elif unit == "fs":
        dt = dt / 1000
    # for optical delay lines, because the laght travels forth and back,
    # the delay stage only needs to move dx/2 to delay the light by dx,
    # so the multiples=0.5 in this case. Some delay stages reuses the delay
    # stage several times, so multiples=0.25, 1/6, 1/8, etc.
    dx = dt * c * multiples

    if direction == "Positive":
        pass
    elif direction == "Negative":
        dx = -dx

    return dx


def ignore_connection_error(func):
    def ret():
        try:
            func()
        except requests.exceptions.ConnectionError as e:
            print("Connection failed")
    return ret
