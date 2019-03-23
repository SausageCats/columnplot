#!/usr/bin/env python3

import os
import re
import configparser


def create_columnplot_param(cl_args=None, print_params=False):

    params = dict()

    # use in ColumnGenerator class
    params['enable_graphtitle'] = True
    params['force_graphtitle'] = False
    params['ignore_colnrs'] = list()
    params['max_strelms'] = 15
    params['timefmt'] = list()

    # use in ColumnPlotMain/ColumnPlotSub class
    params['geometry_plotmain'] = '1600x1200+40+50'
    params['geometry_plotsub'] = '1000x750+40+50'
    params['filename'] = ''
    params['linestyle'] = '-'
    params['marker'] = ''
    params['marker1'] = 'o'
    params['marker2'] = '.'
    params['show_grid'] = False
    params['show_marker'] = False
    params['show_msgs'] = False
    params['show_toolbar'] = False

    # key bindings
    params['key_marker1'] = 'm'
    params['key_marker2'] = 'M'
    params['key_grid'] = 'G'
    params['key_linestyle'] = 'l'
    params['key_quit'] = 'q'
    params['key_quitall'] = 'Q'
    params['key_plotsub'] = 's'
    params['key_xcoord'] = 'x'
    params['key_toolbar'] = 'T'

    # mouse bindings
    params['mouse_plotsub'] = 1
    params['mouse_xcoord'] = 2

    update_params_from_cpcfg(params)
    update_params_from_cl(cl_args, params)

    if params['show_marker']:
        params['marker'] = params['marker1']

    if print_params:
        display_parameters(params)

    return params


def update_params_from_cpcfg(params):

    cfgpath = ''
    env_key = 'COLUMNPLOTCFG'
    if env_key in os.environ:
        cfgpath_env = os.path.abspath(os.environ[env_key])
        if os.path.exists(cfgpath_env):
            cfgpath = cfgpath_env
    if not cfgpath:
        cfgpath_default = os.path.expanduser('~/.config/columnplot/columnplot.cfg')
        if os.path.exists(cfgpath_default):
            cfgpath = cfgpath_default

    if cfgpath:
        config = configparser.ConfigParser()
        with open(cfgpath, 'r') as fp:
            section = 'columnplot'
            config.read_file(read_columnplotcfg(fp, section))
            for key, value in config.items(section):
                if key in params:
                    param_val = params[key]
                    if isinstance(param_val, bool):
                        params[key] = config.getboolean(section, key)
                    elif isinstance(param_val, int):
                        params[key] = config.getint(section, key)
                    elif isinstance(param_val, list):
                        if value:
                            try:
                                v = eval(value)
                                if not isinstance(v, list):
                                    raise
                            except Exception:
                                print('"%s" should be set to list... Check config file.' % key)
                                exit(1)
                            if len(v) >= 1:
                                params[key] = v
#                 for string in v:
#                   if string == '':
#                     continue
#                   break
#                 else:
#                   params[key] = list()
                    else:
                        params[key] = str(value)


def read_columnplotcfg(fp, section):
    yield '[' + section + ']\n'
    line = fp.readline()
    while line:
        line = re.sub('%', '%%', line)
        yield line
        line = fp.readline()


def update_params_from_cl(cl_args, params):
    if cl_args:
        for key, value in cl_args.items():
            params[key] = value


def display_parameters(params):
    max_length = max([len(key) for key in params.keys()])
    for key, value in params.items():
        length = len(key)
        string = '  ' + key + ' ' * (max_length - length) + '  |  ' + str(value)
        print(string)


if __name__ == '__main__':
    params = create_columnplot_param()
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(params)
