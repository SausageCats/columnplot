from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler

import tkinter as Tk
from columnplot.mappings import MapPlotBase


class ColumnPlotBase():

    def __init__(self, params):

        self._canvas = None
        self._figure = None
        self._toolbar = None
        self._window = None

        is_root = params['is_root']
        self._is_root = is_root
        self._rootwindow = None if is_root else params['rootwindow']
        self._title = params['title']

        # event
        self._geometry = params['geometry']
        self._linestyle = params['linestyle']
        self._marker = params['marker']
        self._marker1 = params['marker1']
        self._marker2 = params['marker2']
        self._show_grid = params['show_grid']
        self._show_marker = params['show_marker']
        self._show_msgs = params['show_msgs']
        self._show_toolbar = params['show_toolbar']

        self._mapbase = MapPlotBase(params)

#
# protected
#

    def _print(self, msg):
        if self._show_msgs:
            print(msg)

#
# protected
# event functions
#

    def _event_grid(self):
        self._show_grid = False if self._show_grid else True
        self.replot()

    def _event_linestyle(self, linestyle):
        self._linestyle = 'None' if self._linestyle == linestyle else linestyle
        self.replot()

    def _event_marker(self, marker):
        self._marker = '' if self._marker == marker else marker
        self._show_marker = False if self._marker == '' else True
        self.replot()

    def _event_quit(self, destroy_rootwindow=False):
        self._window.quit()     # stops mainloop
        self._window.destroy()  # this is necessary on Windows to prevent
        if destroy_rootwindow and self._rootwindow:
            self._rootwindow.quit()
            self._rootwindow.destroy()

    def _event_toolbar(self):
        self._show_toolbar = False if self._show_toolbar else True
        if self._show_toolbar:
            self._toolbar.pack(side=Tk.BOTTOM, fill=Tk.BOTH)
        else:
            self._toolbar.pack_forget()

# Not need events {{{
#
# from matplotlib import rcParams
#
#   def _event_home(self, event):
#     self._event_known('keymap.home', event)

#   def _event_zoom(self, event):
#     self._toolbar.zoom()
#     self._toolbar._set_cursor(event)
#   def _event_zoom(self, event):
#     self._event_known('keymap.zoom', event)

#   def _event_known(self, action, event):
#     try:
#       key = rcParams[action][0]
#       print(key)
#       if key:
#         event.key = key
#         key_press_handler(event, self._canvas, toolbar=self._toolbar)
#     except Exception:
#       pass
# }}}

    def _move_base_events(self, key, event):

        if key == self._mapbase.key_marker1:
            self._event_marker(self._marker1)
        elif key == self._mapbase.key_marker2:
            self._event_marker(self._marker2)
        elif key == self._mapbase.key_grid:
            self._event_grid()
        elif key == self._mapbase.key_linestyle:
            self._event_linestyle('-')
        elif key == self._mapbase.key_quit:
            self._event_quit()
        elif key == self._mapbase.key_quitall:
            self._event_quit(destroy_rootwindow=False if self._is_root else True)
        elif key == self._mapbase.key_toolbar:
            self._event_toolbar()
        else:
            key_press_handler(event, self._canvas, toolbar=self._toolbar)

#
# protected
# widget functions
#

    def _create_canvas(self, fig, window):
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()  # slow for a huge data???
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=True)
        self._canvas = canvas
        return canvas

    def _create_tk(self):
        if self._is_root:
            window = Tk.Tk()
            rootwindow = window
        else:
            window = Tk.Toplevel(self._rootwindow)
            rootwindow = self._rootwindow
        window.wm_title(self._title)
        window.geometry(self._geometry)
        self._window = window
        self._rootwindow = rootwindow
        return window, rootwindow

    def _set_events(self, canvas, fig):
        canvas.mpl_connect('key_press_event', self._on_key_press)
        fig.canvas.mpl_connect('button_press_event', self._on_mouse_press)
        fig.canvas.mpl_connect('button_release_event', self._on_mouse_release)

    def _set_toolbar(self, window, canvas):
        toolbar = NavigationToolbar2Tk(canvas, window)
#     toolbar.config(background='black')
        toolbar.update()
#     canvas._tkcanvas.pack(side=Tk.TOP, expand=True) # need??? something wrong with side option???
        if not self._show_toolbar:
            toolbar.pack_forget()
        self._toolbar = toolbar
        return toolbar

#
# public
#

    def get_params(self):

        params = dict()

        params['is_root'] = self._is_root
        params['rootwindow'] = self._rootwindow
        params['title'] = self._title

        params['geometry'] = self._geometry
        params['linestyle'] = self._linestyle
        params['marker'] = self._marker
        params['marker1'] = self._marker1
        params['marker2'] = self._marker2
        params['show_grid'] = self._show_grid
        params['show_marker'] = self._show_marker
        params['show_msgs'] = self._show_msgs
        params['show_toolbar'] = self._show_toolbar

        params.update(self._mapbase.get_params())

#     params['is_root'] = None
#     params['title'] = None
#     params['geometry'] = None

        return params

    def plot(self):

        self._on_plot_begin()

        window, rootwindow = self._create_tk()

        fig = Figure(figsize=(8, 6), dpi=100)
        self._create_graph(fig)
        self._figure = fig

        canvas = self._create_canvas(fig, window)
        self._set_toolbar(window, canvas)
        self._set_events(canvas, fig)

        self._on_plot_end()

        Tk.mainloop()

    def replot(self):
        fig = self._figure
        fig.clf()  # clear figure
        self._on_plot_begin()
        self._create_graph(fig)
        self._on_plot_end()
        self._canvas.draw()

#
# override
#

    def _create_graph(self, fig):
        pass

    def _on_plot_begin(self):
        pass

    def _on_plot_end(self):
        pass

    def _on_key_press(self, event):
        pass

    def _on_mouse_press(self, event):
        pass

    def _on_mouse_release(self, event):
        pass


if __name__ == '__main__':

    from config import create_columnplot_param
    params = create_columnplot_param()
    params['is_root'] = True
    params['title'] = 'ColumnPlotBase'
    params['geometry'] = params['geometry_plotsub']
    ColumnPlotBase(params).plot()
    exit()

    from config import create_columnplot_param
    from plotmain import ColumnPlotMain
    params = create_columnplot_param()
    params['data'] = [[3, 4, 5], [-0, -1, -2]]
    params['figtitle'] = ['y=x', 'y=-x']
    ColumnPlotMain(params).plot()


# vim:foldmethod=marker
