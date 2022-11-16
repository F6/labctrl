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

from .remote import RemoteHandlerThreeAxes


class GenericTextInput:
    pass


class GenericButton:
    pass


class GenericRadioButtonGroup:
    pass


class GenericFileInput:
    pass


class AbstractBundleSixSlots(ABC):
    """
    This bundle provides the following widgets and methods 
        to manipulate a 6-slot filter wheel
    """
    # Param Configs
    position_slot_list:     list[Union[GenericTextInput, BokehTextInput]]
    # Interactive Elements
    switch_to_slot_list:    list[Union[GenericButton, BokehButton]]
    # Composites
    remote_handler:         RemoteHandlerThreeAxes

    @abstractmethod
    def switch_to_slot(self, slot_index: int):
        pass


class AbstractBundleSingleFilterWheelAxis:
    """
    This bundle provides the following widgets and methods
        to set motion parameters of a single axis
        which a filter wheel is attached to:
    """
    # Param Configs
    working_unit:                   Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    scan_mode:                      Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    range_scan_start:               Union[GenericTextInput, BokehTextInput]
    range_scan_stop:                Union[GenericTextInput, BokehTextInput]
    range_scan_step:                Union[GenericTextInput, BokehTextInput]
    external_scan_list_file:        Union[GenericFileInput, BokehFileInput]
    position_unit:                  Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    zero_point_absolute_position:   Union[GenericTextInput, BokehTextInput]
    manual_unit:                    Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    manual_position:                Union[GenericTextInput, BokehTextInput]
    manual_step:                    Union[GenericTextInput, BokehTextInput]
    multiples:                      Union[GenericTextInput, BokehTextInput]
    soft_limit_min:                 Union[GenericTextInput, BokehTextInput]
    soft_limit_max:                 Union[GenericTextInput, BokehTextInput]
    working_direction:              Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    driving_speed_unit:             Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    driving_speed:                  Union[GenericTextInput, BokehTextInput]
    driving_acceleration_unit:      Union[GenericRadioButtonGroup,
                                          BokehRadioButtonGroup]
    driving_acceleration:           Union[GenericTextInput, BokehTextInput]
    # Interactive Elements
    manual_move:                    Union[GenericButton, BokehButton]
    manual_step_forward:            Union[GenericButton, BokehButton]
    manual_step_backward:           Union[GenericButton, BokehButton]
    # Composites
    slots:                          AbstractBundleSixSlots
    remote_handler:                 RemoteHandlerThreeAxes

    @abstractmethod
    def set_position(self, position: float):
        pass

    # Decorators
    # python.typing does not support annotation of decorators before 3.9
    # so probably I'll just leave it in the comment...
    # scan_range


class AbstractBundleFilterWheelController(ABC):
    """
    This bundle provides the following widgets and methods
        to set parameters of a 3-axis filter wheel controller
    """
    # Param Configs
    host:           Union[GenericTextInput, BokehTextInput]
    port:           Union[GenericTextInput, BokehTextInput]
    # Interactive Elements
    test_online:    Union[GenericButton, BokehButton]
    # Composites
    axis_0:         AbstractBundleSingleFilterWheelAxis
    axis_1:         AbstractBundleSingleFilterWheelAxis
    axis_2:         AbstractBundleSingleFilterWheelAxis
    remote_handler: RemoteHandlerThreeAxes
