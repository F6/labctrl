# -*- coding: utf-8 -*-

"""test_frontend.py:
This is a simple testing dashboard for tweaking servos.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20230304"

import time
import numpy as np
from threading import Thread
from functools import partial
from abc import ABC, abstractmethod
from typing import Union, NewType, Any
from bokeh.plotting import Figure as BokehFigure
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, LinearColorMapper, Range1d, Whisker, LinearAxis
from bokeh.palettes import viridis
from bokeh.models.widgets import Button, Div, TextInput, RadioButtonGroup
from tornado import gen
from bokeh.plotting import curdoc
from bokeh.layouts import column, row

from drv8870_HAL import DRV8870

doc = curdoc()
servo = DRV8870(com="COM8")
servo.start()


class ServoFigureBundle:
    """
    Copied and modified from labctrl.widgets.figure
    """

    def __init__(self, title: str, plot_width: int, plot_height: int) -> None:
        spectrum_tools = "box_zoom,pan,undo,redo,reset,save,crosshair"
        x_name = "Tick"
        y_names = ["Position", "Velocity", "Target", "OutputP", "OutputN"]
        color_cycle = viridis(len(y_names))
        length = 100  # the length does not matter because every update resets the length
        self.figure = figure(title=title, x_axis_label=x_name,
                             y_axis_label="Observable", plot_width=plot_width,
                             plot_height=plot_height, tools=spectrum_tools)
        self.figure.extra_y_ranges["Velocity"] = Range1d(start=-20, end=20)
        self.figure.add_layout(LinearAxis(
            y_range_name="Velocity", axis_line_color=color_cycle[1]), 'right')
        self.figure.extra_y_ranges["out_p_n"] = Range1d(start=-10, end=800)
        self.figure.add_layout(LinearAxis(
            y_range_name="out_p_n", axis_line_color=color_cycle[4]), 'right')

        self.ys = dict()
        for i, s in enumerate(y_names):
            self.ys[s] = np.zeros(length)

        self.x = np.array(range(length))
        self.ds = ColumnDataSource(data=dict(x=self.x, **self.ys))
        self.position_line = self.figure.line(
            'x', 'Position', line_width=1, source=self.ds,
            legend_label='Position', color=color_cycle[0])
        self.velocity_line = self.figure.line(
            'x', 'Velocity', line_width=1, source=self.ds,
            y_range_name="Velocity", legend_label='Velocity', color=color_cycle[1])
        self.target_line = self.figure.line(
            'x', 'Target', line_width=1, source=self.ds,
            legend_label='Target', color=color_cycle[2])
        self.outp_line = self.figure.line(
            'x', 'OutputP', line_width=1, source=self.ds,
            y_range_name="out_p_n", legend_label='OutputP', color=color_cycle[3])
        self.outn_line = self.figure.line(
            'x', 'OutputN', line_width=1, source=self.ds,
            y_range_name="out_p_n", legend_label='OutputN', color=color_cycle[4])

        ht = HoverTool(
            tooltips=[
                (x_name, '@x{0.000000}'),
                *[(s, '@{y_name}{{0.000000}}'.format(y_name=s))
                  for s in y_names],
            ],
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='vline'
        )
        self.figure.add_tools(ht)

    @gen.coroutine
    def callback_update(self, x, ys):
        """
        Expect:
        x: array
        ys: dict[name, array]
        """
        # update data
        new_data = {'x': x, **ys}
        self.ds.data = new_data

    def update(self, x, y, doc):
        doc.add_next_tick_callback(partial(self.callback_update, x, y))


class ServoTweaker:
    def __init__(self, doc) -> None:
        self.doc = doc
        self.oscilloscope1 = ServoFigureBundle(
            "Servo Status (Channel 0)",
            1080,
            640
        )
        self.oscilloscope2 = ServoFigureBundle(
            "Servo Status (Channel 1)",
            1080,
            640
        )
        self.oscilloscope1_n_sample = 256
        self.ch1_x = np.arange(self.oscilloscope1_n_sample)
        self.ch1_data = {
            "Position": np.zeros(self.oscilloscope1_n_sample),
            "Velocity": np.zeros(self.oscilloscope1_n_sample),
            "Target": np.zeros(self.oscilloscope1_n_sample),
            "OutputP": np.zeros(self.oscilloscope1_n_sample),
            "OutputN": np.zeros(self.oscilloscope1_n_sample)
        }
        self.update_task_running = False
        # Monitoring
        self.start_updating_status = Button(
            label='Start Updating Status', button_type="success")
        self.stop_updating_status = Button(
            label='Stop Updating Status', button_type="warning")
        # Params
        self.pid_p = 0.01
        self.pid_i = 0.001
        self.pid_d = 0.001
        self.pid_p_input = TextInput(title="PID Kp", value=str(self.pid_p))
        self.pid_i_input = TextInput(title="PID Ki", value=str(self.pid_i))
        self.pid_d_input = TextInput(title="PID Kd", value=str(self.pid_d))
        self.working_mode = RadioButtonGroup(
            labels=["Open Loop", "Velocity Loop", "Position Loop", ],
            active=0
        )
        self.submit_parameters = Button(
            label='Submit Parameters', button_type="warning")
        # Target
        self.target = 0
        self.target_input = TextInput(title="Target", value=str(self.target))
        self.submit_target = Button(
            label='Submit Target', button_type="warning")
        self.target2 = 100
        self.target2_input = TextInput(title="Target", value=str(self.target2))
        self.submit_target2 = Button(
            label='Submit Target 2', button_type="warning")

        def __callback_start_updating_status():
            self.update_task_running = True
            self.update_thread = Thread(target=self.update_task)
            self.update_thread.start()

        self.start_updating_status.on_click(__callback_start_updating_status)

        def __callback_stop_updating_status():
            self.update_task_running = False

        self.stop_updating_status.on_click(__callback_stop_updating_status)

        def __callback_pid_p_input(attr, old, new):
            self.pid_p = float(self.pid_p_input.value)

        self.pid_p_input.on_change('value', __callback_pid_p_input)

        def __callback_pid_i_input(attr, old, new):
            self.pid_i = float(self.pid_i_input.value)

        self.pid_i_input.on_change('value', __callback_pid_i_input)

        def __callback_pid_d_input(attr, old, new):
            self.pid_d = float(self.pid_d_input.value)

        self.pid_d_input.on_change('value', __callback_pid_d_input)

        def __callback_submit_parameters():
            servo.set_pid_parameters(0, self.pid_p, self.pid_i, self.pid_d)

        self.submit_parameters.on_click(__callback_submit_parameters)

        def __callback_working_mode(attr, old, new):
            _index = int(self.working_mode.active)
            servo.set_working_mode(0, _index)

        self.working_mode.on_change(
            'active', __callback_working_mode)

        def __callback_target_input(attr, old, new):
            self.target = int(self.target_input.value)

        self.target_input.on_change('value', __callback_target_input)

        def __callback_submit_target():
            servo.set_target(0, self.target)

        self.submit_target.on_click(__callback_submit_target)

        def __callback_target2_input(attr, old, new):
            self.target2 = int(self.target2_input.value)

        self.target2_input.on_change('value', __callback_target2_input)

        def __callback_submit_target2():
            servo.set_target(0, self.target2)

        self.submit_target2.on_click(__callback_submit_target2)

        self.monitors = column(self.oscilloscope1.figure,
                               self.oscilloscope2.figure)
        self.control = column(self.start_updating_status,
                              self.stop_updating_status,
                              self.pid_p_input,
                              self.pid_i_input,
                              self.pid_d_input,
                              self.submit_parameters,
                              self.working_mode,
                              self.target_input,
                              self.submit_target,
                              self.target2_input,
                              self.submit_target2)
        self.w = row(self.monitors, self.control)

    def update_task(self):
        i = 0
        while self.update_task_running:
            # Rate Limit to 10 FPS
            time.sleep(0.1)
            servo.read_status(0, blocking=True)
            print(servo.status)
            self.ch1_data["Position"][i] = servo.status['0']["Position"]
            self.ch1_data["Velocity"][i] = servo.status['0']["Velocity"]
            self.ch1_data["Target"][i] = servo.status['0']["Target"]
            self.ch1_data["OutputP"][i] = servo.status['0']["OutputP"]
            self.ch1_data["OutputN"][i] = servo.status['0']["OutputN"]
            self.oscilloscope1.update(self.ch1_x, self.ch1_data, self.doc)
            i = (i + 1) % self.oscilloscope1_n_sample

        time.sleep(0.1)


t = ServoTweaker(doc)

doc.add_root(t.w)
