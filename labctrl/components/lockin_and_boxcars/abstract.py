# -*- coding: utf-8 -*-

"""
abstract.py:

This module provides the abstract class to define the generated widget bundle
from factory.

The abstract class forces widget bundles to contain all members and methods 
listed in the abstract class, no matter what type of bundle it is (bokeh, Qt,
or other frameworks). This provides a consistant way for higher level layouters
to organize widgets.

If new widget type is needed, use typing.Union to add new type to the abstract
class. The type added here does not change runtime behaviour because python
is dynamic, it just helps type checking systems to work.

Note that a backup 'Generic' widget type is always in the type union, because
some widgets are special to one or several packages, for example you cannot find
3D object widgets in Bokeh, then you cannot have 3D objects in your Bokeh app,
but they do exist in other apps. When this happens, the 'Generic' widget acts as a
fallback for layouters to place placeholders or compatible element if the desired
widget is not present in current package enviroment, so that we don't have to change
the layouter program everytime some new unique widget is added.

Supported widget types are followed after the 'Generic' type.

Note that __callback's are not listed in the bundle, because __callback's are
always package-specific. The bundle only cares what elements may be useful to the
user, but doesn't care about how the elements work, or will the elements work.
This enables us to only generate the widgets but does not in fact implement them,
this accelerates prototype development in the lab. Not implemented widgets can
be disabled in the frontend, and they can be implemented when we actually uses 
that function.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221122"

from abc import ABC, abstractmethod
from typing import Any, NewType, Union

from bokeh.models.widgets import Button as BokehButton
from bokeh.models.widgets import FileInput as BokehFileInput
from bokeh.models.widgets import RadioButtonGroup as BokehRadioButtonGroup
from bokeh.models.widgets import TextInput as BokehTextInput

from labctrl.widgets.generic import (GenericButton, GenericFileInput,
                                     GenericRadioButtonGroup, GenericTextInput)
from labctrl.widgets.figure import AbstractBundleFigure1D

class AbstractBundleBoxcar(ABC):
    """
    This bundle provides the following widgets and methods
        to set motion parameters of and interact with a linear stage:
    """
    # Param Configs
    host:                           Union[GenericTextInput, BokehTextInput]
    port:                           Union[GenericTextInput, BokehTextInput]
    working_unit:                   Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    delay_background_sampling:      Union[GenericTextInput, BokehTextInput]
    delay_integrate:                Union[GenericTextInput, BokehTextInput]
    delay_hold:                     Union[GenericTextInput, BokehTextInput]
    delay_signal_sampling:          Union[GenericTextInput, BokehTextInput]
    delay_reset:                    Union[GenericTextInput, BokehTextInput]
    working_mode:                   Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    # Interactive Elements
    test_online:                    Union[GenericButton, BokehButton]
    submit_config:                  Union[GenericButton, BokehButton]
    set_working_mode:               Union[GenericButton, BokehButton]
    manual_get_boxcar_data:         Union[GenericButton, BokehButton]
    manual_get_PWA_data:            Union[GenericButton, BokehButton]
    start_PWA:                      Union[GenericButton, BokehButton]
    stop_PWA:                       Union[GenericButton, BokehButton]
    # Composite
    PWA_figure:                     AbstractBundleFigure1D
    # Other

    @abstractmethod
    def get_boxcar_data(self, n_samples: int):
        pass

    @abstractmethod
    def get_PWA_data(self, n_samples: int):
        pass
