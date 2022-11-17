# -*- coding: utf-8 -*-

"""main.py:
This module implements the
a method to automatically align input laser beam direction with a linear delay line.

Delay lines are commonly used in coherent or ultrafast laser labs to introduce
time delays or phase difference between two laser beams.
For the delay line to work, an adjustable input coupling mirror must be used to align the
input laser direction precisely with the moving direction of the linear stage.
If the laser beam is misaligned, the output beam from the delay line will shift
in space when the linear stage moves.

Due to temperature drifting, for time-critical or precise experiments,
delay lines are generally re-aligned manually before experiment start.
One simple way to align the linear stage is to put a beam analyzer after the
delay line, then move the delay line from one end to another, and check if
the beam center moves with the beam analyzer.
Adjust the input coupling mirror and repeat until no movement of beam center is observed
on the beam analyzer.

Module requires a motorized 2-axis adjustable mirror mount and a beam analyzer
to work. Before starts, insert the beam analyzer after the delay line (or 
permenently install the beam analyzer after the delay line with a beam sampler.
In our lab we generally use backside-polished 45 degree laser line mirrors
as a simple beam sampler. 99% of the laser energy is reflected and around 0.5%
of energy can pass through the laser line mirror for us to analyze.)
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221028"


import time
import numpy as np

from functools import partial
from threading import Thread

from scipy.fft import fft, fftfreq, fftshift

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div, TextInput, PreText
from bokeh.models import Panel, Tabs
from tornado import gen

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.components.cameras.factory import FactoryCamera
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.widgets.figure import FactoryFigure1D, FactoryImageRGBA

from .image_preprocessor import image_preprocess, image_preprocess_no_fit
from .utils import eval_float, ignore_connection_error

app_name = "linear_stage_alignment"
doc.template_variables["app_name"] = app_name

app_config = lcfg.config["apps"][app_name]

delay_stage = app_config["StageToAlign"]
motorized_mirror_mount = app_config["InputCoupler"]


class AlignPreviewFigure:
    """Images to be showed in the Preview tab
    """

    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.horizontal_max = factory.generate_fig1d(
            "Horizontal Section", "Pixel", "Intensity", 256)
        self.vertical_max = factory.generate_fig1d(
            "Vertical Section", "Pixel", "Intensity", 256)
        factory = FactoryImageRGBA()
        self.denoised_image = factory.generate_bundle(
            "Beam Profile Denoised", "Horizontal", "Vertical", "Intensity")
        self.camera_image = factory.generate_bundle(
            "Beam Profile", "Horizontal", "Vertical", "Intensity")


class AlignExpData:
    """Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.
    """

    def __init__(self, lcfg, lstat) -> None:
        # save a reference for later use. Each time lcfg get updated, expdata
        # instances are always lazy generated just before experiment starts,
        #  so no need to bother copying lcfg
        self.lcfg = lcfg
        self.lstat = lstat

    def export(self, filestem: str) -> None:
        pass


class AlignExperiment:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """

    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.start = Button(label="Start Aligning", button_type='success')
        self.terminate = Button(
            label="Terminate Aligning", button_type='warning')
        self.align_min = TextInput(title="Align Min (ps)", value="")
        self.align_max = TextInput(title="Align Max (ps)", value="")
        self.move_to_align_min = Button(
            label="Move Stage to Align Min", button_type='warning')
        self.move_to_align_max = Button(
            label="Move Stage to Align Max", button_type='warning')
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
        self.preview = AlignPreviewFigure()
        self.data = AlignExpData(lcfg, lstat)
        factory = FactoryLinearStage(lcfg, lstat)
        linear_stage_bundle_config = dict()
        linear_stage_bundle_config["Config"] = lcfg.config["linear_stages"][delay_stage]
        self.delay_stage = factory.generate_bundle(linear_stage_bundle_config)
        factory = FactoryCamera(lcfg, lstat)
        # Preparing to generate camera bundle... This should be moved to front end configurable zone but
        # i'm lazy for now
        camera_bundle_config = dict()
        camera_bundle_config["Name"] = "ToupTek_Color"
        camera_bundle_config["BundleType"] = "Bokeh"
        camera_bundle_config["PreviewImage"] = self.preview.camera_image
        self.camera = factory.generate_bundle(camera_bundle_config)
        factory = FactoryGenericMethods()
        self.generic = factory.generate(lcfg, lstat)
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }
        self.retrive_beam_running_flag = False  # Video Mode

    @gen.coroutine
    def __callback_update_fit_report(self, text):
        self.fit_report_previous.text = "Previous " + self.fit_report.text
        self.fit_report.text = text

    def update_fit_report(self, text):
        lstat.doc.add_next_tick_callback(
            partial(self.__callback_update_fit_report, text))


AutoAlign = AlignExperiment()


@AutoAlign.generic.scan_round
def unit_operation(meta=dict()):
    if AutoAlign.flags["TERMINATE"]:
        meta["TERMINATE"] = True
        lstat.expmsg(
            "AutoAlign operation received signal TERMINATE, trying graceful Thread exit")
        return
    lstat.expmsg("Retriving signal from sensor...")
    img = AutoAlign.camera.get_image()
    lstat.expmsg("Adding latest signal to dataset...")
    img_denoise_fs, img_fs = image_preprocess(img)
    xmin = 0
    ymin = 0
    xmax = img_denoise_fs.shape[1]
    ymax = img_denoise_fs.shape[0]
    lstat.doc.add_next_tick_callback(
        partial(AutoAlign.preview.camera_image.callback_update,
                img_denoise_fs,
                xmin, xmax,
                ymin, ymax)
    )


def task():
    lstat.expmsg("Allocating memory for experiment")
    AutoAlign.data = AlignExpData(lcfg, lstat)
    lstat.expmsg("Starting experiment")
    meta = dict()
    meta["TERMINATE"] = False
    unit_operation(meta=meta)
    AutoAlign.flags["FINISH"] = True
    AutoAlign.flags["RUNNING"] = False
    lstat.expmsg("Experiment done")


def __callback_start():
    AutoAlign.flags["TERMINATE"] = False
    AutoAlign.flags["FINISH"] = False
    AutoAlign.flags["RUNNING"] = True
    thread = Thread(target=task)
    thread.start()


AutoAlign.start.on_click(__callback_start)


def __callback_terminate():
    lstat.expmsg("Terminating current job")
    AutoAlign.flags["TERMINATE"] = True
    AutoAlign.flags["FINISH"] = False
    AutoAlign.flags["RUNNING"] = False


AutoAlign.terminate.on_click(__callback_terminate)

# region align_min_max


@lcfg.update_config
def __callback_align_min(attr, old, new):
    app_config["AlignMin"] = AutoAlign.align_min.value


AutoAlign.align_min.value = str(app_config["AlignMin"])
AutoAlign.align_min.on_change('value', __callback_align_min)


@ignore_connection_error
def __callback_move_to_align_min():
    lstat.expmsg("Moving delay stage to minimum")
    AutoAlign.delay_stage.set_delay(app_config["AlignMin"])


AutoAlign.move_to_align_min.on_click(__callback_move_to_align_min)


@lcfg.update_config
def __callback_align_max(attr, old, new):
    app_config["AlignMax"] = AutoAlign.align_max.value


AutoAlign.align_max.value = str(app_config["AlignMax"])
AutoAlign.align_max.on_change('value', __callback_align_max)


@ignore_connection_error
def __callback_move_to_align_max():
    lstat.expmsg("Moving delay stage to maximum")
    AutoAlign.delay_stage.set_delay(app_config["AlignMax"])


AutoAlign.move_to_align_max.on_click(__callback_move_to_align_max)
# endregion align_min_max

# region analyze_beam


def retrive_task():
    while AutoAlign.retrive_beam_running_flag:
        lstat.expmsg("Retriving signal from sensor...")
        img = AutoAlign.camera.get_image()
        lstat.expmsg("Adding latest signal to dataset...")
        img_denoise_fs, img_fs = image_preprocess_no_fit(img)
        xmin = 0
        ymin = 0
        xmax = img_denoise_fs.shape[1]
        ymax = img_denoise_fs.shape[0]
        lstat.doc.add_next_tick_callback(
            partial(AutoAlign.preview.denoised_image.callback_update,
                    img_denoise_fs,
                    xmin, xmax,
                    ymin, ymax)
        )
        lstat.doc.add_next_tick_callback(
            partial(AutoAlign.preview.camera_image.callback_update,
                    img_fs,
                    xmin, xmax,
                    ymin, ymax)
        )


@ignore_connection_error
def __callback_retrive_beam():
    AutoAlign.retrive_beam_running_flag = True
    thread = Thread(target=retrive_task)
    thread.start()

AutoAlign.retrive_beam.on_click(__callback_retrive_beam)


@ignore_connection_error
def __callback_terminate_retrive_beam():
    AutoAlign.retrive_beam_running_flag = False

AutoAlign.terminate_retrive_beam.on_click(__callback_terminate_retrive_beam)


fit_report_template = """Fit Report:
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
    img = AutoAlign.camera.get_image()
    lstat.expmsg("Adding latest signal to dataset...")
    img_denoise_fs, img_fs, fit_result = image_preprocess(img)
    xmin = 0
    ymin = 0
    xmax = img_denoise_fs.shape[1]
    ymax = img_denoise_fs.shape[0]
    lstat.doc.add_next_tick_callback(
        partial(AutoAlign.preview.denoised_image.callback_update,
                img_denoise_fs,
                xmin, xmax,
                ymin, ymax)
    )
    lstat.doc.add_next_tick_callback(
        partial(AutoAlign.preview.camera_image.callback_update,
                img_fs,
                xmin, xmax,
                ymin, ymax)
    )
    AutoAlign.update_fit_report(fit_report_template.format(**fit_result))


AutoAlign.analyze_beam.on_click(__callback_analyze_beam)
# endregion analyze_beam


# roots: ["dashboard", "setup", "param", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here

# region dashboard
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)
# endregion dashboard

# region setup
# ================ setup ================
foo = column(
    AutoAlign.delay_stage.host,
    AutoAlign.delay_stage.port,
    AutoAlign.delay_stage.multiples,
    AutoAlign.delay_stage.working_direction,
    Div(text="Position and Limitation Unit:"),
    AutoAlign.delay_stage.position_unit,
    AutoAlign.delay_stage.zero_delay_absolute_position,
    AutoAlign.delay_stage.soft_limit_min,
    AutoAlign.delay_stage.soft_limit_max,
    AutoAlign.delay_stage.driving_speed,
    AutoAlign.delay_stage.driving_speed_unit,
    AutoAlign.delay_stage.driving_acceleration,
    AutoAlign.delay_stage.driving_acceleration_unit,
)
setup_tab1 = Panel(child=foo, title="Aligning Delay Line")
setup_tabs = Tabs(tabs=[setup_tab1], name="setup")
doc.add_root(setup_tabs)
# endregion setup

# region params
# ================ params ================
foo = column(
    AutoAlign.delay_stage.scan_mode,
    AutoAlign.delay_stage.working_unit,
    AutoAlign.delay_stage.range_scan_start,
    AutoAlign.delay_stage.range_scan_stop,
    AutoAlign.delay_stage.range_scan_step,
    AutoAlign.delay_stage.external_scan_list_file,
)
param_tab1 = Panel(child=foo, title="Aligning Delay Line")
param_tabs = Tabs(tabs=[param_tab1], name="param")
doc.add_root(param_tabs)
# endregion params

# region manual
# ================ manual ================
foo = column(
    AutoAlign.delay_stage.test_online,
    Div(text="Manual Operation Unit:"),
    AutoAlign.delay_stage.manual_unit,
    AutoAlign.delay_stage.manual_position,
    AutoAlign.delay_stage.manual_move,
    AutoAlign.delay_stage.manual_step,
    AutoAlign.delay_stage.manual_step_forward,
    AutoAlign.delay_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Aligning Delay Line")
foo = column(
    AutoAlign.camera.test_online,
    AutoAlign.camera.manual_take_sample,
)
manual_tab2 = Panel(child=foo, title="Camera")
manual_tabs = Tabs(tabs=[manual_tab1, manual_tab2], name="manual")
doc.add_root(manual_tabs)
# endregion manual

# region schedule
# ================ schedule ================
foo = column(
    AutoAlign.generic.filestem,
    AutoAlign.generic.scanrounds,
    AutoAlign.start,
    AutoAlign.terminate
)
schedule_tab1 = Panel(child=foo, title="Auto Align")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)
# endregion schedule

# region reports
# ================ reports ================
image_panel0 = Panel(child=AutoAlign.preview.denoised_image.fig,
                     title="Denoised Beam Profile")
image_panel1 = Panel(child=AutoAlign.preview.camera_image.fig,
                     title="Full Scaled Beam Profile")
image_panel = Tabs(tabs=[image_panel0, image_panel1])
foo = column(
    image_panel,
    row(AutoAlign.fit_report, AutoAlign.fit_report_previous)
    # AutoAlign.preview.horizontal_max.fig,
    # AutoAlign.preview.vertical_max.fig,
)
foo2 = column(
    # Div(text="<h5>Delay Stage</h5>"),
    AutoAlign.align_min,
    AutoAlign.move_to_align_min,
    AutoAlign.align_max,
    AutoAlign.move_to_align_max,
    # Div(text="<h5>Beam Analyzer</h5>"),
    AutoAlign.retrive_beam,
    AutoAlign.terminate_retrive_beam,
    AutoAlign.analyze_beam,
)
bar = row(foo, foo2)
reports_tab1 = Panel(child=bar, title="Auto Align")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)
# endregion reports
