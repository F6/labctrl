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
    # ast.BitXor: op.xor,
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