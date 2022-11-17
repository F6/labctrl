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
__version__ = "20221115"

from abc import ABC, abstractmethod
from typing import Union, NewType, Any

from bokeh.models.widgets import TextInput as BokehTextInput
from bokeh.models.widgets import Button as BokehButton
from bokeh.models.widgets import RadioButtonGroup as BokehRadioButtonGroup
from bokeh.models.widgets import FileInput as BokehFileInput

from labctrl.widgets.generic import (
    GenericButton, GenericRadioButtonGroup, GenericTextInput)
from labctrl.widgets.figure import AbstractBundleImageRGBA


from .remote import RemoteCamera


class AbstractBundleCamera(ABC):
    """
    This bundle provides the following widgets and methods
        to set working parameters and interact with a
        camera sensor (2D array image sensors in general):
    """
    # Param Configs
    host:                               Union[GenericTextInput, BokehTextInput]
    port:                               Union[GenericTextInput, BokehTextInput]
    working_mode:                       Union[GenericRadioButtonGroup,
                                              BokehRadioButtonGroup]
    change_working_mode:                Union[GenericButton, BokehButton]
    exposure_time_unit:                 Union[GenericRadioButtonGroup,
                                              BokehRadioButtonGroup]
    exposure_time:                      Union[GenericTextInput, BokehTextInput]
    change_exposure_time:               Union[GenericButton, BokehButton]

    # Interactive Elements
    test_online:                        Union[GenericButton, BokehButton]
    apply_all_settings:                 Union[GenericButton, BokehButton]
    manual_take_sample:                 Union[GenericButton, BokehButton]
    start_continuous_video_streaming:   Union[GenericButton, BokehButton]
    stop_continuous_video_streaming:    Union[GenericButton, BokehButton]
    # Composite
    preview_figure:                     AbstractBundleImageRGBA
    # Other
    remote:                             RemoteCamera

    @abstractmethod
    def get_image(self):
        pass
