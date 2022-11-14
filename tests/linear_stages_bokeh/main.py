# -*- coding: utf-8 -*-

"""main.py:
This is a simple test for linear stage widgets generated with bokeh library.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221113"


import time
import numpy as np

from functools import partial
from threading import Thread

from scipy.fft import fft, fftfreq, fftshift

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div, TextInput, PreText
from bokeh.models import Panel, Tabs
from tornado import gen

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.cameras.factory import FactoryCamera
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.methods.figure import FactoryFigure1D, FactoryImageRGBA

app_name = "linear_stages_bokeh"
doc.template_variables["app_name"] = app_name

app_config = lcfg.config["tests"][app_name]

delay_stage = app_config["LinearStageUnderTesting"]


class LinearStagesBokehWidgetTester:
    def __init__(self) -> None:
        self.linear_stage_config = lcfg.config["linear_stages"][delay_stage]
        factory = FactoryLinearStage(lcfg, lstat)
        linear_stage_bundle_config = dict()
        linear_stage_bundle_config["Config"] = self.linear_stage_config
        self.delay_stage = factory.generate_bundle(linear_stage_bundle_config)
        self.start = Button(label="Start Range Scan", button_type="success")
        self.terminate = Button(label="Terminate Range Scan", button_type="warning")

tester = LinearStagesBokehWidgetTester()

foo = column(
    # basic config
    Div(text="Stage Under Test: {}".format(tester.linear_stage_config["Name"])),
    tester.delay_stage.host,
    tester.delay_stage.port,
    tester.delay_stage.multiples,
    tester.delay_stage.working_direction,
    Div(text="Position and Limitation Unit:"),
    tester.delay_stage.position_unit,
    tester.delay_stage.zero_delay_absolute_position,
    tester.delay_stage.soft_limit_min,
    tester.delay_stage.soft_limit_max,
    tester.delay_stage.driving_speed,
    tester.delay_stage.driving_speed_unit,
    tester.delay_stage.driving_acceleration,
    tester.delay_stage.driving_acceleration_unit,
)
foo2 = column(
    # exp params
    Div(text="Range Scan Param Settings:"),
    tester.delay_stage.scan_mode,
    tester.delay_stage.working_unit,
    tester.delay_stage.range_scan_start,
    tester.delay_stage.range_scan_stop,
    tester.delay_stage.range_scan_step,
    tester.delay_stage.external_scan_list_file,
    # schedule
    tester.start,
    tester.terminate,
)
foo3 = column(
    # manual
    Div(text="Manual Operations:"),
    tester.delay_stage.test_online,
    Div(text="Manual Operation Unit:"),
    tester.delay_stage.manual_unit,
    tester.delay_stage.manual_position,
    tester.delay_stage.manual_move,
    tester.delay_stage.manual_step,
    tester.delay_stage.manual_step_forward,
    tester.delay_stage.manual_step_backward,
)

bar = row(foo, foo2, foo3)
p = Panel(child=bar, title="Linear Stage Under Test")
t = Tabs(tabs=[p], name="dashboard")

doc.add_root(t)
