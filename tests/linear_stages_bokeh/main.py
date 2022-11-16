# -*- coding: utf-8 -*-

"""main.py:
This is a simple test for single axis movement (linear stage) widgets generated with bokeh library.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221116"


from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.main_doc import doc

from .utils import ignore_connection_error

app_name = "linear_stages_bokeh"
doc.template_variables["app_name"] = app_name

app_config = lcfg.config["tests"][app_name]

motion_controller_name = app_config["ControllerUnderTesting"]


class LinearStagesBokehWidgetTester:
    def __init__(self) -> None:
        self.motion_controller_config = lcfg.config["linear_stages"][motion_controller_name]
        factory = FactoryLinearStage(lcfg, lstat)
        motion_controller_bundle_config = dict()
        motion_controller_bundle_config["Config"] = self.motion_controller_config
        self.motion_controller = factory.generate_bundle(
            motion_controller_bundle_config)
        self.start = Button(label="Start Range Scan", button_type="success")
        self.terminate = Button(
            label="Terminate Range Scan", button_type="warning")
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }


tester = LinearStagesBokehWidgetTester()


@tester.motion_controller.scan_range
def range_scan_unit_operation(meta=dict()):
    if tester.flags["TERMINATE"]:
        meta["TERMINATE"] = True
        lstat.expmsg(
            "[ALERT] Range Scan Test operation received signal TERMINATE, trying graceful Thread exit")
        return
    lstat.expmsg(
        "[range_scan_unit_operation] Range Scan Task Running, meta: {}".format(meta))


def range_scan_task():
    lstat.expmsg('Starting to test "Range Scan"')
    meta = dict()
    meta["TERMINATE"] = False
    range_scan_unit_operation(meta=meta)
    tester.flags["FINISH"] = True
    tester.flags["RUNNING"] = False
    lstat.expmsg("Test done")


@ignore_connection_error
def __callback_range_scan_start():
    tester.flags["TERMINATE"] = False
    tester.flags["FINISH"] = False
    tester.flags["RUNNING"] = True
    thread = Thread(target=range_scan_task)
    thread.start()


tester.start.on_click(__callback_range_scan_start)


def __callback_range_scan_terminate():
    lstat.expmsg("Terminating current job")
    tester.flags["TERMINATE"] = True
    tester.flags["FINISH"] = False
    tester.flags["RUNNING"] = False


tester.terminate.on_click(__callback_range_scan_terminate)

# region basic
foo0 = column(
    # basic config
    Div(text="<b>Linear Stage Under Test: {}</b>".format(
        tester.motion_controller_config["Name"])),
    tester.motion_controller.host,
    tester.motion_controller.port,
    tester.motion_controller.test_online,
    # schedule
    tester.start,
    tester.terminate,
)
bar0 = Panel(child=foo0, title="Linear Stage Controller")
# endregion basic

# region axis_0
foo0 = column(
    tester.motion_controller.multiples,
    tester.motion_controller.working_direction,
    Div(text="Position and Limitation Unit:"),
    tester.motion_controller.position_unit,
    tester.motion_controller.zero_point_absolute_position,
    tester.motion_controller.soft_limit_min,
    tester.motion_controller.soft_limit_max,
    tester.motion_controller.driving_speed,
    tester.motion_controller.driving_speed_unit,
    tester.motion_controller.driving_acceleration,
    tester.motion_controller.driving_acceleration_unit,
)

foo1 = column(
    # exp params
    Div(text="<b>Range Scan Param Settings:</b>"),
    tester.motion_controller.scan_mode,
    tester.motion_controller.working_unit,
    tester.motion_controller.range_scan_start,
    tester.motion_controller.range_scan_stop,
    tester.motion_controller.range_scan_step,
    tester.motion_controller.external_scan_list_file,
)

foo2 = column(
    # manual
    Div(text="<b>Manual Operations:</b>"),
    Div(text="Manual Operation Unit:"),
    tester.motion_controller.manual_unit,
    tester.motion_controller.manual_position,
    tester.motion_controller.manual_move,
    tester.motion_controller.manual_step,
    tester.motion_controller.manual_step_forward,
    tester.motion_controller.manual_step_backward,
)

bar = row(foo0, foo1, foo2)
bar1 = Panel(child=bar, title="Axis 0")
# endregion axis_0


t = Tabs(tabs=[bar0, bar1], name="dashboard")

doc.add_root(t)
