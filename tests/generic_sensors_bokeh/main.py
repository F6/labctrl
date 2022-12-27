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
from labctrl.components.generic_sensors.factory import FactorySensor


app_name = "generic_sensors_bokeh"
doc.template_variables["app_name"] = app_name
app_config = lcfg.config["tests"][app_name]
sensor_name = app_config["UnderTesting"]


class GenericSensorBokehWidgetTester:
    def __init__(self) -> None:
        self.config = lcfg.config["generic_sensors"][sensor_name]
        factory = FactorySensor(lcfg, lstat)
        bundle_config = dict()
        bundle_config["BundleType"] = "Bokeh"
        bundle_config["Config"] = self.config
        self.bundle = factory.generate_bundle(bundle_config)


tester = GenericSensorBokehWidgetTester()


# region basic
foo1 = column(
    # basic config
    Div(text="<b>Sensor Under Test: {}</b>".format(
        tester.config["Name"])),
    tester.bundle.host,
    tester.bundle.port,
    tester.bundle.test_online,
    tester.bundle.sensor_config_file,
    tester.bundle.submit_config,
    tester.bundle.manually_retrive_data,
    tester.bundle.start_retrive_data,
    tester.bundle.stop_retrive_data
)

bar0 = Panel(child=foo1, title="Sensors")
# endregion basic

t = Tabs(tabs=[bar0], name="dashboard")

doc.add_root(t)
# Experiment Message
doc.add_root(lstat.pre_exp_msg)
