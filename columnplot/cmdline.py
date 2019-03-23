#!/usr/bin/env python3

import argparse
import os


def parser():

    parser = argparse.ArgumentParser(description='columnplot (version 1.0.0)')

    parser.add_argument('filepath', metavar='filepath', nargs=1, help='Input data file')
#     parser.add_argument('filepath', metavar='filepath', nargs='?', default='../data/test.csv', help='input data flie')
#     parser.add_argument('filepath', metavar='filepath', nargs='?', default='../data/graph.dat', help='input data flie')
#     parser.add_argument('filepath', metavar='filepath', nargs='?', default='../data/graph_notmatchx.dat', help='input data flie')
#     parser.add_argument('filepath', metavar='filepath', nargs='?', default='../data/column_missing.csv', help='input data flie')
#     parser.add_argument('filepath', metavar='filepath', nargs='?', default='../data/noalign.csv', help='input data flie')
#     parser.add_argument('filepath', metavar='filepath', nargs='?', default='../data/vge.csv', help='input data flie')

    parser.add_argument('-d', '--delimiter', action='store', nargs=1, type=str, metavar='DELIM', help='Specify a delimiter to separate columns in a data file')
    parser.add_argument('-D', '--datetime', action='store', nargs='+', type=str, metavar='TIMEFMT', help='Specify datetime format such as "%%Y-%%m-%%d %%H:%%M:%%S.%%f"')
    parser.add_argument('-i', '--ignore', action='store', nargs='+', type=int, metavar='COLUMNNR', help='Specify column numbers that should be ignored')
    parser.add_argument('-l', '--limit', action='store', nargs='+', type=int, metavar='COLUMNNR', help='Specify column numbers to draw')
    parser.add_argument('-p', '--print', action='store_true', help='Print configuration information')
    parser.add_argument('-t', '--titleline', action='store_true', help='Use the first data line as a graph title')
    parser.add_argument('-v', '--version', action='version', version='ColumnPlot (version 1.0.0)')

    t_clargs = parser.parse_args()
    args = t_clargs.__dict__

    name = 'print'
    print_params = args[name]

    cl_args = dict()

    name = 'delimiter'
    rename = name
    cl_args[rename] = args[name][0] if args[name] else ''

    name = 'filepath'
    rename = 'filename'
    filepath = args[name]
    if isinstance(filepath, list):
        filepath = filepath[0]
    if not filepath or not os.path.exists(filepath):
        print("Error: input file does not exist")
        exit(1)
    cl_args[rename] = os.path.basename(filepath)

    name = 'ignore'
    rename = 'ignore_colnrs'
    save_rename = rename
    cl_args[rename] = list()
    if args[name] is not None:
        s = set()
        for i in args[name]:
            if i > 0:
                s.add(i)
        cl_args[rename] = sorted(list(s))

    name = 'limit'
    rename = 'limit_colnrs'
    if args[name] is not None:
        cl_args[save_rename] = [i for i in range(1, 100) if i not in args[name]]
        if print_params:
            cl_args[rename] = sorted(args[name])

    name = 'datetime'
    rename = 'timefmt'
    if args[name] is not None:
        cl_args[rename] = args[name]

    name = 'titleline'
    rename = 'force_graphtitle'
    cl_args[rename] = args[name]

    return cl_args, filepath, print_params


if __name__ == '__main__':

    cl_args, filepath, print_params = parser()

    print('filepath : ' + filepath)
    print('print_params  : ' + str(print_params))
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(cl_args)
