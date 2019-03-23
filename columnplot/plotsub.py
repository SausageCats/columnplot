from columnplot.plotbase import ColumnPlotBase


class ColumnPlotSub(ColumnPlotBase):

    def __init__(self, params):

        params['geometry'] = params['geometry_plotsub']
        params['is_root'] = False
        params['title'] = params['title'] if 'title' in params else 'ColumnPlotSub'
        super().__init__(params)

        self._data = params['data']
        self._figtitle = params['figtitle']
        self._xcoord = params['xcoord']

#
# override
#

    def _on_key_press(self, event):
        key = event.key
        self._move_base_events(key, event)

    def _create_graph(self, fig):
        fig.subplots_adjust(left=0.10, bottom=0.1, right=0.95, top=0.95, wspace=0.3, hspace=0.3)
        f = fig.add_subplot('111')
        f.grid(self._show_grid)
#     f.set_title(' || '.join(self._figtitle))
        if self._xcoord:
            for data in self._data:
                f.plot(self._xcoord, data, marker=self._marker, linestyle=self._linestyle)
        else:
            for data in self._data:
                f.plot(data, marker=self._marker, linestyle=self._linestyle)
        f.legend(labels=self._figtitle, loc='upper right')


if __name__ == '__main__':

    from config import create_columnplot_param
    params = create_columnplot_param()

    params['rootwindow'] = ''
    params['xcoord'] = list()

    params['data'] = [[0, 1, 2], [-0, -1, -2]]
    params['figtitle'] = ['y=x', 'y=-x']

    ColumnPlotSub(params).plot()
