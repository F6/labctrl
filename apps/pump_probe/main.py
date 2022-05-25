# -*- coding: utf-8 -*-

"""main.py:
This module implements the
Pump-Probe transcient absorption spectroscopy
technic

In such experiment, an Optical Parametric Amplifier(OPA) is deployed
to selectively amplify a beam of supercontinuum white light to generate
an arbitrary wavelength laser pulse, which is called the pump pulse.
Another beam of supercontinuum white light generated with the same
seed pulse, which is weaker but spectrally wider, is called the probe pulse.

The pump pulse and probe pulse is aligned to simultaneously arrive at the
same spot on the sample at zero point. A delay line is put into the probe
pulse path to delay the probe pulse, typically about 10 fs to 10 ns, so the
pump pulse is first absorbed by the sample and excites the sample to its
excited state, then the probe pulse arrives and is absorbed by both ground
state sample molecules and excited state ones. The probe pulse is then
collected and analysed with spectrometer.

A chopper chops the pump pulse in sync with half of the laser repetition
frequency, so half of time the sample is pumped and probed, half of time
the sample is not pumped but probed. Subtracting the later from the previous
results in the optical absorption change (delta O. D.), which is correlated
with change of population in excited states and ground state over time. 

"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20220525"


import time

from bokeh.layouts import column, row
from bokeh.models.widgets import Button, Div
from bokeh.models import Panel, Tabs

from labctrl.labconfig import lcfg
from labctrl.labstat import lstat
from labctrl.components.linear_stages.factory import FactoryLinearStage
from labctrl.main_doc import doc
from labctrl.dashboard import taskoverview
from labctrl.methods.generic import FactoryGenericMethods
from labctrl.methods.figure import FactoryFigure1D

doc.template_variables["app_name"] = "pump_probe"

factory = FactoryLinearStage()
linear_stage = factory.generate_bundle(
    lcfg.config["linear_stages"]["USB1020"], lcfg, lstat)

factory = FactoryGenericMethods()
gschedule = factory.generate(lcfg, lstat)



class PumpProbePreviewFigure:
    def __init__(self) -> None:
        factory = FactoryFigure1D()
        self.signal = factory.generate_fig1d(
            "Kerr Gate Scan", "Time (ps)", "Boxcar Delta (V)", 40)


class KerrGateExpData:
    """Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.
    """

    def __init__(self, lcfg, lstat) -> None:
        # save a reference for later use. Each time lcfg get updated, expdata
        # instances are always lazy generated just before experiment starts,
        #  so no need to bother copying lcfg
        self.lcfg = lcfg
        self.delays = lstat.stat[dlname]["ScanList"]
        self.sig = np.zeros(len(self.delays), dtype=np.float64)
        self.sigsum = np.zeros(len(self.delays), dtype=np.float64)

    def export(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        tosave = self.sig
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        tosave = self.sigsum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delays.csv"
        tosave = np.array(self.delays)
        np.savetxt(filename, tosave, delimiter=',')

class BundleKerrGating:
    """
    this holds all the UI widgets, unit operations and thread 
    tasks for the experiment
    """
    def __init__(self) -> None:
        init_str = 'Initialize at {}'.format(self)
        self.start = Button(label="Start Kerr Gate Scan", button_type='success')
        # self.pause = Button(label="Pause Kerr Gate Scan", button_type='warning')
        self.terminate = Button(label="Terminate Kerr Gate Scan", button_type='warning')
        self.preview = KerrGatePreviewFig()
        self.generic = None
        self.delayline = None
        self.boxcar = None
        self.data = None
        self.unit_operation = None
        self.task = None
        self.flags = {
            "RUNNING": False,
            # "PAUSE": False,
            "TERMINATE": False,
            "FINISH": False,
        }

    def quick_control_group(self):
        return row(
            column(
            self.generic.quick_control_group(),
            # self.delayline.quick_control_group(),
            # self.boxcar.quick_control_group(),
            self.start,
            # self.pause,
            self.terminate),
            self.preview.signal.fig,
        )

class FactoryKerrGating:
    def __init__(self) -> None:
        pass

    def generate(self, bundle_linearstage, bundle_boxcar, lcfg, lstat) -> BundleKerrGating:
        """
        requires:
            bundle_linearstage -> must implement @scan_delay decorator
            bundle_boxcar -> must implement get_value function for single point detection
        """

        bundle = BundleKerrGating()
        bundle.delayline = bundle_linearstage
        bundle.boxcar = bundle_boxcar

        factory = FactoryGenericMethods()
        bundle.generic = factory.generate(lcfg, lstat)

        scan_round = bundle.generic.scan_round
        scan_delay = bundle.delayline.scan_delay


        @scan_round
        @scan_delay
        def unit_operation(meta=dict()):
            if bundle.flags["TERMINATE"]:
                meta["TERMINATE"] = True
                lstat.expmsg("kerr_gating received signal TERMINATE, trying graceful Thread exit")
                return
            lstat.expmsg("Retriving signal from Lock-in amplifier data server")
            sig = bundle.boxcar.get_value()
            lstat.expmsg("Adding latest signal to dataset...")
            stat = lstat.stat[dlname]
            bundle.data.sig[stat["iDelay"]] = sig
            bundle.data.sigsum[stat["iDelay"]] += sig
            lstat.doc.add_next_tick_callback(
                partial(bundle.preview.signal.callback_update, stat["ScanList"], bundle.data.sig))
            # if this the end of delay scan, call export
            if stat["iDelay"] + 1 == len(stat["ScanList"]):
                bundle.data.export("scandata/" + lcfg.config["basic"]["FileStem"] +
                            "-Round{rd}".format(rd=lstat.stat["basic"]["iRound"]))

        bundle.unit_operation = unit_operation

        def task():
            lstat.expmsg("Allocating memory for experiment")
            bundle.data = KerrGateExpData(lcfg, lstat)
            lstat.expmsg("Starting experiment")
            meta = dict()
            meta["TERMINATE"] = False
            bundle.unit_operation(meta=meta)
            bundle.flags["FINISH"] = True
            bundle.flags["RUNNING"] = False
            lstat.expmsg("Experiment done")

        bundle.task = task

        def __callback_start():
            bundle.flags["TERMINATE"] = False
            bundle.flags["FINISH"] = False
            bundle.flags["RUNNING"] = True
            thread = Thread(target=bundle.task)
            thread.start()

        bundle.start.on_click(__callback_start)

        def __callback_terminate():
            lstat.expmsg("Terminating current job")
            bundle.flags["TERMINATE"] = True
            bundle.flags["FINISH"] = False
            bundle.flags["RUNNING"] = False

        bundle.terminate.on_click(__callback_terminate)

        return bundle




# roots: ["dashboard", "setup", "params", "schedule", "reports", "messages"]
# messages are directly put at labstat, so dismissed here
# ================ dashboard ================
dashboard_tab1 = Panel(child=taskoverview.div, title="Tasks")
dashboard_tabs = Tabs(tabs=[dashboard_tab1], name="dashboard")
doc.add_root(dashboard_tabs)

# ================ params ================
foo = column(
    linear_stage.scan_mode,
    linear_stage.scan_zero,
    linear_stage.scan_start,
    linear_stage.scan_stop,
    linear_stage.scan_step,
    linear_stage.scan_file
)
param_tab1 = Panel(child=foo, title="Linear Stage")
param_tabs = Tabs(tabs=[param_tab1], name="param")
doc.add_root(param_tabs)

# ================ manual ================
foo = column(
    linear_stage.test_online,
    linear_stage.manual_position,
    linear_stage.manual_move,
    linear_stage.manual_step,
    linear_stage.manual_step_forward,
    linear_stage.manual_step_backward,
)
manual_tab1 = Panel(child=foo, title="Linear Stage")
manual_tabs = Tabs(tabs=[manual_tab1], name="manual")
doc.add_root(manual_tabs)

# ================ schedule ================
foo = column(
    gschedule.filestem,
    gschedule.scanrounds,
    kerrgate.start,
    kerrgate.terminate
)
schedule_tab1 = Panel(child=foo, title="Kerr Gate")
schedule_tabs = Tabs(tabs=[schedule_tab1], name="schedule")
doc.add_root(schedule_tabs)

# ================ reports ================
foo = column(
    kerrgate.preview.signal.fig
)
reports_tab1 = Panel(child=foo, title="Kerr Gate")
reports_tabs = Tabs(tabs=[reports_tab1], name="reports")
doc.add_root(reports_tabs)