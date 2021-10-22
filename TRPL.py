# -*- coding: utf-8 -*-

"""TRPL.py:
This module assembles the Bokeh UI for 
Kerr Gating Time-resolved Photoluminescence Spectroscopy (TRPL)

The experiment is essentially delay line scan and voltage measurement.
"""
__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211021"


from kerr_gating import button_start_trpl

from general_setting import ti_file_stem, ti_scan_rounds
from linear_stage import rbg_delay_mode, ti_zero_delay, ti_delay_start, ti_delay_stop, ti_delay_step, fi_delay_list
from linear_stage import button_test_stage_online
from linear_stage import ti_move_stage, button_move_stage
from photodiode import figure_photodiode
from main_doc import doc
from expmsg import div_exp_msg

from bokeh.layouts import column, row
from bokeh.models import Panel, Tabs
from bokeh.models.widgets import Div


DEV_TEST = True


c_expst1 = column(
    ti_file_stem,
    ti_scan_rounds,
    button_start_trpl,
)


c_expst2 = column(Div(text='<h3>Delay Line Setup</h3>'),
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

c_components = column(
    Div(text='<h3>Delay Line Control</h3>'),
    button_test_stage_online, 
    ti_move_stage,
    button_move_stage,
)

r_manual = row(c_components)
c_manual = column(
    Div(text='<h2>Manual Control</h2>'),
    r_manual
)

c_preview = column(
    Div(text='<h2>Result Preview</h2>'),
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
