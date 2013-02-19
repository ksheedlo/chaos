###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: plot.py
# Author: Ken Sheedlo
#
# High level plotting library.
#
###############################################################################

from __future__ import division

import matplotlib.pyplot
import mpl_toolkits.mplot3d

from utils import split_dict

def _render_to_output(figure, file_prefix):
    '''
    Outputs a plot to the screen or a file.

    Params:
        figure      The figure to show.
        file_prefix Either a filename prefix (the file extension is always .png)
                    or None, in which case outputs to the screen.

    Returns None, and results in a plot to the screen or a file.
    '''
    if file_prefix is None:
        figure.show()
    else:
        figure.savefig('{0}.png'.format(file_prefix), dpi=220)

def render(*args, **kwargs):
    '''
    Renders a 2D plot.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opt_actions = (
        ('title', axes.set_title),
        ('xlabel', axes.set_xlabel),
        ('ylabel', axes.set_ylabel),
        ('xticks', axes.set_xticks),
        ('yticks', axes.set_yticks),
        ('xticklabels', axes.set_xticklabels),
        ('yticklabels', axes.set_yticklabels),
        ('xbound', lambda (x1, x2): axes.set_xbound(x1, x2)),
        ('ybound', lambda (y1, y2): axes.set_ybound(y1, y2)),
        ('file_prefix', lambda _: None),
        ('ax_callback', lambda _: None),
    )
    opts, plot_args = split_dict([name for (name, _) in opt_actions], kwargs)

    if 'ax_callback' in opts:
        opts['ax_callback'](axes) 
    else:
        axes.plot(*args, **plot_args)

    # Use tuples instead of a dict because order matters. Want to set xticks
    # before xlabels, etc.
    for (name, action) in opt_actions:
        if name in opts:
            action(opts[name])

    _render_to_output(figure, opts.get('file_prefix'))

def render3d(*args, **kwargs):
    '''
    Renders a 3D plot.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.add_subplot(111, projection='3d')
    opt_actions = (
        ('title', axes.set_title),
        ('xlabel', axes.set_xlabel),
        ('ylabel', axes.set_ylabel),
        ('zlabel', axes.set_zlabel),
        ('xticks', axes.set_xticks),
        ('yticks', axes.set_yticks),
        ('zticks', axes.set_zticks),
        ('xticklabels', axes.set_xticklabels),
        ('yticklabels', axes.set_yticklabels),
        ('zticklabels', axes.set_zticklabels),
        ('xbound', lambda (x1, x2): axes.set_xbound(x1, x2)),
        ('ybound', lambda (y1, y2): axes.set_ybound(y1, y2)),
        ('zbound', lambda (z1, z2): axes.set_zbound(z1, z2)),
        ('file_prefix', lambda _: None),
        ('ax_callback', lambda _: None),
    )
    opts, plot_args = split_dict([name for (name, _) in opt_actions], kwargs)

    if 'ax_callback' in opts:
        opts['ax_callback'](axes)
    else:
        axes.plot(*args, **plot_args)

    for (name, action) in opt_actions:
        if name in opts:
            action(opts[name])

    _render_to_output(figure, opts.get('file_prefix'))
