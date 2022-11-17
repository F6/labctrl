# -*- coding: utf-8 -*-

"""
figure.py:

This module implements figure widget bundles for components and apps.

20221117: refactor: change seperated factories into one factory that generates
                    all sorts of figure bundles.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20221115"


import numpy as np
from functools import partial
from abc import ABC, abstractmethod
from typing import Union, NewType, Any
from bokeh.plotting import Figure as BokehFigure
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, LinearColorMapper, Range1d, Whisker
from tornado import gen

from labctrl.labconfig import LabConfig
from labctrl.labstat import LabStat

from .generic import GenericFigure
from .mandelbrot import mandelbrot_image


class AbstractBundleFigure(ABC):
    """
    [TODO]: implement abstract class as a base class for bundles. For now only bokeh bundles are used so 
            temporarily leave it here (unused).
    """
    figure:     Union[GenericFigure, BokehFigure]


class AbstractBundleFigure1D(AbstractBundleFigure):
    @abstractmethod
    def update(self, x, y, lstat: LabStat):
        pass


class AbstractBundleFigure1DWithWhiskers(AbstractBundleFigure):
    @abstractmethod
    def update(self, x, y, base, upper, lower, lstat: LabStat):
        pass


class AbstractBundleFigure2D(AbstractBundleFigure):
    @abstractmethod
    def update(self, d, xmin: float, xmax: float, ymin: float, ymax: float, lstat: LabStat):
        pass


class AbstractBundleImageRGBA(AbstractBundleFigure):
    @abstractmethod
    def update(self, new_img, xmin: float, xmax: float, ymin: float, ymax: float, lstat: LabStat):
        pass


class FactoryFigure:
    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat

    def generate_bundle(self, bundle_config: dict):
        figure_type: str = bundle_config["FigureType"]
        if figure_type == "1D":
            return self.generate_bundle_figure_1d(bundle_config)
        elif figure_type == "2D":
            return self.generate_bundle_figure_2d(bundle_config)
        elif figure_type == "Image":
            return self.generate_bundle_figure_image_RGBA(bundle_config)
        else:
            raise ValueError(
                "Unknown figure type to generate: {}".format(figure_type))

    def generate_bundle_figure_1d(self, bundle_config: dict):
        title = bundle_config["Title"]
        x_name = bundle_config["XName"]
        y_name = bundle_config["YName"]
        # Load default values if not present in config
        plot_height = bundle_config["PlotHeight"] if "PlotHeight" in bundle_config else 360
        plot_width = bundle_config["PlotWidth"] if "PlotWidth" in bundle_config else 640
        if "Whiskers" in bundle_config:
            if bundle_config["Whiskers"]:
                return BundleFigure1DWithWhiskers(title, x_name, y_name, plot_width, plot_height)
        return BundleFigure1D(title, x_name, y_name, plot_width, plot_height)

    def generate_bundle_figure_2d(self, bundle_config: dict):
        title = bundle_config["Title"]
        x_name = bundle_config["XName"]
        y_name = bundle_config["YName"]
        d_name = bundle_config["DataName"]
        # Load default values if not present in config
        plot_height = bundle_config["PlotHeight"] if "PlotHeight" in bundle_config else 640
        plot_width = bundle_config["PlotWidth"] if "PlotWidth" in bundle_config else 640
        return BundleFigure2D(title, x_name, y_name, d_name, plot_width, plot_height)

    def generate_bundle_figure_image_RGBA(self, bundle_config: dict):
        title = bundle_config["Title"]
        x_name = bundle_config["XName"]
        y_name = bundle_config["YName"]
        # Load default values if not present in config
        plot_height = bundle_config["PlotHeight"] if "PlotHeight" in bundle_config else 360
        plot_width = bundle_config["PlotWidth"] if "PlotWidth" in bundle_config else 640
        return BundleImageRGBA(title, x_name, y_name, plot_width, plot_height)


class BundleFigure1D(AbstractBundleFigure1D):
    def __init__(self, title: str, x_name: str, y_name: str, plot_width: int, plot_height: int) -> None:
        spectrum_tools = "box_zoom,pan,undo,redo,reset,save,crosshair"
        length = 100  # the length does not matter because every update resets the length
        self.figure = figure(title=title, x_axis_label=x_name,
                             y_axis_label=y_name, plot_width=plot_width,
                             plot_height=plot_height, tools=spectrum_tools)
        self.y = np.zeros(length)
        self.x = np.array(range(length))
        self.ds = ColumnDataSource(data=dict(x=self.x, y=self.y))
        self.line = self.figure.line('x', 'y', line_width=1, source=self.ds)
        ht = HoverTool(
            tooltips=[
                (x_name, '@x{0.000000}'),
                (y_name, '@y{0.000000}'),
            ],
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='vline'
        )
        self.figure.add_tools(ht)

    @gen.coroutine
    def callback_update(self, x, y):
        new_data = dict()
        new_data['x'] = x
        new_data['y'] = y
        self.ds.data = new_data

    def update(self, x, y, lstat: LabStat):
        lstat.doc.add_next_tick_callback(partial(self.callback_update, x, y))


class BundleFigure1DWithWhiskers(AbstractBundleFigure1DWithWhiskers):
    def __init__(self, title: str, x_name: str, y_name: str, plot_width: int, plot_height: int) -> None:
        spectrum_tools = "box_zoom,pan,undo,redo,reset,save,crosshair"
        length = 100
        self.figure = figure(title=title, x_axis_label=x_name,
                          y_axis_label=y_name, plot_width=plot_width,
                          plot_height=plot_height, tools=spectrum_tools)
        self.y = np.zeros(length)
        self.x = np.arange(length)
        self.base = np.arange(length)
        self.upper = np.zeros(length)
        self.lower = np.zeros(length)
        self.ds = ColumnDataSource(data=dict(
            x=self.x, y=self.y, base=self.base, upper=self.upper, lower=self.lower))
        self.line = self.figure.line('x', 'y', line_width=1, source=self.ds)
        ht = HoverTool(
            tooltips=[
                (x_name, '@x{0.000000}'),
                (y_name, '@y{0.000000}'),
            ],
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='vline'
        )
        self.figure.add_tools(ht)
        self.figure.add_layout(
            Whisker(source=self.ds, base="base", upper="upper", lower="lower"))

    @gen.coroutine
    def callback_update(self, x, y, base, upper, lower):
        new_data = dict()
        new_data['x'] = x
        new_data['y'] = y
        new_data['base'] = base
        new_data['upper'] = upper
        new_data['lower'] = lower
        self.ds.data = new_data

    def update(self, x, y, base, upper, lower, lstat: LabStat):
        lstat.doc.add_next_tick_callback(partial(
            self.callback_update,
            x, y, base, upper, lower
        ))


class BundleFigure2D(AbstractBundleFigure2D):
    def __init__(self, title: str, x_name: str, y_name: str, d_name: str, plot_width: int, plot_height: int) -> None:
        spectrum_tools = "box_zoom,pan,undo,redo,reset,save,crosshair"
        self.figure = figure(title=title, x_axis_label=x_name,
                             y_axis_label=y_name, plot_width=plot_width,
                             plot_height=plot_height, tools=spectrum_tools)
        # This rules out slow computers haha
        self.d = mandelbrot_image(width=128, height=128)
        self.ds = ColumnDataSource({
            'image': [self.d],
            'x': [-2],
            'y': [-1.5],
            'dw': [3],
            'dh': [3]
        })
        self.figure.x_range = Range1d(-2, 1)
        self.figure.y_range = Range1d(-1.5, 1.5)
        # you can choose palettes you like, list see https://docs.bokeh.org/en/2.4.3/docs/reference/palettes.html
        color_mapper = LinearColorMapper(palette="Viridis256")
        self.img = self.figure.image(image='image', source=self.ds,
                                     x='x', y='y', dw='dw', dh='dh', color_mapper=color_mapper)
        self.color_bar = ColorBar(color_mapper=color_mapper, title=d_name)
        self.figure.add_layout(self.color_bar, 'right')
        ht = HoverTool(
            tooltips=[
                (x_name, '$x{0.000000}'),
                (y_name, '$y{0.000000}'),
                ("data", '@image{0.000000}')
            ],
            # display a tooltip only when the mouse is directly over a glyph
            mode='mouse'
        )
        self.figure.add_tools(ht)

    @gen.coroutine
    def callback_update(self, d, xmin: float, xmax: float, ymin: float, ymax: float):
        new_data = dict()
        new_data['image'] = [d]
        new_data['x'] = [xmin]
        new_data['y'] = [ymin]
        new_data['dw'] = [xmax - xmin]
        new_data['dh'] = [ymax - ymin]
        self.ds.data = new_data
        self.figure.x_range.start = xmin
        self.figure.x_range.end = xmax
        self.figure.y_range.start = ymin
        self.figure.y_range.end = ymax

    def update(self, d, xmin: float, xmax: float, ymin: float, ymax: float, lstat: LabStat):
        lstat.doc.add_next_tick_callback(partial(
            self.callback_update,
            d, xmin, xmax, ymin, ymax
        ))

    # TODO: implement interplolation for not width-equal-spaced height-equal-spaced images

    def interpolate_for_equal_space():
        """
        Most 2D spectrums have x-axis or y-axis not equally spaced, for example delays in pump probe spectroscopy
        Thus it is necessary to interpolate the image, and resample the interplolated image to plot it correctly
          to a grid. This is also sometimes called a data griding.
        """
        pass


class BundleImageRGBA(AbstractBundleImageRGBA):
    def __init__(self, title: str, x_name: str, y_name: str, plot_width: int, plot_height: int) -> None:
        spectrum_tools = "box_zoom,pan,undo,redo,reset,save,crosshair"
        self.figure = figure(title=title, x_axis_label=x_name,
                          y_axis_label=y_name, plot_width=plot_width,
                          plot_height=plot_height, tools=spectrum_tools)
        self.d = np.zeros((100, 100), dtype=np.uint32)
        self.ds = ColumnDataSource({
            'image': [self.d],
            'x': [0],
            'y': [0],
            'dw': [1],
            'dh': [1]
        })
        self.figure.x_range = Range1d(-2, 1)
        self.figure.y_range = Range1d(-1.5, 1.5)
        self.img = self.figure.image_rgba(
            image='image', source=self.ds, x='x', y='y', dw='dw', dh='dh')
        ht = HoverTool(
            tooltips=[
                (x_name, '$x{0.000000}'),
                (y_name, '$y{0.000000}'),
                ("data", '@image{0.000000}')
            ],
            # display a tooltip only when the mouse is directly over a glyph
            mode='mouse'
        )
        self.figure.add_tools(ht)

    @gen.coroutine
    def callback_update(self, new_img, xmin, xmax, ymin, ymax):
        """
        Converts opencv format img to bokeh format and updates ColumnDataSource
            ''After investigation, the return result from OpenCV is a Numpy array of 
                bytes with shape (M, N, 3), i.e. RGB tuples. What Bokeh expects is a 
                Numpy array of shape (M, N) 32-bit integers representing RGBA values. 
                So you need to convert from one format to the other.''
        """
        M, N, _ = new_img.shape
        img = np.empty((M, N), dtype=np.uint32)
        view = img.view(dtype=np.uint8).reshape((M, N, 4))
        view[:, :, 0] = new_img[:, :, 2]  # copy red channel
        view[:, :, 1] = new_img[:, :, 1]  # copy blue channel
        view[:, :, 2] = new_img[:, :, 0]  # copy green channel
        view[:, :, 3] = 255
        new_data = dict()
        new_data['image'] = [img]
        new_data['x'] = [xmin]
        new_data['y'] = [ymin]
        new_data['dw'] = [xmax - xmin]
        new_data['dh'] = [ymax - ymin]
        self.ds.data = new_data
        self.figure.x_range.start = xmin
        self.figure.x_range.end = xmax
        self.figure.x_range.reset_start = xmin
        self.figure.x_range.reset_end = xmax
        self.figure.y_range.start = ymin
        self.figure.y_range.end = ymax
        self.figure.y_range.reset_start = ymin
        self.figure.y_range.reset_end = ymax

    def update(self, new_img, xmin: float, xmax: float, ymin: float, ymax: float, lstat: LabStat):
        lstat.doc.add_next_tick_callback(partial(
            self.callback_update,
            new_img, xmin, xmax, ymin, ymax
        ))