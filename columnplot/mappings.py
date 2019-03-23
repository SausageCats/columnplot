#!/usr/bin/env python3

#
# call from ColumnPlotBase constructor
#


class MapPlotBase(object):

    def __init__(self, params):
        self.key_marker1 = params['key_marker1']
        self.key_marker2 = params['key_marker2']
        self.key_grid = params['key_grid']
        self.key_linestyle = params['key_linestyle']
        self.key_quit = params['key_quit']
        self.key_quitall = params['key_quitall']
        self.key_toolbar = params['key_toolbar']

    def get_params(self):
        return self.__dict__

#
# call from ColumnPlotMain constructor
#


class MapPlotMain(object):

    def __init__(self, params):
        self.key_plotsub = params['key_plotsub']
        self.key_xcoord = params['key_xcoord']
        self.mouse_plotsub = params['mouse_plotsub']
        self.mouse_xcoord = params['mouse_xcoord']

    def get_params(self):
        return self.__dict__


#
# main
#


if __name__ == '__main__':
    from config import create_columnplot_param
    params = create_columnplot_param()
    key = MapPlotBase(params)

    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(key.get_params())
