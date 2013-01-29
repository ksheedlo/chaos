###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: logistic.py
# Author: Ken Sheedlo
#
# Provides library functions and a main program for plotting the logistic map.
#
###############################################################################

from __future__ import division

import getopt
import matplotlib.pyplot
import numpy
import sys

from mpl_toolkits.mplot3d import Axes3D
from utils import split_dict

def hmap(x_start, y_start, a_ratio, b_ratio, steps, cutoff=0):
    '''
    Generates points along the Henon map.

    Parameters:
        x_start     A starting value for x0 in the map.
        y_start     A starting value for y0 in the map.
        a_ratio     The ratio to use for a.
        b_ratio     The ratio to use for b.
        steps       The number of steps to iterate, as an integer.
        cutoff      The number of initial steps to throw away, as an integer.

    Returns a vector of real-valued results.
    '''
    result = numpy.empty((steps+1, 2), dtype=numpy.float64)
    result[0,:] = x_start, y_start
    for i in xrange(steps):
        x_i, y_i = result[i,:]
        result[i+1,:] = (y_i + 1 - a_ratio*(x_i ** 2)), (b_ratio*x_i)
    return result[cutoff:,:]

def bifurcate(a_start, a_end, a_delta, steps, cutoff):
    '''
    Generates a vs. X data for bifurcation plotting and analysis.

    '''
    ass = numpy.arange(a_start, a_end, a_delta, dtype=numpy.float64)
    xs = numpy.array([
                    hmap(0.1, 0.1, a, 0.3, steps, cutoff=cutoff)[:,0] for a in ass
                ], dtype=numpy.float64)
    return ass, xs

def plot_bifdiag(ass, xs, **kwargs):
    '''
    Plots a bifurcation diagram of the Henon map.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(('title', 'filename'), kwargs)
    plot_args.update(markersize=0.2)
    axes.plot(ass, xs, 'k.', **plot_args)
    axes.set_xlabel('a')
    axes.set_ylabel('$x_n$')
    axes.set_title(opts.get('title', 'Bifurcation Diagram for the Henon Map'))

    if opts.get('filename') is not None:
        figure.savefig(kwargs['filename'], dpi=220)
    else:
        figure.show()

def plot_time(ts, xs, **kwargs):
    '''
    Generates a 3D plot of the Henon map over time.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.add_subplot(111, projection='3d')
    opts, plot_args = split_dict(('title', 'filename'), kwargs)
    axes.plot(ts, xs[:,0], xs[:,1], '-', **plot_args)
    figure.show()

def plot_ret1(xs, **kwargs):
    '''
    Plots the Henon map in the first return map space.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(('title', 'filename'), kwargs)
    plot_args.update(markersize=0.2)

    axes.plot(xs[:,0], xs[:,1], '.', **plot_args)
    axes.set_xlabel('$x_n$')
    axes.set_ylabel('$y_n$')
    axes.set_title(opts.get('title', 'Henon Map'))

    if opts.get('filename') is not None:
        figure.savefig(kwargs['filename'], dpi=220)
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

    ass, xs = bifurcate(0.0, 1.4, 0.001, 2000, 500)
    zs = hmap(0.0, 0.0, 1.4, 0.3, 10000)

    if file_prefix is not None:
 #       import pdb; pdb.set_trace()
        plot_bifdiag(ass, xs, filename='{0}_bifurc.png'.format(file_prefix))
        plot_ret1(
                zs, 
                filename='{0}_ret1.png'.format(file_prefix),
                title='Henon Map, $a=1.4$'
            )
    else:
        plot_bifdiag(ass, xs)
        plot_ret1(xs, title='Henon Map, $a=1.4$')

    return 0

if __name__ == "__main__":
    sys.exit(main())