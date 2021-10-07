# -*- coding: utf-8 -*-

"""singleton.py:
This module provides the singleton metaclass.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


class Singleton(type):
    """Metaclass for singleton class. Although the python standard states 
    that modules are only imported once so instancializing singleton classes
    in a module and importing the instance multiple times should be safe, 
    there is no guarantee that various embedded implementations of python 
    will follow that guideline. This metaclass is used to make sure that
    the singleton class is instancialized once and only once."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
