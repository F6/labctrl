import unittest

import logging

from logging_helper import TestingLogFormatter


class TestFormatter(unittest.TestCase):
    def test_TestingLogFormatter(self):
        lg = logging.getLogger("TestFormatter.test_TestingLogFormatter")
        lg.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(TestingLogFormatter())
        lg.addHandler(ch)
        lg.debug("This is a debug message.")
        lg.info("This is an info message.")
        lg.warning("This is a warning message.")
        lg.error("This is an error message.")
        lg.critical("This is a critical message.")

if __name__ == '__main__':
    unittest.main()