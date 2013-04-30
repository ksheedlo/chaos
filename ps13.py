###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
# File: ps13.py
# Author: Ken Sheedlo
#
# I Went to Space and the Law Won
#
###############################################################################

from __future__ import division

import getopt
import multiprocessing
import numpy
import plot
import rungekutta
import sys

from mechanics import threebody
from utils import suffixed

def pr1(file_prefix):
    df = threebody(1.0, 0.5, 0.5, 0.5)
    x0 = numpy.array([
                0, 0, 0,
                0, 0, 0,
                1, 0, 0,
                0, 1, 0,
                0, 3000, 0,
                0, 0, 0
            ], dtype=numpy.float64)
    ts, xs = rungekutta.rk4(df, 0, x0, 0.005, 7600)
    xs = xs.transpose()
    plot.render(xs[:,0], xs[:,1], 'b', xs[:,6], xs[:,7], 'r', xs[:,12], xs[:,13], 'g',
            xlabel='x (normalized AU)',
            ylabel='y (normalized AU)',
            xbound=(-10.0, 10.0),
            ybound=(0.0, 20.0),
            aspect='equal',
            title='3-body Orbital Trajectory',
            legend=('Star A', 'Star B'),
            file_prefix=suffixed(file_prefix, '_1a')
        )
    plot.render(xs[:,6] - xs[:,0], xs[:,7] - xs[:,1], 'r',
            xlabel='x (normalized AU)',
            ylabel='y (normalized AU)',
            aspect='equal',
            title='3-body Trajectory, Star A at origin',
            legend=('Star B',),
            file_prefix=suffixed(file_prefix, '_1b')
        )

def pr2(file_prefix):
    df = threebody(1.0, 0.5, 0.5, 0.5)
    x0 = numpy.array([
                0, 0, 0,
                0, 0, 0,
                1, 0, 0,
                0, 1, 0,
                0, 20, 0,
                0, -0.15, 0
            ], dtype=numpy.float64)
    ts, xs = rungekutta.rk4(df, 0, x0, 0.005, 50000)
    xs = xs.transpose()
    plot.render(xs[:5500,0], xs[:5500,1], 'b', xs[:5500,6], xs[:5500,7], 'r', xs[:5500,12], xs[:5500,13], 'g',
            xlabel='x (normalized AU)',
            ylabel='y (normalized AU)',
            title='3-body Orbital Interaction',
            legend=('Star A', 'Star B', 'Star C'),
            file_prefix=suffixed(file_prefix, '_2a')
        )
    plot.render(xs[:,0], xs[:,1], 'b', xs[:,12], xs[:,13], 'g',
            xlabel='x (normalized AU)',
            ylabel='y (normalized AU)',
            title='3-body Orbital Interaction',
            legend=('Star A', 'Star C'),
            file_prefix=suffixed(file_prefix, '_2b')
        )

def pr3(file_prefix):
    ic = lambda y: numpy.array([
                        0, 0, 0,
                        0, 0, 0,
                        1, 0, 0,
                        0, 1, 0,
                        0, y, 0,
                        0, -0.15, 0
                    ], dtype=numpy.float64)
    df = threebody(1.0, 0.5, 0.5, 0.5)
    for i in xrange(8):
        ts, xs = rungekutta.rk4(df, 0, ic(0.3*i + 20.0), 0.005, 8000)
        xs = xs.transpose()
        plot.render(xs[:,0], xs[:,1], 'b', xs[:,6], xs[:,7], 'r', xs[:,12], xs[:,13], 'g',
                xlabel='x (normalized AU)',
                ylabel='y (normalized AU)',
                title=r'3-body Orbital Interaction ($x_{14}=%.1f$)' % (0.3*i+20.0),
                legend=('Star A', 'Star B', 'Star C'),
                file_prefix=suffixed(file_prefix, '_3{0}'.format(chr(97+i)))
            )

def pr4(file_prefix):
    """This is not the problem you are looking for."""
    x0 = numpy.array([
                    0, 0, 0,
                    0, 0, 0,
                    1, 0, 0,
                    0, 1, 0,
                    0, 21.5, 0,
                    0, -0.15, 0
            ], dtype=numpy.float64)
    ts, xs = rungekutta.rk4(df, 0, x0, 0.005, 8000)
    xs = xs.transpose()
    plot.render(xs[:,0], xs[:,1], 'b', xs[:,6], xs[:,7], 'r', xs[:,12], xs[:,13], 'g',
            xlabel='x (normalized AU)',
            ylabel='y (normalized AU)',
            title=r'3-body Orbital Interaction ($x_{14}=21.5$)',
            legend=('Star A', 'Star B', 'Star C'),
            file_prefix=suffixed(file_prefix, '_4')
        )

def main(argv=None):
    argv = argv or sys.argv
    file_prefix = None

    try:
        options, args = getopt.getopt(argv[1:], 'f:')
        for opt, arg in options:
            if opt == '-f':
                file_prefix = arg 
    except getopt.GetoptError as err:
        print str(err)
        return 2

    pr1(file_prefix)
    pr2(file_prefix)
    pr3(file_prefix)

    return 0

if __name__ == "__main__":
    sys.exit(main())