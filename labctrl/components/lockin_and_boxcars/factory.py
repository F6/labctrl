# -*- coding: utf-8 -*-

"""factory.py:
This module provides the Factory class for Bokeh UI widgets for 
testing and controlling the boxcar integrator parameters

Breaking change: 
    ver 20221124 : refactored to use abstract model
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221124"


from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat

from .bundle_bokeh import BundleBokehBoxcar


class FactoryBoxcar:
    """
    This class is responsible for generating BundleBoxcar objects 
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
                "[SANITY] FactoryBoxcar: BundleBoxcar with name {} \
                    already generated before!".format(name))
        # if bundle_config[widget_package]==bokeh ->
        foo = BundleBokehBoxcar(
            bundle_config, self.lcfg, self.lstat)
        self.generated[name] = foo
        return foo
        # endif
