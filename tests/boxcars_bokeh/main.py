# -*- coding: utf-8 -*-

"""main.py:
This is a simple test for boxcar widgets generated with bokeh library.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221124"


from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.main_doc import doc
from labctrl.components.lockin_and_boxcars.factory import FactoryBoxcar


app_name = "boxcars_bokeh"
doc.template_variables["app_name"] = app_name
app_config = lcfg.config["tests"][app_name]
boxcar_name = app_config["BoxcarUnderTesting"]


class BoxcarBokehWidgetTester:
    def __init__(self) -> None:
        self.config = lcfg.config["lockin_and_boxcars"][boxcar_name]
        factory = FactoryBoxcar(lcfg, lstat)
        boxcar_bundle_config = dict()
        boxcar_bundle_config["BundleType"] = "Bokeh"
        boxcar_bundle_config["Config"] = self.config
        self.boxcar_bundle = factory.generate_bundle(boxcar_bundle_config)


tester = BoxcarBokehWidgetTester()


# region basic
foo1 = column(
    # basic config
    Div(text="<b>Boxcar Under Test: {}</b>".format(
        tester.config["Name"])),
    tester.boxcar_bundle.host,
    tester.boxcar_bundle.port,
    tester.boxcar_bundle.test_online,
    Div(text="Boxcar Working Unit:"),
    tester.boxcar_bundle.working_unit,
    tester.boxcar_bundle.delay_background_sampling,
    tester.boxcar_bundle.delay_integrate,
    tester.boxcar_bundle.delay_hold,
    tester.boxcar_bundle.delay_signal_sampling,
    tester.boxcar_bundle.delay_reset,
    tester.boxcar_bundle.submit_config,
    Div(text="Boxcar Working Mode:"),
    tester.boxcar_bundle.working_mode,
    tester.boxcar_bundle.set_working_mode,
    tester.boxcar_bundle.manual_get_boxcar_data,
    tester.boxcar_bundle.manual_get_PWA_data,
    tester.boxcar_bundle.start_PWA,
    tester.boxcar_bundle.stop_PWA
)
foo0 = column(
    tester.boxcar_bundle.boxcar_preview.figure,
    tester.boxcar_bundle.PWA_figure.figure
)
foooo = row(foo0, foo1)
bar0 = Panel(child=foooo, title="Boxcar")
# endregion basic

t = Tabs(tabs=[bar0], name="dashboard")

doc.add_root(t)
# Experiment Message
doc.add_root(lstat.pre_exp_msg)
