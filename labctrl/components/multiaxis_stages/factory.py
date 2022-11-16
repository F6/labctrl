# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling motorized filter wheel parameters

ver 20221106:
    init

ver 20221115:
    filter wheels are just multiaxis stages, modified multiaxis stages factory
    for filter wheels.

ver 20221116:
    because increasing size and complexity, add abstract class to better 
    define widgets needed.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221115"

from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat

from .bundle_bokeh import BundleBokehMultiAxisController


class FactoryMultiAxis:
    """
    This class is responsible for generating BundleFilterWheelController objects 
    from given params
    """

    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat
        self.generated = dict()

    def generate_bundle(self, bundle_config: dict):
        """
        actually generates the bundle
            bundle_config:  dict that contains all information needed to generate
                             the bundle
                            required fields: 
                                "Config" : config dict of target device

        for now only bokeh bundle is used, so direct generation, 
        if more are required, then the fork goes here
        """
        # sanity check
        name = bundle_config["Config"]["Name"]
        if name in self.generated:
            print(
                "[SANITY] FactoryMultiAxis: BundleMultiAxisController with name {} \
                    already generated before!".format(name))
        # if bundle_config[widget_package]==bokeh ->
        foo = BundleBokehMultiAxisController(
            bundle_config, self.lcfg, self.lstat)
        self.generated[name] = foo
        return foo
        # endif
