import re
import math
from columnplot.variables import INVALID_DATA

from columnplot.plotbase import ColumnPlotBase
from columnplot.plotsub import ColumnPlotSub

from columnplot.mappings import MapPlotMain


class ColumnPlotMain(ColumnPlotBase):

    def __init__(self, params):

        params['geometry'] = params['geometry_plotmain']
        params['is_root'] = True
        params['title'] = 'ColumnPlotMain'
        super().__init__(params)

        self._data = params['data']
        self._filename = params['filename']
        self._geometry_plotsub = params['geometry_plotsub']
        self._figtitle = params['figtitle']

        # on single graph selection
        self.__event_key = ''
        self.__is_figselect = False
        self.__inp_fignr = ''
        self.__fignrlist = self.__get_valid_fignr()

        # on multiple graph selection
        self.__fignrlist_mosemode = list()

        # on x coordinate selection
        self.__basetitle = self._title
        self.__is_xcoord_select = False
        self.__xcoordnr_ini = -1
        self.__xcoordnr = self.__xcoordnr_ini

        self.__mapmain = MapPlotMain(params)

#
# private
#

    def __get_figtitle(self, idx):  # {{{
        try:
            title = self._figtitle[idx]
        except IndexError:
            title = ''
        return title
#  }}}

    def __get_plotsize(self, n_data):  # {{{
        n_col = int(math.ceil(math.sqrt(n_data)))
        n_row = 1
        while True:
            n_data -= n_col
            if n_data <= 0:
                break
            n_row += 1
        return n_row, n_col
#  }}}

    def __get_valid_fignr(self):  # {{{
        valid_fignr = list()
        for i in range(len(self._data)):
            if self._data[i][0] != INVALID_DATA:
                valid_fignr.append(i + 1)  # figure number starts from 1 not 0
        return valid_fignr
#  }}}

#
# prviate
# functions called from key and mouse events
#

    def __check_fignr(self, fignr_anytype):  # {{{
        if isinstance(fignr_anytype, str):
            # Here is called from key event
            if int(fignr_anytype) not in self.__fignrlist:
                self.__cancel_event(msg='Invalid number ({})'.format(fignr_anytype), call_raise=True)
        elif isinstance(fignr_anytype, list):
            # Here is called from mouse event
            for fignr in fignr_anytype:
                if fignr + 1 in self.__fignrlist:
                    break
            else:
                return False
            return True
# }}}

    def __create_params(self, fignrs):  # {{{

        params = dict()
        params = self.get_params()

        params['geometry_plotsub'] = self._geometry_plotsub
        params['data'] = [self._data[nr] for nr in fignrs]
        params['figtitle'] = [self._figtitle[nr] for nr in fignrs]
        params['title'] = 'ColumnPlotSub (file={})'.format(self._filename)
        params['xcoord'] = self._data[self.__xcoordnr] if self.__is_xcoord_select else list()

        return params
# }}}

    def __merge_graphs(self, fignr_anytype):  # {{{

        # need to call __check_fignr function before calling this function

        fignrs = list()
        if isinstance(fignr_anytype, str):
            fignrs = [int(fignr_anytype) - 1]
        elif isinstance(fignr_anytype, list):
            for fignr in fignr_anytype:
                if fignr + 1 in self.__fignrlist:
                    if fignr not in fignrs:
                        fignrs.append(fignr)

        params = self.__create_params(fignrs)

        ps = ColumnPlotSub(params)
        ps.plot()

        return True
#  }}}

    def __set_xcoord(self, fignr):  # {{{
        if self.__xcoordnr == fignr and self.__is_xcoord_select:
            self.__is_xcoord_select = False
            self.__xcoordnr = self.__xcoordnr_ini
        else:
            self.__is_xcoord_select = True
            self.__xcoordnr = fignr
        self.replot()
# }}}

#
# prviate
# functions called from key event
#

    def __cancel_event(self, msg='Canceled', call_raise=False):  # {{{
        if msg:
            self._print(msg)
        self.__is_figselect = False
        if call_raise:
            raise 'Failure'
#  }}}

    def __select_event(self, fignr_str):  # {{{
        self.__check_fignr(fignr_str)
        self.__is_figselect = False
        self._print('Select figure ' + fignr_str)
        if self.__event_key == self.__mapmain.key_plotsub:
            if self.__merge_graphs(fignr_str):
                raise 'Success'
        elif self.__event_key == self.__mapmain.key_xcoord:
            self.__set_xcoord(int(fignr_str) - 1)
        raise 'Failure'
# }}}

    def __start_figselect(self, event_key):  # {{{
        if self.__fignrlist:
            fignrlist = self.__fignrlist
            if len(fignrlist) == 1:
                text = '(' + str(fignrlist[0]) + ')'
            else:
                hyphen = False
                prenr = fignrlist[0]
                text = '(' + str(prenr)
                for nownr in fignrlist[1:]:
                    if nownr == prenr + 1:
                        if not hyphen:
                            text += '-'
                        hyphen = True
                    else:
                        if hyphen:
                            text += str(prenr)
                        text += ',' + str(nownr)
                        hyphen = False
                    prenr = nownr
                if text[-1] == '-':
                    text += str(fignrlist[-1])
                text += ')'
            self._print('Enter figure number ' + text)

            # set to initial values for figure selection
            # and then should call __select_fignr function next
            self.__is_figselect = True
            self.__inp_fignr = ''
            self.__event_key = event_key
#  }}}

    def __select_fignr(self, key):  # {{{
        if re.match('\d', key):
            self.__inp_fignr += key
            fignr_str = self.__inp_fignr
            # suppose that the number of elements in fignrlist is less than 100
            max_fignr = self.__fignrlist[-1]
            if max_fignr < 100:
                find_unique_number = False
                if fignr_str == '0':
                    self.__cancel_event()
                elif len(fignr_str) == 1:
                    tens_place_digit = -1 if max_fignr < 10 else int(str(max_fignr)[0])
                    if int(fignr_str) > tens_place_digit:
                        find_unique_number = True
                else:
                    find_unique_number = True
                if find_unique_number:
                    self.__select_event(fignr_str)
            raise 'Success'
        elif key == 'enter':
            fignr_str = self.__inp_fignr
            if fignr_str:
                self.__select_event(fignr_str)
        self.__cancel_event()
#  }}}

#
# private
# functions called from mouse event
#

    def __clear_fignrlist(self):  # {{{
        self.__fignrlist_mosemode = list()
#  }}}

    def __get_fignr(self, event):  # {{{
        inaxes = event.inaxes
        n_col = inaxes.numCols
        rownr = inaxes.rowNum
        colnr = inaxes.colNum
        fignr = rownr * n_col + colnr
        return fignr
#  }}}

#
# override
#

    def _create_graph(self, fig):

        fig.subplots_adjust(left=0.07, bottom=0.05, right=0.97, top=0.95, wspace=0.3, hspace=0.3)

        data = self._data
        n_data = len(data)
        n_row, n_col = self.__get_plotsize(n_data)
        for i in range(n_data):
            loc = ','.join([str(n_row), str(n_col), str(i + 1)])
            f = eval('fig.add_subplot(' + str(loc) + ')')
            f.set_title(self.__get_figtitle(i))
            if data[i][0] == INVALID_DATA:
                f.set_xticks([])
                f.set_yticks([])
                f.text(-0.01, -0.01, "Invalid\ndata")
                f.plot(0)
            else:
                f.grid(self._show_grid)
                if self.__is_xcoord_select:
                    f.plot(data[self.__xcoordnr], data[i], marker=self._marker, color='r', linestyle=self._linestyle)
                else:
                    f.plot(data[i], marker=self._marker, color='r', linestyle=self._linestyle)

    def _on_key_press(self, event):

        key = event.key

        if self.__is_figselect:
            try:
                self.__select_fignr(key)
            except Exception:
                return

        if key == self.__mapmain.key_plotsub:
            self.__start_figselect(key)
        elif key == self.__mapmain.key_xcoord:
            self.__start_figselect(key)
        else:
            self._move_base_events(key, event)

    def _on_mouse_press(self, event):

        if event.button != self.__mapmain.mouse_plotsub:
            self.__clear_fignrlist()

        if event.xdata:

            if event.button == self.__mapmain.mouse_plotsub:
                fignr = self.__get_fignr(event)
                self.__fignrlist_mosemode.append(fignr)
                if event.dblclick:
                    fignrlist_mousemode = self.__fignrlist_mosemode
                    self.__clear_fignrlist()
                    if not self.__check_fignr(fignrlist_mousemode):
                        return
                    self.__merge_graphs(fignrlist_mousemode)
            elif event.button == self.__mapmain.mouse_xcoord:
                fignr = self.__get_fignr(event)
                if fignr + 1 in self.__fignrlist:
                    self.__set_xcoord(fignr)
#       elif event.button == 3:
#         if event.dblclick:
#           fignr = self.__get_fignr(event)
#           self.__merge_graphs(fignr)

    def _on_plot_begin(self):
        self._title = self.__basetitle + ' (file={}, x={})'.format(self._filename, str(self.__xcoordnr + 1))
        if self._window:
            self._window.wm_title(self._title)


if __name__ == '__main__':

    test_case = 1

    from config import create_columnplot_param
    params = create_columnplot_param()

    params['data'] = [[3, 4, 5], [INVALID_DATA], [-0, -1, -2]]
    params['figtitle'] = ['y=x', 'INVALID DATA', 'y=-x']

    if test_case == 1:
        ColumnPlotMain(params).plot()
        exit()

    elif test_case == 2:
        from generator import ColumnGenerator
        cg = ColumnGenerator('data/vge.csv', params)
        params['data'] = cg.get_data()
        params['figtitle'] = cg.get_title()
        ColumnPlotMain(params).plot()
        exit()


# vim:foldmethod=marker
