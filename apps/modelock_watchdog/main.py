# -*- coding: utf-8 -*-

"""main.py:
This is a simple control panel for modelock watchdog generated with bokeh library.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20230711"

import time
import json
import base64
import os
import pandas as pd
from datetime import datetime
from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg, LabConfig
from labctrl.labstat import lstat, LabStat
from labctrl.main_doc import doc
from labctrl.widgets.figure import AbstractBundleFigure1D
from labctrl.components.generic_sensors.factory import FactorySensor
from labctrl.widgets.figure import FactoryFigure
from labctrl.widgets.text_display import FactoryTextDisplay
from labctrl.utilities import ignore_connection_error

app_name = "modelock_watchdog"
doc.template_variables["app_name"] = app_name
app_config = lcfg.config["apps"][app_name]
sensor_name = app_config["Sensor"]


sensor_values_report_template = """================================
Current Sensor Values:
================================
Temperature 1  : {t1:.3f} °C
Temperature 2  : {t2:.3f} °C
Humidity 1     : {h1:.3f} %RH
Humidity 2     : {h2:.3f} %RH
Air Pressure 1 : {ap1} kPa
Air Pressure 2 : {ap2} kPa
Pulse Counter  : {pc}
RTC Ticks      : {rtc}
================================
Calculated Values:
================================
Abs. Humidity 1: {ah1:.3f} kg/m3
Abs. Humidity 2: {ah2:.3f} kg/m3
Frequency      : {f:.6f} Hz
Intensity      : {i:.3f} V
Time           : {t}
================================
"""


class ModelockWatchdogAlarm:
    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.last_frequencies = []

    def check_frequency(self, frequency: float):
        self.last_frequencies.append(frequency)
        

class ModelockWatchdogApplication:
    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat
        self.sensor_config = lcfg.config["generic_sensors"][sensor_name]
        factory = FactorySensor(lcfg, lstat)
        bundle_config = dict()
        bundle_config["BundleType"] = "Bokeh"
        bundle_config["Config"] = self.sensor_config
        self.sensor_bundle = factory.generate_bundle(bundle_config)
        factory = FactoryFigure(lcfg, lstat)
        figure_bundle_config = dict()
        figure_bundle_config["BundleType"] = "Bokeh"
        self.data_preview_figures: dict[str, AbstractBundleFigure1D] = dict()
        for figure_config_name in app_config["PreviewFigures"]:
            figure_bundle_config["Config"] = app_config["PreviewFigures"][figure_config_name]
            self.data_preview_figures[figure_config_name] = factory.generate_bundle(
                figure_bundle_config)
        factory = FactoryTextDisplay(lcfg, lstat)
        text_display_bundle_config = dict()
        text_display_bundle_config["BundleType"] = "Bokeh"
        text_display_bundle_config["Config"] = {"Type": "PreText"}
        self.current_sensor_values_report = factory.generate_bundle(
            text_display_bundle_config)
        self.current_sensor_values_report.update(
            sensor_values_report_template.format(
                t1=0, t2=0, h1=0, h2=0,
                ap1=0, ap2=0, pc=0, rtc=0,
                ah1=0, ah2=0, f=0, i=0, t=''),
            self.lstat)
        self.watchdog_task_running = False
        self.watchdog_thread = None

        self.enable_watchdog = Button(
            label='Enable Watchdog', button_type="success")
        self.disable_watchdog = Button(
            label='Disable Watchdog', button_type="warning")


        # region enable_watchdog
        @ignore_connection_error
        def __callback_enable_watchdog():
            self.watchdog_task_running = True
            self.watchdog_thread = Thread(target=self.watchdog_task)
            self.watchdog_thread.start()

        self.enable_watchdog.on_click(__callback_enable_watchdog)
        # endregion enable_watchdog

        # region disable_watchdog
        def __callback_disable_watchdog():
            self.watchdog_task_running = False

        self.disable_watchdog.on_click(__callback_disable_watchdog)
        # endregion disable_watchdog

    def watchdog_task(self):
        plot_length = 3600*24  # around 1 day
        response = self.sensor_bundle.get_sensor_data()
        self.lstat.fmtmsg(response)
        data = response["data"]
        df = pd.DataFrame(data=data, index=[0])
        while self.watchdog_task_running:
            response = self.sensor_bundle.get_sensor_data()
            self.lstat.fmtmsg(response)
            data = response["data"]
            new_row = pd.Series(data)
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
            # save data every hour
            data_len = len(df)
            if data_len > 3600:
                # os.makedirs('logs', exist_ok=True)
                savename = datetime.fromtimestamp(
                    time.time()).strftime("%Y-%m-%d-%H-%M-%S")
                df.to_csv('logs/modelock_watchdog_{}.csv'.format(savename))
                # clear dataframe after save
                df = pd.DataFrame(data=data, index=[0])
            t_for_plot = datetime.fromtimestamp(data["Timestamp"])
            watchdog_app.data_preview_figures["Temperature1"].stream(
                [t_for_plot],
                [data["Temperature1"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Temperature2"].stream(
                [t_for_plot],
                [data["Temperature2"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Humidity1"].stream(
                [t_for_plot],
                [data["Humidity1"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Humidity2"].stream(
                [t_for_plot],
                [data["Humidity2"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Frequency"].stream(
                [t_for_plot],
                [data["Frequency"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Intensity"].stream(
                [t_for_plot],
                [data["Intensity"]],
                self.lstat,
                rollover=plot_length
            )
            self.current_sensor_values_report.update(
                sensor_values_report_template.format(
                    t1=data["Temperature1"],
                    t2=data["Temperature2"],
                    h1=data["Humidity1"],
                    h2=data["Humidity2"],
                    ap1='', 
                    ap2='', 
                    pc='', 
                    rtc='',
                    ah1=data["AbsoluteHumidity1"], 
                    ah2=data["AbsoluteHumidity2"], 
                    f=data["Frequency"],
                    i=data["Intensity"],
                    t=data["Time"],
                    ),
                self.lstat
            )
            time.sleep(1)  # 1fps


watchdog_app = ModelockWatchdogApplication(lcfg, lstat)


# region basic
foo1 = column(
    # basic config
    watchdog_app.sensor_bundle.host,
    watchdog_app.sensor_bundle.port,
    watchdog_app.sensor_bundle.test_online,
    watchdog_app.sensor_bundle.sensor_config_file,
    watchdog_app.sensor_bundle.submit_config,
    watchdog_app.sensor_bundle.manually_retrive_data,
    watchdog_app.enable_watchdog,
    watchdog_app.disable_watchdog,
    watchdog_app.current_sensor_values_report.text_display,
)

foo0 = column(
    watchdog_app.data_preview_figures["Temperature1"].figure,
    watchdog_app.data_preview_figures["Temperature2"].figure,
    watchdog_app.data_preview_figures["Humidity1"].figure,
    watchdog_app.data_preview_figures["Humidity2"].figure,
    watchdog_app.data_preview_figures["Frequency"].figure,
    watchdog_app.data_preview_figures["Intensity"].figure,
)

foo = row(foo1, foo0)

bar0 = Panel(child=foo, title="Sensors")
# endregion basic

t = Tabs(tabs=[bar0], name="dashboard")

doc.add_root(t)
# Experiment Message
doc.add_root(lstat.pre_exp_msg)
