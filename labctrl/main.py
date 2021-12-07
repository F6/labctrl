# -*- coding: utf-8 -*-

"""main.py:

"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"


import time

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labconfig import lcfg
from labstat import lstat


from methods.kerr_gating import FactoryKerrGating
from components.linear_stages.factory import FactoryLinearStage
from components.ziUHF.factory import FactoryZiUHF

from main_doc import doc

from dashboard import taskoverview

factory = FactoryLinearStage()
AeroTech_NView = factory.generate_bundle(
    lcfg.config["linear_stages"]["AeroTech_NView"], lcfg, lstat)
AeroTech_THz = factory.generate_bundle(
    lcfg.config["linear_stages"]["AeroTech_THz"], lcfg, lstat)
cdhd2 = factory.generate_bundle(
    lcfg.config["linear_stages"]["CDHD2"], lcfg, lstat)
crd507 = factory.generate_bundle(
    lcfg.config["linear_stages"]["CRD507"], lcfg, lstat)
pmc48mt6 = factory.generate_bundle(
    lcfg.config["linear_stages"]["PMC48MT6"], lcfg, lstat)
usb1020 = factory.generate_bundle(
    lcfg.config["linear_stages"]["USB1020"], lcfg, lstat)

linear_stages = [
    AeroTech_NView,
    AeroTech_THz,
    cdhd2,
    crd507,
    pmc48mt6,
    usb1020,
]

factory = FactoryZiUHF()
ziUHF = factory.generate_bundle(lcfg, lstat)

factory = FactoryKerrGating()
kerrgate = factory.generate(
    AeroTech_NView, ziUHF, lcfg, lstat)

# roots: ["dashboard", "setup", "params", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here

dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

foo = column(
    AeroTech_NView.scan_mode,
    AeroTech_NView.scan_zero,
    AeroTech_NView.scan_start,
    AeroTech_NView.scan_stop,
    AeroTech_NView.scan_step,
    AeroTech_NView.scan_file
)
param_tab1 = Panel(child=foo, title="AeroTech_NView")
param_tabs = Tabs(tabs=[param_tab1], name="param")
doc.add_root(param_tabs)

foo = column(
    AeroTech_NView.test_online,
    AeroTech_NView.manual_position,
    AeroTech_NView.manual_move,
    AeroTech_NView.manual_step,
    AeroTech_NView.manual_step_forward,
    AeroTech_NView.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="AeroTech_NView")
foo = column(
    ziUHF.test_online,
    ziUHF.manual_take_sample,
)
manual_tab2 = Panel(child=foo, title="ziUHF")
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