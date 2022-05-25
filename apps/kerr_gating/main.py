# -*- coding: utf-8 -*-

"""main.py:
This module implements the
Kerr Gating Time-resolved Photoluminescence Spectroscopy
technic

The balanced Kerr gate spectroscopy can measure the ultrafast dynamics
of light emission from molecules with very weak fluorescence or phosphorescence,
for example the fluorescence from 2-dimensional materials, ACQ systems
or single molecule systems.

In such experiments, an ultrafast laser pulse excites the sample to
higher electronic excited states, then the fluorescence and
phosphorescence from the decay of the electronic excited
states are collected with reflective objectives, then sent into a 
Kerr gate and detected with balanced detector. A chopper chops the
excitation pulse train into 50% duty cycle, the sync TTL of the chopper
and the balanced signal are sent into a boxcar averager to recover 
the lifetime signal by shot-to-shot subtraction of backgrounds.
Another synchronized beam of ultrafast laser pulse and a delay 
line is used to set the opening time window of the Kerr gate. 

Reflective objectives are prefered over regular microscope objectives
because this type of objective introduces minimum distortion of
wavepacket-front in the geometric space, which will significantly decrease 
the Kerr gating efficiency and make it hard to detect the already weak
signal.

For single wavelength TRPL measurements, a notch filter is inserted
before the detector. For multi wavelength measurements, typically an array
of notch filter is used. Note that the instrument introduces dispersion
to the original signal, so dispersion correction from standard samples
must be applied for multi-wavelength time zeros.

the Zurich Instruments UHF is used as the boxcar integrator.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"


import time

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.methods.kerr_gating import FactoryKerrGating
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.ziUHF.factory import FactoryZiUHF
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview

doc.template_variables["app_name"] = "kerr_gating"

factory = FactoryLinearStage()
linear_stage = factory.generate_bundle("AeroTech_NView", lcfg, lstat)

factory = FactoryZiUHF()
ziUHF = factory.generate_bundle(lcfg, lstat)

factory = FactoryKerrGating()
kerrgate = factory.generate(
    linear_stage, ziUHF, lcfg, lstat)

# roots: ["dashboard", "setup", "params", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here

dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

foo = column(
    linear_stage.scan_mode,
    linear_stage.scan_zero,
    linear_stage.scan_start,
    linear_stage.scan_stop,
    linear_stage.scan_step,
    linear_stage.scan_file
)
param_tab1 = Panel(child=foo, title="Linear Stage")
param_tabs = Tabs(tabs=[param_tab1], name="param")
doc.add_root(param_tabs)

foo = column(
    linear_stage.test_online,
    linear_stage.manual_position,
    linear_stage.manual_move,
    linear_stage.manual_step,
    linear_stage.manual_step_forward,
    linear_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Linear Stage")
foo = column(
    ziUHF.test_online,
    ziUHF.manual_take_sample,
)
manual_tab2 = Panel(child=foo, title="ziUHF")
# manual_tab2.disabled = True
manual_tabs = Tabs(tabs=[manual_tab1, manual_tab2], name="manual")
doc.add_root(manual_tabs)

foo = column(
    kerrgate.generic.filestem,
    kerrgate.generic.scanrounds,
    kerrgate.start,
    kerrgate.terminate
)
schedule_tab1 = Panel(child=foo, title="Kerr Gate")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)

foo = column(
    kerrgate.preview.signal.fig
)
reports_tab1 = Panel(child=foo, title="Kerr Gate")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)