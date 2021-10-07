# -*- coding: utf-8 -*-

"""backend.py:
This module assembles the Bokeh UI for experiment
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

from andor_camera import ti_exposure_time
from photodiode import rbg_pd_reference
from shutter import rbg_shutter_background
from ir_mod_fluorescence import button_start_imfs
from general_setting import ti_file_stem, ti_scan_rounds
from linear_stage import rbg_delay_mode, ti_zero_delay, ti_delay_start, ti_delay_stop, ti_delay_step, fi_delay_list
from ir_topas import rbg_ir_topas_mode, ti_ir_topas_start, ti_ir_topas_stop, ti_ir_topas_step, fi_ir_topas_list
from visible_topas import rbg_visible_topas_mode, ti_visible_topas_start, ti_visible_topas_stop, ti_visible_topas_step, fi_visible_topas_list
from linear_stage import button_test_stage_online
from andor_camera import button_test_CCD_online
from ir_topas import button_check_ir_topas
from visible_topas import button_check_topas_vis
from shutter import button_change_shutter, button_turn_off_shutter, button_turn_on_shutter
from linear_stage import ti_move_stage, button_move_stage
from photodiode import button_pd_take_signal
from andor_camera import take_signal_button
from expmsg import div_exp_msg
from photodiode import figure_photodiode
from andor_camera import figure_andor_camera
from main_doc import doc
from bokeh.layouts import column, row

from bokeh.models import Panel, Tabs
from bokeh.models.widgets import Div


DEV_TEST = True

c_expst1 = column(
    ti_file_stem,
    ti_scan_rounds,
    button_start_imfs,
    Div(text='<h3>Shutter Setup</h3>'),
    rbg_shutter_background,
    Div(text='<h3>PD Setup</h3>'),
    rbg_pd_reference,
    Div(text='<h3>CCD Setup</h3>'),
    ti_exposure_time,

)


c_expst2 = column(Div(text='<h3>Visible Topas Setup</h3>'),
                  rbg_visible_topas_mode,
                  ti_visible_topas_start,
                  ti_visible_topas_stop,
                  ti_visible_topas_step,
                  fi_visible_topas_list,
                  Div(text='<h3>ps Topas Setup</h3>'),
                  rbg_ir_topas_mode,
                  ti_ir_topas_start,
                  ti_ir_topas_stop,
                  ti_ir_topas_step,
                  fi_ir_topas_list,
                  Div(text='<h3>Delay Line Setup</h3>'),
                  rbg_delay_mode,
                  ti_zero_delay,
                  ti_delay_start,
                  ti_delay_stop,
                  ti_delay_step,
                  fi_delay_list,
                  )

r_experiment_setup = row(c_expst1, c_expst2)

c_experiment_setup = column(
    Div(text='<h2>Experiment Setup</h2>'),
    r_experiment_setup
)

c_nettest = column(
    Div(text='<h3>Shutter Control</h3>'),
    button_change_shutter,
    button_turn_off_shutter,
    button_turn_on_shutter,
    Div(text='<h3>Network Test</h3>'),
    button_check_topas_vis,
    button_check_ir_topas,
    button_test_CCD_online,
    button_test_stage_online,
)

c_components = column(
    Div(text='<h3>CCD Control</h3>'),
    take_signal_button,
    Div(text='<h3>PD Control</h3>'),
    button_pd_take_signal,
    Div(text='<h3>Delay Line Control</h3>'),
    ti_move_stage,
    button_move_stage,
)

r_manual = row(c_nettest, c_components)
c_manual = column(
    Div(text='<h2>Manual Control</h2>'),
    r_manual
)


c_preview = column(
    Div(text='<h2>Result Preview</h2>'),
    figure_andor_camera,
    figure_photodiode,
)

tab1 = Panel(child=c_experiment_setup, title="Experiment Setup")
tab2 = Panel(child=c_manual, title="Manual Control")
tab3 = Panel(child=c_preview, title="Result Preview")
tabs_main = Tabs(tabs=[tab1, tab2, tab3])

c_msg = column(
    Div(text='<h2>Messages</h2>'),
    div_exp_msg,
)

r1 = row(tabs_main, c_msg,)
doc.add_root(r1)
doc.title = "Lab Control Panel"
