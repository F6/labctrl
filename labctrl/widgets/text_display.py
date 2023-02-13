# -*- coding: utf-8 -*-

"""
text_display.py:

This module implements text display widget bundles for components and apps.

20230213: init release
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20230213"

from abc import ABC, abstractmethod
from typing import Union, NewType, Any
from functools import partial
from bokeh.models.widgets import PreText as BokehPreText
from tornado import gen
from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat
from .generic import GenericTextDisplay

class AbstractBundleTextDisplay(ABC):
    """
    [TODO]: implement abstract class as a base class for bundles. For now only bokeh bundles are used so 
            temporarily leave it here (unused).
    """
    text_display:     Union[GenericTextDisplay, BokehPreText]

    @abstractmethod
    def update(self, new_text, lstat: LabStat):
        pass


class FactoryTextDisplay:
    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat

    
    def generate_bundle(self, bundle_config: dict):
        config: dict = bundle_config["Config"]
        text_display_type: str = config["Type"]
        if text_display_type == "PreText":
            return self.generate_bundle_pre_text(config)
        # elif text_display_type == "Div":
        #     return self.generate_bundle_div(config)
        else:
            raise ValueError(
                "Unknown text display type to generate: {}".format(text_display_type))

    def generate_bundle_pre_text(self, config: dict):
        return BundlePreText()


class BundlePreText(AbstractBundleTextDisplay):
    def __init__(self) -> None:
        self.text_display = BokehPreText(text="")

    @gen.coroutine
    def callback_update(self, new_text):
        self.text_display.text = new_text

    def update(self, new_text, lstat: LabStat):
        lstat.doc.add_next_tick_callback(partial(self.callback_update, new_text))

