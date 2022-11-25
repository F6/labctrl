# -*- coding: utf-8 -*-

from __future__ import annotations

"""
interlock.py:

This module provides the abstract class and implementation of an interlock.
The interlock models all contradictions in a component, method or application.

When handling experiments, we probably need to prohibit certain dangerous
or erroneous states to be reached, for example in confocal Raman microscopes,
the preview camera shutter and eyepiece shutter must be closed before 
laser shutter is opened, and they are only allowed to be re-opend after
the laser shutter is closed. If we fail to do it in correct sequence, the
preview camera CMOS and naked eye of human may be damaged from intensive
laser beam. The interlock detects such states before actual action and raises
exceptions for erroneous commands.

Another usage of an interlock is monitoring, for example automatically sending
alarms to other units when humidity or temperature changes significantly, or
when beam quality is deteriorated.

NOTE: Using interlocks does not guarantee safety, because interlocks cannot
magically get information on current states. The interlock relies on inputs
from other functions to determine the current state of the system, if some
new function alters a state without reporting to the interlock, then the 
interlock has no way to know the state has been changed, thus cannot take 
action upon rule violation.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221124"

from abc import ABC, abstractmethod
from typing import Any
from functools import wraps


class InterlockError(Exception):
    def __init__(self, interlock: Interlock,
                 message: str = "Interlock rule violation") -> None:
        self.interlock = interlock
        self.message = message
        self.status = "\n".join(["Rule: {}, Locked: {}".format(i.name, i.locked)
                                for i in self.interlock.rules])
        super().__init__()

    def __str__(self) -> str:
        return "{message}: {status}".format(message=self.message, status=self.status)


class AbstractInterlockRule(ABC):
    name:       str
    interlock:  Interlock
    locked:     bool
    supressed:  bool

    def __init__(self, name: str, interlock: Interlock, ) -> None:
        # name of the rule, e.g. "DisallowBothShutterOpen"
        self.name: str = name
        # the interlock to bind to
        self.interlock: Interlock = interlock
        # rule locked state, if rule check fails, then locked = True
        self.locked: bool = False
        # supressed: if supressed, you can still check the rule,
        # but it can't be locked
        self.supressed: bool = False
        # register at interlock
        self.interlock.add_rule(self)

    @abstractmethod
    def check(self) -> bool:
        """ 
        Pure function, please do not introduce any side effect
        to ensure thread safety.
        Check with self.interlock.states
        """
        pass

    def lock(self):
        if not self.supressed:
            self.interlock.rules_locked.append(self)
            self.locked = True

    def restore(self):
        if self in self.interlock.rules_locked:
            self.interlock.rules_locked.remove(self)
        self.locked = False

    def supress(self):
        self.supressed = True

    def unsupress(self):
        self.supressed = False


class Interlock:
    def __init__(self, states: dict[str, Any]) -> None:
        self.states: dict = states
        self.rules: list[AbstractInterlockRule] = []
        self.rules_locked: list[AbstractInterlockRule] = []

    def add_rule(self, rule: AbstractInterlockRule, new_states: dict[str, str] = dict()):
        """
        Add a new rule to interlock after init. Triggers all rules check
        """
        self.states.update(new_states)
        self.rules.append(rule)
        if self.check_interlock_rules():
            pass
        else:
            raise InterlockError(self)

    def check_interlock_rules(self) -> bool:
        """
        Invokes check method for all rules in this interlock.
        Locks all failed rules.
        Returns True if all rule checks pass.
        Returns False if at least one rule checks fail.
        """
        all_pass: bool = True
        for rule in self.rules:
            check_pass = rule.check()
            if check_pass:
                # print("Interlock check OK for rule {rule}".format(rule=rule.name))
                rule.restore()
            else:
                # print("Interlock check failed for rule {rule}".format(
                #     rule=rule.name))
                rule.lock()
                all_pass = False

        return all_pass

    def interlocked(self, func):
        """
        Decorator. Before function excecution, check all interlock rules.
        If at least one rule fails, then do not execute the function and raise
        interlock error.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.check_interlock_rules():
                func(*args, **kwargs)
            else:
                raise InterlockError(self)
        return wrapper
