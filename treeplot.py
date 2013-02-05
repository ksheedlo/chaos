###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: treeplot.py
# Author: Ken Sheedlo
#
# Fractal tree plotting thinglet.
#
###############################################################################

from __future__ import division

import getopt
import matplotlib.pyplot
import numpy
import sys

from utils import split_dict
from matplotlib.lines import Line2D

def rotate(vec, theta):
    '''
    Rotates a 2D vector theta degrees.

    '''
    cos_theta = numpy.cos(theta)
    sin_theta = numpy.sin(theta)
    translation = numpy.array([
                                [cos_theta, -sin_theta],
                                [sin_theta, cos_theta]
                            ], numpy.float64)
    return numpy.dot(vec, translation)

def render(x_start=1.0, y_start=0.5, size=1.0, iterations=13, **kwargs):
    '''
    Draws a neat fractal tree. 

    '''
    opts, plot_args = split_dict(('title', 'filename', 'ratio'), kwargs)
    render_color = opts.get('color', 'k')
    ratio = opts.get('ratio', 0.6)
    figure = matplotlib.pyplot.figure()

    def _iterate(axes, x_center, y_center, horizontal, size, iterations):
        '''
        Iterates the fractal tree over the axes.

        '''
        if iterations == 0:
            return

        halfsize = size / 2
        if horizontal:
            (x1, x2) = (x_center - halfsize, x_center + halfsize)
            (y1, y2) = (y_center, y_center)
        else:
            # Vertical
            (x1, x2) = (x_center, x_center)
            (y1, y2) = (y_center - halfsize, y_center + halfsize)

        axes.plot((x1,x2), (y1,y2), color=render_color, **plot_args)
        _iterate(axes, x1, y1, not horizontal, ratio*size, iterations-1)
        _iterate(axes, x2, y2, not horizontal, ratio*size, iterations-1)

    axes = figure.gca()
    axes.plot(
            (x_start, x_start), 
            (y_start - (size/2), y_start + (size/2)), 
            color=render_color, 
            **plot_args
        )
    _iterate(axes, x_start, y_start + (size/2), True, 0.6*size, iterations)
    axes.set_xbound((0.4, 1.6))
    axes.set_ybound((0.0, 1.4))
    axes.set_title(opts.get('title', 'Self-similar Fractal Tree'))

    if opts.get('filename') is not None:
        figure.savefig(opts['filename'], dpi=220)
    else:
        figure.show()

def skewed(x_start=1.0, y_start=0.5, size=1.0, iterations=13, **kwargs):
    '''
    Draws a fractal tree with tuneable parameters.

    '''
    opts, plot_args = split_dict((
                                'title', 
                                'filename', 
                                'llength', 
                                'rlength', 
                                'ltheta', 
                                'rtheta'
                            ), kwargs)
    llength = opts.get('llength', 0.6)
    rlength = opts.get('rlength', 0.6)
    render_color = opts.get('color', 'k')
    ltheta = -numpy.deg2rad(opts.get('ltheta', 90.0))
    rtheta = numpy.deg2rad(opts.get('rtheta', 90.0))

    def _iterate(axes, p0, p1, iterations):
        '''
        Iterates a fancy fractal tree over the axes.

        '''
        if iterations == 0:
            return

        x0, y0 = p0
        x1, y1 = p1
        dv = numpy.array([x1 - x0, y1 - y0], numpy.float64)

        lvec = llength * rotate(dv, ltheta)
        rvec = rlength * rotate(dv, rtheta)

        axes.plot((x1, x1+lvec[0]), (y1, y1+lvec[1]), color=render_color, 
                    **plot_args)
        _iterate(axes, p1, (x1+lvec[0], y1+lvec[1]), iterations-1)
        axes.plot((x1, x1+rvec[0]), (y1, y1+rvec[1]), color=render_color, 
                    **plot_args)
        _iterate(axes, p1, (x1+rvec[0], y1+rvec[1]), iterations-1)

    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    axes.plot(
            (x_start, x_start), 
            (y_start - (size/2), y_start + (size/2)), 
            color=render_color, 
            **plot_args
        )
    _iterate(axes, (x_start, y_start-(size/2)), (x_start, y_start+(size/2)), 
                iterations)

    axes.set_title(opts.get('title', 'Rotated Fractal Tree'))
    if opts.get('filename') is not None:
        figure.savefig(opts['filename'], dpi=220)
    else:
        figure.show()

def main(argv=None):
    if argv is None:
        argv = sys.argv

    file_prefix = None

    try:
        options, args = getopt.getopt(argv[1:], 'f:')
        for opt, arg in options:
            if opt == '-f':
                file_prefix = arg
    except getopt.GetoptError as err:
        print str(err)
        return 2

    if file_prefix is not None:
        render(filename='{0}.png'.format(file_prefix))
    else:
        render()

    return 0

if __name__ == "__main__":
    sys.exit(main())