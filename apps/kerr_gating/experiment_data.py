



from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat

import numpy as np



class KerrGatingExpData:
    """Holds all temporary data generated in the experiment.
    The data memory are reallocated according to labconfig just before experiment
     starts. So it is necessary for the init to read the labconfig.
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat, ) -> None:
        # save a reference for later use. Each time lcfg get updated, expdata
        # instances are always lazy generated just before experiment starts,
        #  so no need to bother copying lcfg
        self.lcfg = lcfg
        delay_stage_name = lstat.stat["kerr_gating"]["DelayLine"]
        self.delays = lstat.stat[delay_stage_name]["ScanList"]
        self.ymin = np.min(self.delays)
        self.ymax = np.max(self.delays)
        self.signal = np.zeros(len(self.delays), dtype=np.float64)
        self.signal_sum = np.zeros(len(self.delays), dtype=np.float64)
        self.background = np.zeros(len(self.delays), dtype=np.float64)
        self.background_sum = np.zeros(len(self.delays), dtype=np.float64)
        self.delta = np.zeros(len(self.delays), dtype=np.float64)  # fig delay
        self.delta_stddev = np.zeros(
            len(self.delays), dtype=np.float64)  # fig delay
        self.delta_sum = np.zeros(len(self.delays), dtype=np.float64)

    def export(self, filestem: str) -> None:
        filename = filestem + "-Signal.csv"
        tosave = self.signal
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Signal.csv"
        tosave = self.signal_sum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Background.csv"
        tosave = self.background
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Background.csv"
        tosave = self.background_sum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delta.csv"
        tosave = self.delta
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Standard-Deviation-Delta.csv"
        tosave = self.delta
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Sum-Delta.csv"
        tosave = self.delta_sum
        np.savetxt(filename, tosave, delimiter=',')
        filename = filestem + "-Delays.csv"
        tosave = np.array(self.delays)
        np.savetxt(filename, tosave, delimiter=',')
