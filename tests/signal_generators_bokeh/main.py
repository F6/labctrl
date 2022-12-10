# -*- coding: utf-8 -*-

"""main.py:
This is a simple test for signal generator widgets generated with bokeh library.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221117"


from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.main_doc import doc
from labctrl.components.signal_generators.factory import FactorySignalGenerator

from .utils import ignore_connection_error

app_name = "signal_generators_bokeh"
doc.template_variables["app_name"] = app_name
app_config = lcfg.config["tests"][app_name]
signal_generator_name = app_config["SignalGeneratorUnderTesting"]


class SignalGeneratorBokehWidgetTester:
    def __init__(self) -> None:
        self.config = lcfg.config["signal_generators"][signal_generator_name]
        factory = FactorySignalGenerator(lcfg, lstat)
        signal_generator_bundle_config = dict()
        signal_generator_bundle_config["Config"] = self.config
        self.sg_bundle = factory.generate_bundle(signal_generator_bundle_config)


tester = SignalGeneratorBokehWidgetTester()


# region basic
foo1 = column(
    # basic config
    Div(text="<b>Signal Generator Under Test: {}</b>".format(
        tester.config["Name"])),
    tester.sg_bundle.host,
    tester.sg_bundle.port,
    tester.sg_bundle.test_online,
    Div(text="Signal Generator Working Mode:"),
    tester.sg_bundle.working_mode,
    tester.sg_bundle.change_working_mode,
    tester.sg_bundle.waveform_file,
    tester.sg_bundle.update_waveform_button
)
foo0 = column(
    tester.sg_bundle.waveform_figure.figure
)
foooo = row(foo0, foo1)
bar0 = Panel(child=foooo, title="Waveform")
# endregion basic

t = Tabs(tabs=[bar0], name="dashboard")

doc.add_root(t)
# Experiment Message
doc.add_root(lstat.pre_exp_msg)
