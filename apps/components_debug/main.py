"""
a simple script to debug components like boxcar, etc.
"""
from threading import Thread
from functools import partial

import numpy as np
from bokeh.layouts import column, row


from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.lockin_and_boxcars.factory import FactoryBoxcarController
from labctrl.main_doc import doc
from labctrl.widgets.figure import FactoryFigure1D, FactoryFigure2D


boxcar_name = "generic_boxcar"

factory = FactoryBoxcarController()
boxcar = factory.generate_bundle(boxcar_name, lcfg, lstat)


class BoxcarPreviewFigure:
    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.signal = factory.generate_fig1d("Boxcar Signal", "Data #", "Intensity / V", 256)
        self.background = factory.generate_fig1d("Boxcar Background", "Data #", "Intensity / V", 256)
        self.delta = factory.generate_fig1d("Boxcar Delta", "Data #", "Intensity / V", 256)
        self.PWA = factory.generate_fig1d("PWA", "Time/us", "Intensity / V", 1024)


boxcarfigs = BoxcarPreviewFigure()

def data_updating_task():
    while True:
        if "Boxcar" == lstat.stat[boxcar_name]["Mode"]:
            data = boxcar.get_boxcar_data()
            ds = np.size(data)
            sig = data[:ds//2]
            bg = data[ds//2:]
            doc.add_next_tick_callback(partial(boxcarfigs.signal.callback_update, np.arange(ds//2), sig))
            doc.add_next_tick_callback(partial(boxcarfigs.background.callback_update, np.arange(ds//2), bg))
            doc.add_next_tick_callback(partial(boxcarfigs.delta.callback_update, np.arange(ds//2), sig-bg))
        elif "PWA" == lstat.stat[boxcar_name]["Mode"]:
            data = boxcar.get_PWA_data()
            ds = np.size(data)
            doc.add_next_tick_callback(partial(boxcarfigs.PWA.callback_update, np.linspace(0, ds//2, ds), data))



t = Thread(target=data_updating_task)
t.start()

cfigs = column(
    boxcarfigs.signal.fig,
    boxcarfigs.background.fig,
    boxcarfigs.delta.fig,
    boxcarfigs.PWA.fig,
)


r = row(boxcar.quick_control_group(), cfigs)

doc.add_root(r)
