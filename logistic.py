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

import getopt
import matplotlib.pyplot
import numpy
import sys

from utils import split_dict

'''
Logistic function implementation and plotting.

All function parameters are real numbers (numpy.float64) unless otherwise 
specified. If a parameter is specified as an integer, it should be numpy.int32
unless otherwise stated.
'''

def lmap(start, ratio, steps, cutoff=0):
    '''
    Iterates the Logistic map and produces a vector of results.

    Parameters:
        start   The starting value x_0 for the mapping.
        ratio   The scaling parameter R.
        steps   The number of steps to run the mapping, as an integer.
        cutoff  The number of initial steps to throw away, as an integer.

    Returns: a vector of real-valued results.
    '''
    result = numpy.empty(steps+1, dtype=numpy.float64)
    result[0] = start
    for i in xrange(steps):
        x_i = result[i]
        result[i+1] = ratio * x_i * (1-x_i)
    return result[cutoff:]

def plot_time(ts, xs, **kwargs):
    '''
    Plots the specified vector in the time domain.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(['title', 'filename'], kwargs)
    axes.plot(ts, xs, '.', **plot_args)
    axes.set_ylim((0.0, 1.0))
    axes.set_aspect(ts[-1] - ts[0])
    axes.set_xlabel('n')
    axes.set_ylabel(r'$x_n$')
    axes.set_title(opts.get('title', r'$x_n$'))
    if opts.get('filename') is not None:
        figure.savefig(kwargs['filename'], dpi=220)
    else:
        figure.show()

def plot_time2(ts, xs1, xs2, **kwargs):
    '''
    Plots 2 vectors in the time domain.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(['title', 'filename'], kwargs)
    axes.plot(ts, xs1, 'b-o', **plot_args)
    axes.plot(ts, xs2, 'r-o', **plot_args)
    axes.set_ylim((0.0, 1.0))
    axes.set_xlabel('n')
    axes.set_ylabel(r'$x_n$')
    axes.legend(('$x_0 = {0}$'.format(xs1[0]), '$x_0 = {0}$'.format(xs2[0])))
    axes.set_title(opts.get('title', r'$x_n$'))
    if opts.get('filename') is not None:
        figure.savefig(kwargs['filename'], dpi=220)
    else:
        figure.show()


def plot_ret1(xs, **kwargs):
    '''
    Plots the specified vector in the first return map space.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(['title', 'filename'], kwargs)
    axes.plot(xs[:-1], xs[1:], '.', **plot_args)
    axes.set_ylim((0.0, 1.0))
    axes.set_xlim((0.0, 1.0))
    axes.set_aspect(1.0)
    axes.set_xlabel(r'$x_n$')
    axes.set_ylabel(r'$x_{n+1}$')
    axes.set_title(opts.get('title', 'First Return Map Space'))
    if opts.get('filename') is not None:
        figure.savefig(kwargs['filename'], dpi=220)
    else:
        figure.show()

def plot_ret2(xs, **kwargs):
    '''
    Plots the specified vector in the second return map space.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(['title', 'filename'], kwargs)
    axes.plot(xs[:-2], xs[2:], '.', **plot_args)
    axes.set_ylim((0.0, 1.0))
    axes.set_xlim((0.0, 1.0))
    axes.set_aspect(1.0)
    axes.set_xlabel(r'$x_n$')
    axes.set_ylabel(r'$x_{n+2}$')
    axes.set_title(opts.get('title', 'Second Return Map Space'))
    if opts.get('filename') is not None:
        figure.savefig(kwargs['filename'], dpi=220)
    else:
        figure.show()

def main(argv=None):
    '''
    Main program function.

    '''
    if argv is None:
        argv = sys.argv

    start_x = 0.2
    ratio = 3.0
    steps = 100
    cutoff = 0
    delta = 0.0001
    file_prefix = None
    try:
        options, args = getopt.getopt(argv[1:], 'x:R:m:k:f:d:')
        for opt, arg in options:
            if opt == '-x':
                start_x = numpy.float64(arg)
            elif opt == '-R':
                ratio = numpy.float64(arg)
            elif opt == '-m':
                steps = numpy.int32(arg)
            elif opt == '-k':
                cutoff = numpy.int32(arg)
            elif opt == '-f':
                file_prefix = arg
            elif opt == '-d':
                delta = numpy.float64(arg)
    except getopt.GetoptError as err:
        print str(err)
        return 2

    result = lmap(start_x, ratio, steps, cutoff=cutoff)
    res2 = lmap(start_x + delta, ratio, steps, cutoff=cutoff)
    ts = numpy.array(range(cutoff, steps+1), dtype=numpy.int32)

    if file_prefix is not None:
        plot_time(ts, result, filename=('{0}_time.png'.format(file_prefix)),
                        title='$x_n$ (r={0}, $x_0$={1})'.format(ratio, start_x))
        plot_time2(ts, result, res2, filename=('{0}_offset.png'.format(file_prefix)),
                        title='Chaotic Divergence (r={0})'.format(ratio))
        plot_ret1(result, filename=('{0}_ret1.png'.format(file_prefix)),
                        title='First Return Map (r={0}, $x_0$={1})'.format(ratio, start_x))
        plot_ret2(result, filename=('{0}_ret2.png'.format(file_prefix)),
                        title='Second Return Map (r={0}, $x_0$={1})'.format(ratio, start_x))
    else:
        plot_time(ts, result,
                    title='$x_n$ (r={0}, $x_0$={1})'.format(ratio, start_x)
                    )
        plot_time2(ts, result, res2, title='Chaotic Divergence (r={0})'.format(ratio))
        plot_ret1(result,
                    title='First Return Map (r={0}, $x_0$={1})'.format(ratio, start_x)
                    )
        plot_ret2(result,
                    title='Second Return Map (r={0}, $x_0$={1})'.format(ratio, start_x)
                    )

    return 0

if __name__ == "__main__":
    sys.exit(main())