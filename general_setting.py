# -*- coding: utf-8 -*-

"""general_setting.py:
This module provides the Bokeh UI widgets for 
exporting and saving experiment results, and other
generic experiment hyperparams like experiment rounds, etc.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"


from labconfig import lcfg
from expmsg import expmsg
from bokeh.models.widgets import TextInput


def __callback_file_stem_text_input(attr, old, new):
    try:
        lcfg.file_stem = str(
            ti_file_stem.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_file_stem = TextInput(
    title='File Stem', value=str(lcfg.file_stem))
ti_file_stem.on_change(
    'value', __callback_file_stem_text_input)


def __callback_scan_rounds_text_input(attr, old, new):
    try:
        lcfg.scan_rounds = int(
            ti_scan_rounds.value)
        lcfg.refresh_config()
    except Exception as inst:
        print(type(inst), inst.args)


ti_scan_rounds = TextInput(
    title='Scan Rounds', value=str(lcfg.scan_rounds))
ti_scan_rounds.on_change(
    'value', __callback_scan_rounds_text_input)


def scan_rounds(func, meta=''):
    """scan rounds for func"""
    def iterate(meta=dict()):
        for i, rd in enumerate(range(lcfg.scan_rounds)):
            expmsg("Scanning Round No.{}".format(rd))
            meta["Round"] = rd
            meta["iRound"] = i
            func(meta=meta)

    return iterate
