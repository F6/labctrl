# -*- coding: utf-8 -*-

"""main.py:
This module implements
a method to automatically align input laser beam direction with a linear delay line.

Delay lines are commonly used in coherent or ultrafast laser labs to introduce
time delays or phase difference between two laser beams.
For the delay line to work, an adjustable input coupling mirror must be used to align the
input laser direction precisely with the moving direction of the linear stage.
If the laser beam is misaligned, the output beam from the delay line will shift
in space when the linear stage moves.

Due to temperature drifting and material aging, for time-critical or precise experiments,
delay lines are generally re-aligned manually before experiment start.
One simple way to align the linear stage is to put a beam analyzer after the
delay line, then move the delay line from one end to another, and check with the 
beam analyzer if the beam center moves during linear stage movement.
Adjust the input coupling mirror and repeat until no movement of beam center is observed
on the beam analyzer.

Module requires a motorized 2-axis adjustable mirror mount and a beam analyzer
to work. Before starts, insert the beam analyzer after the delay line (or 
permenently install the beam analyzer after the delay line with a beam sampler.
In our lab we usually use a backside-polished 45 degree laser line mirror
as a simple beam sampler. 99% of the laser energy is reflected at front surface
and around 0.5% of energy can pass through the laser line mirror for us to analyze.)
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221117"


import time
import numpy as np

from functools import partial
from threading import Thread

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div, TextInput, PreText
from bokeh.models import Panel, Tabs
from tornado import gen

from labctrl.labconfig import lcfg, LabConfig
from labctrl.labstat import lstat, LabStat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.multiaxis_stages.factory import FactoryMultiAxis
from labctrl.components.cameras.factory import FactoryCamera
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.widgets.figure import FactoryFigure

from .image_preprocessor import image_preprocess, image_preprocess_no_fit
from .utils import eval_float, ignore_connection_error

app_name = "linear_stage_alignment"
doc.template_variables["app_name"] = app_name
app_config: dict = lcfg.config["apps"][app_name]
delay_stage_name: str = app_config["StageToAlign"]
motorized_mirror_mount_name: str = app_config["InputCoupler"]
beam_analyzer_name: str = app_config["BeamAnalyzerCamera"]


class AlignExperiment:
    """
    this holds all the UI widgets, unit operations, bundles and thread 
    tasks for the experiment
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        factory = FactoryLinearStage(lcfg, lstat)
        linear_stage_bundle_config = dict()
        linear_stage_bundle_config["BundleType"] = "Bokeh"
        linear_stage_bundle_config["Config"] = lcfg.config["linear_stages"][delay_stage_name]
        self.delay_stage = factory.generate_bundle(linear_stage_bundle_config)

        factory = FactoryMultiAxis(lcfg, lstat)
        input_coupler_bundle_config = dict()
        input_coupler_bundle_config["BundleType"] = "Bokeh"
        input_coupler_bundle_config["Config"] = lcfg.config["multiaxis_stages"][motorized_mirror_mount_name]
        self.input_coupler = factory.generate_bundle(
            input_coupler_bundle_config)

        factory = FactoryCamera(lcfg, lstat)
        camera_bundle_config = dict()
        camera_bundle_config["BundleType"] = "Bokeh"
        camera_bundle_config["Config"] = lcfg.config["cameras"][beam_analyzer_name]
        self.camera = factory.generate_bundle(camera_bundle_config)

        factory = FactoryFigure(lcfg, lstat)
        denoised_figure_bundle_config = dict()
        denoised_figure_bundle_config["BundleType"] = "Bokeh"
        denoised_figure_bundle_config["Config"] = app_config["BeamAnalyzerDenoisedFigure"]
        self.denoised_figure_bundle = factory.generate_bundle(
            denoised_figure_bundle_config)
        original_figure_bundle_config = dict()
        original_figure_bundle_config["BundleType"] = "Bokeh"
        original_figure_bundle_config["Config"] = app_config["BeamAnalyzerOriginalFigure"]
        self.original_figure_bundle = factory.generate_bundle(
            original_figure_bundle_config)

        factory = FactoryGenericMethods()
        self.generic = factory.generate(lcfg, lstat)

        # region align_min_max
        self.align_min = TextInput(
            title="Align Min (ps)", value=str(app_config["AlignMin"]))
        self.align_max = TextInput(
            title="Align Max (ps)", value=str(app_config["AlignMax"]))
        self.move_to_align_min = Button(
            label="Move Stage to Align Min", button_type='warning')
        self.move_to_align_max = Button(
            label="Move Stage to Align Max", button_type='warning')

        @lcfg.update_config
        def __callback_align_min(attr, old, new):
            app_config["AlignMin"] = eval_float(self.align_min.value)

        self.align_min.on_change('value', __callback_align_min)

        @lcfg.update_config
        def __callback_align_max(attr, old, new):
            app_config["AlignMax"] = eval_float(self.align_max.value)

        self.align_max.on_change('value', __callback_align_max)

        @ignore_connection_error
        def __callback_move_to_align_min():
            lstat.expmsg("Moving delay stage to minimum")
            self.delay_stage.set_delay(app_config["AlignMin"])

        self.move_to_align_min.on_click(__callback_move_to_align_min)

        @ignore_connection_error
        def __callback_move_to_align_max():
            lstat.expmsg("Moving delay stage to maximum")
            self.delay_stage.set_delay(app_config["AlignMax"])

        self.move_to_align_max.on_click(__callback_move_to_align_max)
        # endregion align_min_max

        # region analyze_beam
        self.retrive_beam_running_flag = False

        self.retrive_beam = Button(
            label="Start Retriving Beam Profile", button_type='success')
        self.terminate_retrive_beam = Button(
            label="Terminate Retriving Beam Profile", button_type='warning')
        self.analyze_beam = Button(
            label="Retrive and Analyze Beam Profile", button_type='success')
        self.fit_report = PreText(
            text='''Fit Report: ''', width=300, height=300)
        self.fit_report_previous = PreText(
            text='''Previous Fit Report: ''', width=300, height=300)

        def retrive_task():
            while self.retrive_beam_running_flag:
                lstat.expmsg("Retriving signal from sensor...")
                img = self.camera.get_image()
                lstat.expmsg("Adding latest signal to dataset...")
                img_denoise_fs, img_fs = image_preprocess_no_fit(img)
                xmin = 0
                ymin = 0
                xmax = img_denoise_fs.shape[1]
                ymax = img_denoise_fs.shape[0]
                self.denoised_figure_bundle.update(
                    img_denoise_fs, xmin, xmax, ymin, ymax, lstat)
                self.original_figure_bundle.update(
                    img_fs, xmin, xmax, ymin, ymax, lstat)

        @ignore_connection_error
        def __callback_retrive_beam():
            self.retrive_beam_running_flag = True
            thread = Thread(target=retrive_task)
            thread.start()

        self.retrive_beam.on_click(__callback_retrive_beam)

        @ignore_connection_error
        def __callback_terminate_retrive_beam():
            self.retrive_beam_running_flag = False

        self.terminate_retrive_beam.on_click(__callback_terminate_retrive_beam)

        self.fit_report_template = """Fit Report:
    Center X : {centerx},
    Center Y : {centery},
    FWHM X   : {fwhmx},
    FWHM Y   : {fwhmy},
    Amplitude: {amplitude},
    Height   : {height},
    Sigma X  : {sigmax},
    Sigma Y  : {sigmay}
        """

        @ignore_connection_error
        def __callback_analyze_beam():
            lstat.expmsg("Retriving signal from sensor...")
            img = self.camera.get_image()
            lstat.expmsg("Adding latest signal to dataset...")
            img_denoise_fs, img_fs, fit_result = image_preprocess(img)
            xmin = 0
            ymin = 0
            xmax = img_denoise_fs.shape[1]
            ymax = img_denoise_fs.shape[0]
            self.denoised_figure_bundle.update(
                img_denoise_fs, xmin, xmax, ymin, ymax, lstat)
            self.original_figure_bundle.update(
                img_fs, xmin, xmax, ymin, ymax, lstat)
            self.update_fit_report(
                self.fit_report_template.format(**fit_result))

        self.analyze_beam.on_click(__callback_analyze_beam)
        # endregion analyze_beam

        # region schedule
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }

        self.start = Button(label="Start Aligning", button_type='success')
        self.terminate = Button(
            label="Terminate Aligning", button_type='warning')

        @self.generic.scan_round
        def unit_operation(meta=dict()):
            if self.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg(
                    "AutoAlign operation received signal TERMINATE, trying graceful Thread exit")
                return
            lstat.expmsg("Retriving signal from sensor...")
            img = self.camera.get_image()
            lstat.expmsg("Adding latest signal to dataset...")
            img_denoise_fs, img_fs, fit_result = image_preprocess(img)
            xmin = 0
            ymin = 0
            xmax = img_denoise_fs.shape[1]
            ymax = img_denoise_fs.shape[0]
            self.denoised_figure_bundle.update(
                img_denoise_fs, xmin, xmax, ymin, ymax, lstat)
            self.original_figure_bundle.update(
                img_fs, xmin, xmax, ymin, ymax, lstat)
            self.update_fit_report(
                self.fit_report_template.format(**fit_result))

        def task():
            lstat.expmsg("Starting experiment")
            meta = dict()
            meta["TERMINATE"] = False
            unit_operation(meta=meta)
            self.flags["FINISH"] = True
            self.flags["RUNNING"] = False
            lstat.expmsg("Experiment done")

        def __callback_start():
            self.flags["TERMINATE"] = False
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = True
            thread = Thread(target=task)
            thread.start()

        self.start.on_click(__callback_start)

        def __callback_terminate():
            lstat.expmsg("Terminating current job")
            self.flags["TERMINATE"] = True
            self.flags["FINISH"] = False
            self.flags["RUNNING"] = False

        self.terminate.on_click(__callback_terminate)
        # endregion schedule

    @gen.coroutine
    def __callback_update_fit_report(self, text):
        self.fit_report_previous.text = "Previous " + self.fit_report.text
        self.fit_report.text = text

    def update_fit_report(self, text):
        lstat.doc.add_next_tick_callback(
            partial(self.__callback_update_fit_report, text))


align = AlignExperiment(lcfg, lstat)


# roots: ["dashboard", "setup", "param", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here

# region dashboard
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)
# endregion dashboard

# region messages
# ================ Experiment Message ================
doc.add_root(lstat.pre_exp_msg)
# endregion messages

# region setup
# ================ setup ================
foo = column(
    align.delay_stage.host,
    align.delay_stage.port,
    align.delay_stage.multiples,
    align.delay_stage.working_direction,
    Div(text="Position and Limitation Unit:"),
    align.delay_stage.position_unit,
    align.delay_stage.zero_point_absolute_position,
    align.delay_stage.soft_limit_min,
    align.delay_stage.soft_limit_max,
    align.delay_stage.driving_speed,
    align.delay_stage.driving_speed_unit,
    align.delay_stage.driving_acceleration,
    align.delay_stage.driving_acceleration_unit,
)
setup_tab1 = Panel(child=foo, title="Aligning Delay Line")
foo = column(
    align.camera.host,
    align.camera.port,
    Div(text="Camera Working Mode:"),
    align.camera.working_mode,
    align.camera.change_working_mode,
    align.camera.exposure_time,
    align.camera.exposure_time_unit,
    align.camera.change_exposure_time,
    align.camera.apply_all_settings,
)
setup_tab2 = Panel(child=foo, title="Beam Analyzer")
foo = column(
    align.input_coupler.host,
    align.input_coupler.port,
)
setup_tab3 = Panel(child=foo, title="Input Coupler (IC)")
foo0 = column(
    Div(text="<b>Axis 0</b>"),
    align.input_coupler.axis_0.multiples,
    align.input_coupler.axis_0.working_direction,
    Div(text="Position and Limitation Unit:"),
    align.input_coupler.axis_0.position_unit,
    align.input_coupler.axis_0.zero_point_absolute_position,
    align.input_coupler.axis_0.soft_limit_min,
    align.input_coupler.axis_0.soft_limit_max,
    align.input_coupler.axis_0.driving_speed,
    align.input_coupler.axis_0.driving_speed_unit,
    align.input_coupler.axis_0.driving_acceleration,
    align.input_coupler.axis_0.driving_acceleration_unit,
)

foo1 = column(
    Div(text="<b>Axis 1</b>"),
    align.input_coupler.axis_1.multiples,
    align.input_coupler.axis_1.working_direction,
    Div(text="Position and Limitation Unit:"),
    align.input_coupler.axis_1.position_unit,
    align.input_coupler.axis_1.zero_point_absolute_position,
    align.input_coupler.axis_1.soft_limit_min,
    align.input_coupler.axis_1.soft_limit_max,
    align.input_coupler.axis_1.driving_speed,
    align.input_coupler.axis_1.driving_speed_unit,
    align.input_coupler.axis_1.driving_acceleration,
    align.input_coupler.axis_1.driving_acceleration_unit,
)

foo2 = column(
    Div(text="<b>Axis 2</b>"),
    align.input_coupler.axis_2.multiples,
    align.input_coupler.axis_2.working_direction,
    Div(text="Position and Limitation Unit:"),
    align.input_coupler.axis_2.position_unit,
    align.input_coupler.axis_2.zero_point_absolute_position,
    align.input_coupler.axis_2.soft_limit_min,
    align.input_coupler.axis_2.soft_limit_max,
    align.input_coupler.axis_2.driving_speed,
    align.input_coupler.axis_2.driving_speed_unit,
    align.input_coupler.axis_2.driving_acceleration,
    align.input_coupler.axis_2.driving_acceleration_unit,
)
bar = row(foo0, foo1, foo2)
setup_tab4 = Panel(child=bar, title="IC Axes")
setup_tabs = Tabs(tabs=[setup_tab1,
                        setup_tab2,
                        setup_tab3,
                        setup_tab4], name="setup")
doc.add_root(setup_tabs)
# endregion setup

# region params
# ================ params ================
foo = column(
    align.delay_stage.scan_mode,
    align.delay_stage.working_unit,
    align.delay_stage.range_scan_start,
    align.delay_stage.range_scan_stop,
    align.delay_stage.range_scan_step,
    align.delay_stage.external_scan_list_file,
)
param_tab1 = Panel(child=foo, title="Aligning Delay Line")

param_tabs = Tabs(tabs=[param_tab1], name="param")
doc.add_root(param_tabs)
# endregion params

# region manual
# ================ manual ================
foo = column(
    align.delay_stage.test_online,
    Div(text="Manual Operation Unit:"),
    align.delay_stage.manual_unit,
    align.delay_stage.manual_position,
    align.delay_stage.manual_move,
    align.delay_stage.manual_step,
    align.delay_stage.manual_step_forward,
    align.delay_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Aligning Delay Line")
foo = column(
    align.camera.preview_figure.figure,
    align.camera.test_online,
    align.camera.manual_take_sample,
)
manual_tab2 = Panel(child=foo, title="Beam Analyzer")
foo = column(
    align.input_coupler.test_online,
)
manual_tab3 = Panel(child=foo, title="Input Coupler (IC)")
foo0 = column(
    Div(text="<b>Axis 0</b>"),
    Div(text="Manual Operation Unit:"),
    align.input_coupler.axis_0.manual_unit,
    align.input_coupler.axis_0.manual_position,
    align.input_coupler.axis_0.manual_move,
    align.input_coupler.axis_0.manual_step,
    align.input_coupler.axis_0.manual_step_forward,
    align.input_coupler.axis_0.manual_step_backward,
)

foo1 = column(
    Div(text="<b>Axis 1</b>"),
    Div(text="Manual Operation Unit:"),
    align.input_coupler.axis_1.manual_unit,
    align.input_coupler.axis_1.manual_position,
    align.input_coupler.axis_1.manual_move,
    align.input_coupler.axis_1.manual_step,
    align.input_coupler.axis_1.manual_step_forward,
    align.input_coupler.axis_1.manual_step_backward,
)

foo2 = column(
    Div(text="<b>Axis 2</b>"),
    Div(text="Manual Operation Unit:"),
    align.input_coupler.axis_2.manual_unit,
    align.input_coupler.axis_2.manual_position,
    align.input_coupler.axis_2.manual_move,
    align.input_coupler.axis_2.manual_step,
    align.input_coupler.axis_2.manual_step_forward,
    align.input_coupler.axis_2.manual_step_backward,
)

bar = row(foo0, foo1, foo2)
manual_tab4 = Panel(child=bar, title="IC Axes")
manual_tabs = Tabs(tabs=[manual_tab1,
                         manual_tab2,
                         manual_tab3,
                         manual_tab4,], name="manual")
doc.add_root(manual_tabs)
# endregion manual

# region schedule
# ================ schedule ================
foo = column(
    align.generic.filestem,
    align.generic.scanrounds,
    align.start,
    align.terminate
)
schedule_tab1 = Panel(child=foo, title="Auto Align")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)
# endregion schedule

# region reports
# ================ reports ================
image_panel0 = Panel(child=align.denoised_figure_bundle.figure,
                     title="Denoised Beam Profile")
image_panel1 = Panel(child=align.original_figure_bundle.figure,
                     title="Full Scaled Beam Profile")
image_panel = Tabs(tabs=[image_panel0, image_panel1])
foo = column(
    image_panel,
    row(align.fit_report, align.fit_report_previous)
)
foo2 = column(
    Div(text="<b>Delay Stage:</b>"),
    align.align_min,
    align.move_to_align_min,
    align.align_max,
    align.move_to_align_max,
    Div(text="<b>Beam Analyzer:</b>"),
    align.retrive_beam,
    align.terminate_retrive_beam,
    align.analyze_beam,
    Div(text="<b>Input Coupler:</b>"),
    Div(text="X Axis:"),
    align.input_coupler.axis_0.manual_step,
    align.input_coupler.axis_0.manual_step_forward,
    align.input_coupler.axis_0.manual_step_backward,
    Div(text="Y Axis:"),
    align.input_coupler.axis_1.manual_step,
    align.input_coupler.axis_1.manual_step_forward,
    align.input_coupler.axis_1.manual_step_backward,
)
bar = row(foo, foo2)
reports_tab1 = Panel(child=bar, title="Auto Align")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
# endregion reports
