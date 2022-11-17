# -*- coding: utf-8 -*-

"""main.py:
This is a simple test for camera widgets generated with bokeh library.
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
from labctrl.components.cameras.factory import FactoryCamera

from .utils import ignore_connection_error

app_name = "cameras_bokeh"
doc.template_variables["app_name"] = app_name
app_config = lcfg.config["tests"][app_name]
camera_name = app_config["CameraUnderTesting"]


class CameraBokehWidgetTester:
    def __init__(self) -> None:
        self.config = lcfg.config["cameras"][camera_name]
        factory = FactoryCamera(lcfg, lstat)
        camera_bundle_config = dict()
        camera_bundle_config["Config"] = self.config
        self.camera_bundle = factory.generate_bundle(camera_bundle_config)


tester = CameraBokehWidgetTester()


# region basic
foo1 = column(
    # basic config
    Div(text="<b>Camera Under Test: {}</b>".format(
        tester.config["Name"])),
    tester.camera_bundle.host,
    tester.camera_bundle.port,
    tester.camera_bundle.test_online,
    Div(text="Camera Working Mode:"),
    tester.camera_bundle.working_mode,
    tester.camera_bundle.change_working_mode,
    tester.camera_bundle.exposure_time,
    tester.camera_bundle.exposure_time_unit,
    tester.camera_bundle.change_exposure_time,
    tester.camera_bundle.apply_all_settings,
    tester.camera_bundle.manual_take_sample,
    tester.camera_bundle.start_continuous_video_streaming,
    tester.camera_bundle.stop_continuous_video_streaming,
)
foo0 = column(
    tester.camera_bundle.preview_figure.figure
)
foooo = row(foo0, foo1)
bar0 = Panel(child=foooo, title="Camera")
# endregion basic

t = Tabs(tabs=[bar0], name="dashboard")

doc.add_root(t)
# Experiment Message
doc.add_root(lstat.pre_exp_msg)
