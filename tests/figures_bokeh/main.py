# -*- coding: utf-8 -*-

"""main.py:
This is a simple test for figure widgets generated with bokeh library.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221113"

import time
import numpy as np
from threading import Thread

from bokeh.layouts import column

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.main_doc import doc
from labctrl.widgets.figure import (FactoryFigure, AbstractBundleFigure,
                                    BundleFigure1D, BundleFigure1DWithWhiskers, 
                                    BundleFigure2D, BundleImageRGBA)

config = lcfg.config["tests"]["figures_bokeh"]


class FigureWidgetTester():
    def __init__(self) -> None:
        self.figure_bundles: list[AbstractBundleFigure] = list()
        factory = FactoryFigure(lcfg, lstat)
        # ======== Test 1D Figure ========
        for bundle_config in config["TestFigures"]:
            figure_bundle = factory.generate_bundle(bundle_config)
            self.figure_bundles.append(figure_bundle)
        self.phase = 0
        thread = Thread(target=self.update_task)
        thread.start()

    def update_task(self):
        while True:
            time.sleep(0.05)
            self.phase = self.phase + 0.1
            for i in self.figure_bundles:
                if isinstance(i, BundleFigure1D):
                    x = np.linspace(0, 6*np.pi, 100)
                    y = np.sin(x + self.phase)
                    i.update(x, y, lstat)
                elif isinstance(i, BundleFigure1DWithWhiskers):
                    x = np.linspace(0, 6*np.pi, 100)
                    y = np.sin(x + self.phase)
                    base = x + 0.1
                    upper = 1.0 * y + 0.2
                    lower = 0.9 * y - 0.2
                    i.update(x, y, base, upper, lower, lstat)
                elif isinstance(i, BundleFigure2D):
                    x = np.linspace(0, 6*np.pi, 100)
                    y = np.linspace(0, 6*np.pi, 100)
                    xx, yy = np.meshgrid(x, y)
                    d = np.sin(xx + self.phase) * np.cos(yy + self.phase * 0.5)
                    i.update(d, np.min(x), np.max(x), np.min(y), np.max(y), lstat)
                elif isinstance(i, BundleImageRGBA):
                    pass
                else:
                    raise ValueError("Test not covered for bundle type {}".format(type(i)))



tester = FigureWidgetTester()

figs = list()
for i in tester.figure_bundles:
    figs.append(i.figure)

foo = column(*figs)
doc.add_root(foo)
