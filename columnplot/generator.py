#!/usr/bin/env python3


import re
from columnplot.utility import file_exists
from columnplot.variables import INVALID_DATA
import dateutil.parser
from datetime import datetime


class ColumnGenerator(object):

    def __init__(self, datapath, params):

        file_exists(datapath)

        self.__enable_titleline = params['enable_graphtitle']
        self.__force_titleline = params['force_graphtitle']
        self.__max_strelms = params['max_strelms']
        self.__timefmt = params['timefmt']

        self.__ignore_colnrs = params['ignore_colnrs']
        delimiter = params['delimiter']

        self.__datapath = datapath
        self.__comment = self.__get_comment()
        self.__delimiter = self.__get_delimiter(datapath, delimiter)
        self.__data = self.__get_data(datapath, self.__comment, self.__delimiter, self.__timefmt)
        self.__title = self.__get_title(datapath, self.__comment, self.__delimiter)

#
# private
#

    def __check_datatype(self, c_datatype, p_datatype, i, data_type, linenr, data_str):
        if p_datatype == 'ini':
            data_type[i] = c_datatype
            return
        else:
            print('[Error] Detect different type at line {} in column {} : {}'.format(str(linenr), str(i + 1), data_str))
            exit(1)

    def __get_iscsv(self, datapath):
        return True if re.match('.*\.csv$', datapath) else False

    def __get_comment(self):
        return '^\s*#'

    def __get_delimiter(self, datapath, delimiter):
        if delimiter:
            return delimiter
        is_csv = self.__get_iscsv(datapath)
        return ',' if is_csv else '\s+'

    def __get_data(self, datapath, comment, delimiter, timefmt):

        data = list()
        data_str = list()
        data_type = list()
        label_count = list()
        is_invalid_data = list()

        ignore_firstnr = self.__ignore_colnrs[0] if self.__ignore_colnrs else 0
        ignore_lastnr = self.__ignore_colnrs[-1] if self.__ignore_colnrs else 0

        is_comment = re.compile(comment)
        pat_number = re.compile('\d')

        linenr = 0
        load_first_data = False

        with open(datapath, 'r') as f:

            if self.__force_titleline:
                linenr = 1
                f.readline()

            for line in f:

                linenr += 1

                if is_comment.match(line):
                    continue

                idx_invalid_nr = 0
                invalid_nr = ignore_firstnr
                ignore_data = False
                splitdata = list()
                for i, sd in enumerate(re.split(delimiter, line.strip('\n')), start=1):
                    if i == invalid_nr:
                        if i < ignore_lastnr:
                            idx_invalid_nr += 1
                            invalid_nr = self.__ignore_colnrs[idx_invalid_nr]
                        continue
                    sd = sd.strip()
                    if sd == '':
                        ignore_data = True
                        break
                    splitdata.append(sd)
                if ignore_data or not splitdata:
                    continue

                if not load_first_data:
                    for _ in splitdata:
                        data.append(list())
                        data_type.append('ini')  # the value is 'ini', 'num', 'date', or 'str'
                        data_str.append(list())
                        label_count.append(0)
                        is_invalid_data.append(False)
                    load_first_data = True

                for i, d in enumerate(splitdata):
                    if is_invalid_data[i]:
                        continue

                    try:
                        # save numerical value
                        data[i].append(float(d))
                        if data_type[i] != 'num':
                            self.__check_datatype('num', data_type[i], i, data_type, linenr, d)
                        continue
                    except Exception:
                        pass

                    if timefmt != ['']:
                        try:
                            if timefmt:
                                for fmt in timefmt:
                                    try:
                                        dt = datetime.strptime(d, fmt)
                                        break
                                    except Exception:
                                        pass
                                else:
                                    raise
                            else:
                                if not re.search(pat_number, d):
                                    raise
                                # takes a long time
                                dt = dateutil.parser.parse(d)
                            # save datetime
                            data[i].append(dt)
                            if data_type[i] != 'date':
                                self.__check_datatype('date', data_type[i], i, data_type, linenr, d)
                            continue
                        except Exception:
                            pass

                    if d not in data_str[i]:
                        label_count[i] += 1
                        data_str[i].append(d)
                    if label_count[i] > self.__max_strelms:
                        # invalidate column i
                        data[i].insert(0, INVALID_DATA)
                        is_invalid_data[i] = True
                    else:
                        # save string
                        data[i].append(d)
                        if data_type[i] != 'str':
                            self.__check_datatype('str', data_type[i], i, data_type, linenr, d)

        return data

    def __get_title(self, datapath, comment, delimiter):

        title = list()
        is_comment = re.compile(comment)

        with open(datapath, 'r') as f:
            for line in f:

                if self.__force_titleline or (self.__enable_titleline and is_comment.match(line)):
                    line = re.sub(comment, '', line.strip('\n'))
                    splittitle = re.split(delimiter, line)
                    for i, t in enumerate(splittitle, start=1):
                        if i in self.__ignore_colnrs:
                            continue
                        title.append(t.strip())

                else:
                    splitnr = len(re.split(delimiter, line))
                    for i in range(1, splitnr + 1):
                        if i in self.__ignore_colnrs:
                            continue
                        title.append(i)

                break

        return title


#
# public
#

    def get_data(self):
        return self.__data

    def get_title(self):
        return self.__title


if __name__ == '__main__':
    # test1
    from config import create_columnplot_param
    params = create_columnplot_param()

    ColumnGenerator('data/test.csv', params)
    exit()

    print(ColumnGenerator('data/simple.csv', params).get_data())
    print(ColumnGenerator('data/graph.dat', params).get_data())
    print(ColumnGenerator('data/graph_notmatchx.dat', params).get_title())

    # test2
    import time
    params_datefmt = params.copy()
    params_datefmt['timefmt'] = ['%Y-%m-%d %H:%M:%S.%f']
    t1 = time.time()
    ColumnGenerator('data/test.csv', params_datefmt)
    t2 = time.time()
    ColumnGenerator('data/test.csv', params)
    t3 = time.time()
    print("with    fmt : %f[s]" % (t2 - t1))
    print("without fmt : %f[s]" % (t3 - t2))
