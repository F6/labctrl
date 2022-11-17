# -*- coding: utf-8 -*-

"""main.py:
This is a simple test for multiaxis movement widgets generated with bokeh library.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221113"


from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div, TextInput, PreText
from bokeh.models import Panel, Tabs
from tornado import gen

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.multiaxis_stages.factory import FactoryMultiAxis
from labctrl.main_doc import doc

from .utils import ignore_connection_error

app_name = "multiaxis_stages_bokeh"
doc.template_variables["app_name"] = app_name

app_config = lcfg.config["tests"][app_name]

motion_controller_name = app_config["ControllerUnderTesting"]


class MultiaxisStagesBokehWidgetTester:
    def __init__(self) -> None:
        self.motion_controller_config = lcfg.config["multiaxis_stages"][motion_controller_name]
        factory = FactoryMultiAxis(lcfg, lstat)
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


tester = MultiaxisStagesBokehWidgetTester()


@tester.motion_controller.axis_2.scan_range
@tester.motion_controller.axis_1.scan_range
@tester.motion_controller.axis_0.scan_range
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
    Div(text="<b>Multiaxis Controller Under Test: {}</b>".format(
        tester.motion_controller_config["Name"])),
    tester.motion_controller.host,
    tester.motion_controller.port,
    tester.motion_controller.test_online,
    # schedule
    tester.start,
    tester.terminate,
)
bar0 = Panel(child=foo0, title="Multiaxis Controller")
# endregion basic

# region axis_0
foo0 = column(
    tester.motion_controller.axis_0.multiples,
    tester.motion_controller.axis_0.working_direction,
    Div(text="Position and Limitation Unit:"),
    tester.motion_controller.axis_0.position_unit,
    tester.motion_controller.axis_0.zero_point_absolute_position,
    tester.motion_controller.axis_0.soft_limit_min,
    tester.motion_controller.axis_0.soft_limit_max,
    tester.motion_controller.axis_0.driving_speed,
    tester.motion_controller.axis_0.driving_speed_unit,
    tester.motion_controller.axis_0.driving_acceleration,
    tester.motion_controller.axis_0.driving_acceleration_unit,
)

foo1 = column(
    # exp params
    Div(text="<b>Range Scan Param Settings:</b>"),
    tester.motion_controller.axis_0.scan_mode,
    tester.motion_controller.axis_0.working_unit,
    tester.motion_controller.axis_0.range_scan_start,
    tester.motion_controller.axis_0.range_scan_stop,
    tester.motion_controller.axis_0.range_scan_step,
    tester.motion_controller.axis_0.external_scan_list_file,
)

foo2 = column(
    # manual
    Div(text="<b>Manual Operations:</b>"),
    Div(text="Manual Operation Unit:"),
    tester.motion_controller.axis_0.manual_unit,
    tester.motion_controller.axis_0.manual_position,
    tester.motion_controller.axis_0.manual_move,
    tester.motion_controller.axis_0.manual_step,
    tester.motion_controller.axis_0.manual_step_forward,
    tester.motion_controller.axis_0.manual_step_backward,
)

bar = row(foo0, foo1, foo2)
bar1 = Panel(child=bar, title="Axis 0")
# endregion axis_0

# region axis_1
foo0 = column(
    tester.motion_controller.axis_1.multiples,
    tester.motion_controller.axis_1.working_direction,
    Div(text="Position and Limitation Unit:"),
    tester.motion_controller.axis_1.position_unit,
    tester.motion_controller.axis_1.zero_point_absolute_position,
    tester.motion_controller.axis_1.soft_limit_min,
    tester.motion_controller.axis_1.soft_limit_max,
    tester.motion_controller.axis_1.driving_speed,
    tester.motion_controller.axis_1.driving_speed_unit,
    tester.motion_controller.axis_1.driving_acceleration,
    tester.motion_controller.axis_1.driving_acceleration_unit,
)

foo1 = column(
    # exp params
    Div(text="<b>Range Scan Param Settings:</b>"),
    tester.motion_controller.axis_1.scan_mode,
    tester.motion_controller.axis_1.working_unit,
    tester.motion_controller.axis_1.range_scan_start,
    tester.motion_controller.axis_1.range_scan_stop,
    tester.motion_controller.axis_1.range_scan_step,
    tester.motion_controller.axis_1.external_scan_list_file,
)

foo2 = column(
    # manual
    Div(text="<b>Manual Operations:</b>"),
    Div(text="Manual Operation Unit:"),
    tester.motion_controller.axis_1.manual_unit,
    tester.motion_controller.axis_1.manual_position,
    tester.motion_controller.axis_1.manual_move,
    tester.motion_controller.axis_1.manual_step,
    tester.motion_controller.axis_1.manual_step_forward,
    tester.motion_controller.axis_1.manual_step_backward,
)

bar = row(foo0, foo1, foo2)
bar2 = Panel(child=bar, title="Axis 1")
# endregion axis_1

# region axis_2
foo0 = column(
    tester.motion_controller.axis_2.multiples,
    tester.motion_controller.axis_2.working_direction,
    Div(text="Position and Limitation Unit:"),
    tester.motion_controller.axis_2.position_unit,
    tester.motion_controller.axis_2.zero_point_absolute_position,
    tester.motion_controller.axis_2.soft_limit_min,
    tester.motion_controller.axis_2.soft_limit_max,
    tester.motion_controller.axis_2.driving_speed,
    tester.motion_controller.axis_2.driving_speed_unit,
    tester.motion_controller.axis_2.driving_acceleration,
    tester.motion_controller.axis_2.driving_acceleration_unit,
)

foo1 = column(
    # exp params
    Div(text="<b>Range Scan Param Settings:</b>"),
    tester.motion_controller.axis_2.scan_mode,
    tester.motion_controller.axis_2.working_unit,
    tester.motion_controller.axis_2.range_scan_start,
    tester.motion_controller.axis_2.range_scan_stop,
    tester.motion_controller.axis_2.range_scan_step,
    tester.motion_controller.axis_2.external_scan_list_file,
)

foo2 = column(
    # manual
    Div(text="<b>Manual Operations:</b>"),
    Div(text="Manual Operation Unit:"),
    tester.motion_controller.axis_2.manual_unit,
    tester.motion_controller.axis_2.manual_position,
    tester.motion_controller.axis_2.manual_move,
    tester.motion_controller.axis_2.manual_step,
    tester.motion_controller.axis_2.manual_step_forward,
    tester.motion_controller.axis_2.manual_step_backward,
)

bar = row(foo0, foo1, foo2)
bar3 = Panel(child=bar, title="Axis 2")
# endregion axis_2

t = Tabs(tabs=[bar0, bar1, bar2, bar3], name="dashboard")

doc.add_root(t)
# Experiment Message
doc.add_root(lstat.pre_exp_msg)