###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: bifurcation.py
# Author: Ken Sheedlo
#
# Bifurcation diagram plotting and analysis.
#
###############################################################################

from __future__ import division

import getopt
import logistic
import matplotlib.pyplot
import numpy
import sys

from utils import split_dict, fp_equal

def bifurcate(r_start, r_end, r_delta, steps, cutoff):
    '''
    Generates R vs. X data for plotting bifuration diagrams.

    '''
    rs = numpy.arange(r_start, r_end, r_delta, dtype=numpy.float64)
    xs = numpy.array([
                    logistic.lmap(0.5, r, steps, cutoff=cutoff) for r in rs
                ], dtype=numpy.float64)
    return rs, xs

def plot_bifdiag(rs, xs, **kwargs):
    '''
    Plots a bifurcation diagram given a data set of rs, xs.

    '''
    figure = matplotlib.pyplot.figure()
    axes = figure.gca()
    opts, plot_args = split_dict(('title', 'filename'), kwargs)
    plot_args.update(markersize=0.2)
    axes.plot(rs, xs, 'k.', **plot_args)
    axes.set_xlabel('R')
    axes.set_ylabel('$x_n$')
    axes.set_title(opts.get('title', 'Bifurcation Diagram for the Logistic Map'))

    # Check opts.get('filename') is not None instead of 'filename' in opts.
    # Expect callers to pass filename=None and show the plot to the screen.
    if opts.get('filename') is not None:
        figure.savefig(kwargs['filename'], dpi=220)
    else:
        figure.show()

def _get_period(xs):
    for p_test in xrange(1, 33):
        for p_i in xrange(1, p_test+1):
            x_slice = xs[-p_i:-p_i-(p_test+1):-p_test]
            if not fp_equal(x_slice[0], x_slice[1]):
                break
        else:
            return p_test
    return None

def find_period_doubling(rs, xs):
    '''
    Detects period doubling behavior.

    '''
    results = ()
    for (i, r) in enumerate(rs[:-1]):
        p1 = _get_period(xs[i,:])
        p2 = _get_period(xs[i+1,:])
        if p1 is None and p2 is not None:
            results = results + (r,)
        if p1 is not None and p2 is not None and p2 == (2*p1):
            results = results + (r,)
    return results

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

    rs, xs = bifurcate(2.8, 4.0, 0.001, 1200, 800)

    if file_prefix is not None:
        plot_bifdiag(rs, xs, filename='{0}.png'.format(file_prefix))
    else:
        plot_bifdiag(rs, xs)

#    rs, xs = bifurcate(2.8, 4.0, 0.001, 3000, 2600)
#    print find_period_doubling(rs, xs)
#
    return 0

if __name__ == "__main__":
    sys.exit(main())


