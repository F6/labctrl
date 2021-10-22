# -*- coding: utf-8 -*-

"""kerr_gating.py:
This module implements the
Kerr Gating Time-resolved Photoluminescence Spectroscopy
technic

In such experiments, an ultrafast laser pulse excites the sample to
higher electronic excited states, then the fluorescence and
phosphorescence from the decay of the electronic excited
states are collected with reflective objectives, then modulated
with a chopper. The modulated light is then sent into a Kerr gate
and detected with PMT. The PMT signal and chopper TTL sync signal
are sent into lock-in amplifier or boxcar averagers to recover the
lifetime signal. Another beam of ultrafast laser pulse and a delay 
line is used to set the opening time window of the Kerr gate. 

Reflective objectives are prefered over regular microscope objectives
because this type of objective introduces minimum distortion of
wavepacket-front in the geometric space, which will significantly decrease 
the Kerr gating efficiency and make it hard to detect the already weak
signal.

The lock-in amplifier in our lab is the Stanford Research 830. Another
lock-in amplifier, the Zurich Instruments UHF is also available but is
an overkill so try not to use it all the time.
"""
__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211021"


import time
from threading import Thread
from functools import partial
from bokeh.models.widgets import Button

from general_setting import scan_rounds
from linear_stage import scan_delay
from expmsg import expmsg
from remoteAPIs.ziUHF import ziUHF
from main_doc import doc
from photodiode import callback_update_pd_data
from labconfig import lcfg
from expdata import ExpData


@scan_rounds
@scan_delay
def __trpl_take_sample(meta=dict()):
    edata = meta["ExpData"]
    uhf = meta["ziUHF"]
    expmsg("Retriving signal from Lock-in amplifier data server")
    sig = uhf.get_boxcar_value()
    expmsg("Adding latest signal to dataset...")
    edata.sig[meta["iDelay"]] = sig
    edata.sigsum[meta["iDelay"]] += sig
    doc.add_next_tick_callback(
        partial(callback_update_pd_data, edata.sig))
    # if this the end of delay scan, call export
    if meta["iDelay"] + 1 == len(lcfg.delay_line["ScanList"]):
        edata.export("scandata/" + lcfg.file_stem +
                     "-Round{rd}".format(rd=meta["iRound"]))


def __trpl_task():
    """
    Implements the thread task for IR Modulated Fluorescence spectroscopy
    """
    max_retry = 3

    # reallocate space for experiment data
    edata = ExpData(lcfg)

    # initialize UHF instrument
    expmsg("Initializing Zurich Instruments UHF Boxcar Averagers...")
    uhf = ziUHF()
    uhf.init_session()
    uhf.init_boxcar()

    time.sleep(1)

    meta = dict()
    meta["ExpData"] = edata
    meta["ziUHF"] = uhf
    __trpl_take_sample(meta=meta)

    expmsg("Scanning done. Disconnecting from Zurich Instruments UHF Data Server")
    uhf.close_session()


def __callback_start_trpl_button():
    lcfg.experiment_type = "TRPL"
    thread = Thread(target=__trpl_task)
    thread.start()


button_start_trpl = Button(label='Start TRPL', button_type='success')
button_start_trpl.on_click(__callback_start_trpl_button)
