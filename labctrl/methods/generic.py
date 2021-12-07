# -*- coding: utf-8 -*-

"""generic.py:
This module implements the generic methods used by all
technics, such as round-by-round scan, adaptive scan, etc.

This module also manages the filestem and experiment type selection
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"


from bokeh.models.widgets import TextInput
from bokeh.layouts import column


class BundleGenericMethods:
    def __init__(self) -> None:
        self.filestem = TextInput(title='File Stem', value='')
        self.scanrounds = TextInput(title='Scan Rounds', value='')
        self.scan_round = None

    def quick_control_group(self):
        return column(
            self.filestem,
            self.scanrounds,
        )


class FactoryGenericMethods:
    def __init__(self) -> None:
        pass

    def generate(self, lcfg, lstat):
        bundle = BundleGenericMethods()
        update_config = lcfg.update_config

        @update_config
        def __callback_file_stem_text_input(attr, old, new):
            lcfg.config["basic"]["FileStem"] = str(bundle.filestem.value)

        bundle.filestem = TextInput(
            title='File Stem', value=str(lcfg.config["basic"]["FileStem"]))
        bundle.filestem.on_change('value', __callback_file_stem_text_input)

        @update_config
        def __callback_scan_rounds_text_input(attr, old, new):
            lcfg.config["basic"]["ScanRounds"] = int(bundle.scanrounds.value)

        bundle.scanrounds = TextInput(
            title='Scan Rounds', value=str(lcfg.config["basic"]["ScanRounds"]))
        bundle.scanrounds.on_change('value', __callback_scan_rounds_text_input)

        if "basic" not in lstat.stat:
            lstat.stat["basic"] = dict()

        def scan_rounds(func, meta=''):
            """scan rounds for func"""
            def iterate(meta=dict()):
                for i, rd in enumerate(range(lcfg.config["basic"]["ScanRounds"])):
                    if meta["TERMINATE"]:
                        lstat.expmsg("scan_round received signal TERMINATE, trying graceful Thread exit")
                        break
                    lstat.expmsg("Scanning Round No.{}".format(rd))
                    lstat.stat["basic"]["Round"] = rd
                    lstat.stat["basic"]["iRound"] = i
                    func(meta=meta)

            return iterate

        bundle.scan_round = scan_rounds

        return bundle

