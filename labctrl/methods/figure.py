
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from tornado import gen


class BundleFigure1D:
    def __init__(self, title: str, x: str, y: str, length: int) -> None:
        spectrum_tools = "box_zoom,wheel_zoom,undo,redo,reset,save,crosshair,hover"
        self.fig = figure(title=title, x_axis_label=x,
                          y_axis_label=y, plot_width=700, plot_height=360, tools=spectrum_tools)
        self.y = np.zeros(length)
        self.x = np.array(range(length))
        self.ds = ColumnDataSource(data=dict(x=self.x, y=self.y))
        self.line = self.fig.line('x', 'y', line_width=1, source=self.ds)

    @gen.coroutine
    def callback_update(self, x, y):
        new_data = dict()
        new_data['x'] = x
        new_data['y'] = y
        self.ds.data = new_data


class FactoryFigure1D:
    def __init__(self) -> None:
        pass

    def generate_fig1d(self, title, x, y, length):
        return BundleFigure1D(title, x, y, length)

# TODO
# class BundleFigure2D:
#     def __init__(self, title: str, x: str, y: str, length: int) -> None:
#         spectrum_tools = "box_zoom,wheel_zoom,undo,redo,reset,save,crosshair,hover"
#         self.fig = figure(title=title, x_axis_label=x,
#                           y_axis_label=y, plot_width=700, plot_height=360, tools=spectrum_tools)
#         self.y = np.zeros(length)
#         self.x = np.array(range(length))
#         self.ds = ColumnDataSource(data=dict(x=self.x, y=self.y))
#         self.line = self.fig.line('x', 'y', line_width=1, source=self.ds)

#     @gen.coroutine
#     def callback_update(self, x, y):
#         new_data = dict()
#         new_data['x'] = x
#         new_data['y'] = y
#         self.ds.data = new_data
