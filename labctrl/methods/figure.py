
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, LinearColorMapper, Range1d
from tornado import gen
from .mandelbrot import mandelbrot_image

class BundleFigure1D:
    def __init__(self, title: str, x: str, y: str, length: int) -> None:
        spectrum_tools = "box_zoom,pan,undo,redo,reset,save,crosshair"
        self.fig = figure(title=title, x_axis_label=x,
                          y_axis_label=y, plot_width=700, plot_height=360, tools=spectrum_tools)
        self.y = np.zeros(length)
        self.x = np.array(range(length))
        self.ds = ColumnDataSource(data=dict(x=self.x, y=self.y))
        self.line = self.fig.line('x', 'y', line_width=1, source=self.ds)
        ht = HoverTool(
            tooltips=[
                ( x, '@x{0.000000}'  ),
                ( y, '@y{0.000000}'  ),
            ],
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='vline'
        )
        self.fig.add_tools(ht)

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


class BundleFigure2D:
    def __init__(self, title: str, xname: str, yname: str, dname: str) -> None:
        spectrum_tools = "box_zoom,pan,undo,redo,reset,save,crosshair"
        self.fig = figure(title=title, x_axis_label=xname,
                          y_axis_label=yname, plot_width=700, plot_height=640, tools=spectrum_tools)
        self.d = mandelbrot_image(width=128, height=128) # This rules out slow computers haha
        self.ds = ColumnDataSource({
            'image': [self.d],
            'x' : [-2],
            'y' : [-1.5],
            'dw' : [3],
            'dh' : [3]
            })
        self.fig.x_range = Range1d(-2, 1)
        self.fig.y_range = Range1d(-1.5, 1.5)
        # you can choose palettes you like, list see https://docs.bokeh.org/en/2.4.3/docs/reference/palettes.html
        color_mapper = LinearColorMapper(palette="Viridis256")
        self.img = self.fig.image(image='image', source=self.ds, x='x', y='y', dw='dw', dh='dh', color_mapper=color_mapper)
        self.color_bar = ColorBar(color_mapper=color_mapper, title=dname)
        self.fig.add_layout(self.color_bar, 'right')
        ht = HoverTool(
            tooltips=[
                ( xname, '$x{0.000000}'  ),
                ( yname, '$y{0.000000}'  ),
                ( "data", '@image{0.000000}' )
            ],
            # display a tooltip only when the mouse is directly over a glyph
            mode='mouse'
        )
        self.fig.add_tools(ht)

    @gen.coroutine
    def callback_update(self, d, xmin, xmax, ymin, ymax):
        new_data = dict()
        new_data['image'] = [d]
        new_data['x'] = [xmin]
        new_data['y'] = [ymin]
        new_data['dw'] = [xmax - xmin]
        new_data['dh'] = [ymax - ymin]
        self.ds.data = new_data
        self.fig.x_range.start = xmin
        self.fig.x_range.end = xmax
        self.fig.y_range.start = ymin
        self.fig.y_range.end = ymax

    # TODO: implement interplolation for not width-equal-spaced height-equal-spaced images
    def interpolate_for_equal_space():
        """
        Most 2D spectrums have x-axis or y-axis not equally spaced, for example delays in pump probe spectroscopy
        Thus it is necessary to interpolate the image, and resample the interplolated image to plot it correctly
          to a grid. This is also sometimes called a data griding.
        """
        pass

class FactoryFigure2D:
    def __init__(self) -> None:
        pass

    def generate_fig2d(self, title, xname, yname, dname):
        return BundleFigure2D(title, xname, yname, dname)