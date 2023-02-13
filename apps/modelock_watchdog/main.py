# -*- coding: utf-8 -*-

"""main.py:
This is a simple control panel for modelock watchdog generated with bokeh library.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221227"

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


sensor_values_report_template = """Current Sensor Values:
Temperature 1: {t1} °C
Temperature 2: {t2} °C
Humidity 1   : {h1} %RH
Humidity 2   : {h2} %RH
Frequency    : {f} Hz
Intensity    : {i} V
Time         : {t}
"""


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
                t1='', t2='', h1='', h2='', f='', i='', t=''),
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

    def parse_data(self, data):
        """
        [NOTE]: This should be done at server side, but we temporarily put
        it here for some dev flexibility
        [TODO]: Update and move this to server side later 
        """
        parsed = dict()
        parsed["Temperature1"] = data["Temperature1"] / 1000
        parsed["Temperature2"] = data["Temperature2"] / 1000
        parsed["Humidity1"] = data["Humidity1"] / 1000
        parsed["Humidity2"] = data["Humidity2"] / 1000
        parsed["Frequency"] = data["Frequency"]
        parsed["Intensity"] = 0  # no intensity data yet
        parsed["Time"] = datetime.fromtimestamp(data["Timestamp"])
        return parsed

    def watchdog_task(self):
        plot_length = 3600*24  # around 1 day
        response = self.sensor_bundle.get_sensor_data()
        self.lstat.fmtmsg(response)
        data = self.parse_data(response["data"])
        df = pd.DataFrame(data=data, index=[0])
        while self.watchdog_task_running:
            response = self.sensor_bundle.get_sensor_data()
            self.lstat.fmtmsg(response)
            data = self.parse_data(response["data"])
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
            watchdog_app.data_preview_figures["Temperature1"].stream(
                [data["Time"]],
                [data["Temperature1"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Temperature2"].stream(
                [data["Time"]],
                [data["Temperature2"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Humidity1"].stream(
                [data["Time"]],
                [data["Humidity1"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Humidity2"].stream(
                [data["Time"]],
                [data["Humidity2"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Frequency"].stream(
                [data["Time"]],
                [data["Frequency"]],
                self.lstat,
                rollover=plot_length
            )
            watchdog_app.data_preview_figures["Intensity"].stream(
                [data["Time"]],
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
                    f=data["Frequency"],
                    i=data["Intensity"],
                    t=data["Time"]),
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
