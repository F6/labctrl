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
from labctrl.components.filter_wheels.factory import FactoryFilterWheel
from labctrl.main_doc import doc

from .utils import ignore_connection_error

app_name = "filter_wheels_bokeh"
doc.template_variables["app_name"] = app_name
app_config = lcfg.config["tests"][app_name]
controller_name = app_config["ControllerUnderTesting"]


class FilterWheelsBokehWidgetTester:
    def __init__(self) -> None:
        self.controller_config = lcfg.config["filter_wheels"][controller_name]
        factory = FactoryFilterWheel(lcfg, lstat)
        controller_bundle_config = dict()
        controller_bundle_config["Config"] = self.controller_config
        self.filter_wheel = factory.generate_bundle(controller_bundle_config)
        self.start = Button(label="Start Range Scan", button_type="success")
        self.terminate = Button(
            label="Terminate Range Scan", button_type="warning")
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }


tester = FilterWheelsBokehWidgetTester()


@tester.filter_wheel.axis_2.scan_range
@tester.filter_wheel.axis_1.scan_range
@tester.filter_wheel.axis_0.scan_range
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
    Div(text="<b>Filter Wheel Under Test: {}</b>".format(
        tester.controller_config["Name"])),
    tester.filter_wheel.host,
    tester.filter_wheel.port,
    tester.filter_wheel.test_online,
    # schedule
    tester.start,
    tester.terminate,
)
bar0 = Panel(child=foo0, title="Filter Wheel Controller")
# endregion basic

# region axis_0
foo0 = column(
    Div(text="<b>Basic Param Settings:</b>"),
    tester.filter_wheel.axis_0.multiples,
    tester.filter_wheel.axis_0.working_direction,
    Div(text="Position and Limitation Unit:"),
    tester.filter_wheel.axis_0.position_unit,
    tester.filter_wheel.axis_0.zero_point_absolute_position,
    tester.filter_wheel.axis_0.soft_limit_min,
    tester.filter_wheel.axis_0.soft_limit_max,
    tester.filter_wheel.axis_0.driving_speed,
    tester.filter_wheel.axis_0.driving_speed_unit,
    tester.filter_wheel.axis_0.driving_acceleration,
    tester.filter_wheel.axis_0.driving_acceleration_unit,
)

foo1 = column(
    # exp params
    Div(text="<b>Range Scan Param Settings:</b>"),
    tester.filter_wheel.axis_0.scan_mode,
    tester.filter_wheel.axis_0.working_unit,
    tester.filter_wheel.axis_0.range_scan_start,
    tester.filter_wheel.axis_0.range_scan_stop,
    tester.filter_wheel.axis_0.range_scan_step,
    tester.filter_wheel.axis_0.external_scan_list_file,
)

foo2 = column(
    # manual
    Div(text="<b>Manual Operations:</b>"),
    Div(text="Manual Operation Unit:"),
    tester.filter_wheel.axis_0.manual_unit,
    tester.filter_wheel.axis_0.manual_position,
    tester.filter_wheel.axis_0.manual_move,
    tester.filter_wheel.axis_0.manual_step,
    tester.filter_wheel.axis_0.manual_step_forward,
    tester.filter_wheel.axis_0.manual_step_backward,
)

foo3 = column(
    # filter wheels
    Div(text="<b>Filter Wheels:</b>"),
    tester.filter_wheel.axis_0.slots.position_slot_list[0],
    tester.filter_wheel.axis_0.slots.switch_to_slot_list[0],
    tester.filter_wheel.axis_0.slots.position_slot_list[1],
    tester.filter_wheel.axis_0.slots.switch_to_slot_list[1],
    tester.filter_wheel.axis_0.slots.position_slot_list[2],
    tester.filter_wheel.axis_0.slots.switch_to_slot_list[2],
    tester.filter_wheel.axis_0.slots.position_slot_list[3],
    tester.filter_wheel.axis_0.slots.switch_to_slot_list[3],
    tester.filter_wheel.axis_0.slots.position_slot_list[4],
    tester.filter_wheel.axis_0.slots.switch_to_slot_list[4],
    tester.filter_wheel.axis_0.slots.position_slot_list[5],
    tester.filter_wheel.axis_0.slots.switch_to_slot_list[5],
)

bar = row(foo0, foo1, foo2, foo3)
bar1 = Panel(child=bar, title="Axis 0")
# endregion axis_0

# region axis_1
foo0 = column(
    Div(text="<b>Basic Param Settings:</b>"),
    tester.filter_wheel.axis_1.multiples,
    tester.filter_wheel.axis_1.working_direction,
    Div(text="Position and Limitation Unit:"),
    tester.filter_wheel.axis_1.position_unit,
    tester.filter_wheel.axis_1.zero_point_absolute_position,
    tester.filter_wheel.axis_1.soft_limit_min,
    tester.filter_wheel.axis_1.soft_limit_max,
    tester.filter_wheel.axis_1.driving_speed,
    tester.filter_wheel.axis_1.driving_speed_unit,
    tester.filter_wheel.axis_1.driving_acceleration,
    tester.filter_wheel.axis_1.driving_acceleration_unit,
)

foo1 = column(
    # exp params
    Div(text="<b>Range Scan Param Settings:</b>"),
    tester.filter_wheel.axis_1.scan_mode,
    tester.filter_wheel.axis_1.working_unit,
    tester.filter_wheel.axis_1.range_scan_start,
    tester.filter_wheel.axis_1.range_scan_stop,
    tester.filter_wheel.axis_1.range_scan_step,
    tester.filter_wheel.axis_1.external_scan_list_file,
)

foo2 = column(
    # manual
    Div(text="<b>Manual Operations:</b>"),
    Div(text="Manual Operation Unit:"),
    tester.filter_wheel.axis_1.manual_unit,
    tester.filter_wheel.axis_1.manual_position,
    tester.filter_wheel.axis_1.manual_move,
    tester.filter_wheel.axis_1.manual_step,
    tester.filter_wheel.axis_1.manual_step_forward,
    tester.filter_wheel.axis_1.manual_step_backward,
)

foo3 = column(
    # filter wheels
    Div(text="<b>Filter Wheels:</b>"),
    tester.filter_wheel.axis_1.slots.position_slot_list[0],
    tester.filter_wheel.axis_1.slots.switch_to_slot_list[0],
    tester.filter_wheel.axis_1.slots.position_slot_list[1],
    tester.filter_wheel.axis_1.slots.switch_to_slot_list[1],
    tester.filter_wheel.axis_1.slots.position_slot_list[2],
    tester.filter_wheel.axis_1.slots.switch_to_slot_list[2],
    tester.filter_wheel.axis_1.slots.position_slot_list[3],
    tester.filter_wheel.axis_1.slots.switch_to_slot_list[3],
    tester.filter_wheel.axis_1.slots.position_slot_list[4],
    tester.filter_wheel.axis_1.slots.switch_to_slot_list[4],
    tester.filter_wheel.axis_1.slots.position_slot_list[5],
    tester.filter_wheel.axis_1.slots.switch_to_slot_list[5],
)

bar = row(foo0, foo1, foo2, foo3)
bar2 = Panel(child=bar, title="Axis 1")
# endregion axis_1

# region axis_2
foo0 = column(
    Div(text="<b>Basic Param Settings:</b>"),
    tester.filter_wheel.axis_2.multiples,
    tester.filter_wheel.axis_2.working_direction,
    Div(text="Position and Limitation Unit:"),
    tester.filter_wheel.axis_2.position_unit,
    tester.filter_wheel.axis_2.zero_point_absolute_position,
    tester.filter_wheel.axis_2.soft_limit_min,
    tester.filter_wheel.axis_2.soft_limit_max,
    tester.filter_wheel.axis_2.driving_speed,
    tester.filter_wheel.axis_2.driving_speed_unit,
    tester.filter_wheel.axis_2.driving_acceleration,
    tester.filter_wheel.axis_2.driving_acceleration_unit,
)

foo1 = column(
    # exp params
    Div(text="<b>Range Scan Param Settings:</b>"),
    tester.filter_wheel.axis_2.scan_mode,
    tester.filter_wheel.axis_2.working_unit,
    tester.filter_wheel.axis_2.range_scan_start,
    tester.filter_wheel.axis_2.range_scan_stop,
    tester.filter_wheel.axis_2.range_scan_step,
    tester.filter_wheel.axis_2.external_scan_list_file,
)

foo2 = column(
    # manual
    Div(text="<b>Manual Operations:</b>"),
    Div(text="Manual Operation Unit:"),
    tester.filter_wheel.axis_2.manual_unit,
    tester.filter_wheel.axis_2.manual_position,
    tester.filter_wheel.axis_2.manual_move,
    tester.filter_wheel.axis_2.manual_step,
    tester.filter_wheel.axis_2.manual_step_forward,
    tester.filter_wheel.axis_2.manual_step_backward,
)

foo3 = column(
    # filter wheels
    Div(text="<b>Filter Wheels:</b>"),
    tester.filter_wheel.axis_2.slots.position_slot_list[0],
    tester.filter_wheel.axis_2.slots.switch_to_slot_list[0],
    tester.filter_wheel.axis_2.slots.position_slot_list[1],
    tester.filter_wheel.axis_2.slots.switch_to_slot_list[1],
    tester.filter_wheel.axis_2.slots.position_slot_list[2],
    tester.filter_wheel.axis_2.slots.switch_to_slot_list[2],
    tester.filter_wheel.axis_2.slots.position_slot_list[3],
    tester.filter_wheel.axis_2.slots.switch_to_slot_list[3],
    tester.filter_wheel.axis_2.slots.position_slot_list[4],
    tester.filter_wheel.axis_2.slots.switch_to_slot_list[4],
    tester.filter_wheel.axis_2.slots.position_slot_list[5],
    tester.filter_wheel.axis_2.slots.switch_to_slot_list[5],
)

bar = row(foo0, foo1, foo2, foo3)
bar3 = Panel(child=bar, title="Axis 2")
# endregion axis_2

t = Tabs(tabs=[bar0, bar1, bar2, bar3], name="dashboard")

doc.add_root(t)
# Experiment Message
doc.add_root(lstat.pre_exp_msg)