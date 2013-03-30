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
import numpy
import utils

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
        ('aspect', axes.set_aspect),
        ('xbound', lambda (x1, x2): axes.set_xbound(x1, x2)),
        ('ybound', lambda (y1, y2): axes.set_ybound(y1, y2)),
        ('file_prefix', lambda _: None),
        ('ax_callback', lambda _: None),
    )
    opts, plot_args = utils.split_dict([name for (name, _) in opt_actions], kwargs)

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
        ('aspect', axes.set_aspect),
        ('xbound', lambda (x1, x2): axes.set_xbound(x1, x2)),
        ('ybound', lambda (y1, y2): axes.set_ybound(y1, y2)),
        ('zbound', lambda (z1, z2): axes.set_zbound(z1, z2)),
        ('file_prefix', lambda _: None),
        ('ax_callback', lambda _: None),
    )
    opts, plot_args = utils.split_dict([name for (name, _) in opt_actions], kwargs)

    if 'ax_callback' in opts:
        opts['ax_callback'](axes)
    else:
        axes.plot(*args, **plot_args)

    for (name, action) in opt_actions:
        if name in opts:
            action(opts[name])

    _render_to_output(figure, opts.get('file_prefix'))

def mod2pi(*args, **kwargs):
    '''
    Renders a 2D plot modulo 2*pi.

    '''
    plot_args = dict(kwargs)
    plot_args.update({
            'xbound': (0, 2*numpy.pi),
            'xticks': (
                    0,
                    numpy.pi/2,
                    numpy.pi,
                    3*numpy.pi/2,
                    2*numpy.pi
                ),
            'xticklabels': (
                    '0',
                    r'$\frac{\pi}{2}$',
                    r'$\pi$',
                    r'$\frac{3\pi}{2}$',
                    r'$2\pi$'
                )
        })
    render(*args, **plot_args)

def embedded(vs, xdim, ydim, *args, **kwargs):
    '''
    Renders a delay coordinate embedded data set.

    '''
    xs = numpy.array([
                utils.mod2pi(v) for v in vs[:,xdim]
            ], dtype=numpy.float64)
    ys = numpy.array([
                utils.mod2pi(v) for v in vs[:,ydim]
            ], dtype=numpy.float64)
    rfunc = render if 'xbound' in kwargs else mod2pi
    plot_args = (xs, ys) + tuple(args)
    rfunc(*plot_args, **kwargs)

def loglog(*args, **kwargs):
    '''
    Renders a 2D log-log plot.

    All the same options and kwargs as plot.render are supported.
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
        ('aspect', axes.set_aspect),
        ('xbound', lambda (x1, x2): axes.set_xbound(x1, x2)),
        ('ybound', lambda (y1, y2): axes.set_ybound(y1, y2)),
        ('file_prefix', lambda _: None),
        ('ax_callback', lambda _: None),
    )
    opts, plot_args = utils.split_dict([name for (name, _) in opt_actions], kwargs)

    if 'ax_callback' in opts:
        opts['ax_callback'](axes) 
    else:
        axes.loglog(*args, **plot_args)

    # Use tuples instead of a dict because order matters. Want to set xticks
    # before xlabels, etc.
    for (name, action) in opt_actions:
        if name in opts:
            action(opts[name])

    _render_to_output(figure, opts.get('file_prefix'))
