###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
# File: ps12.py
# Author: Ken Sheedlo
#
# Home Automation Laboratory 9001
#
###############################################################################

from __future__ import division

import getopt
import numpy
import plot
import rungekutta
import sys

from mechanics import twobody

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

    df = twobody(1.0, 0.5, 0.5)
    x0 = numpy.array([
                0, 0, 0,
                0, 0, 0,
                1, 0, 0,
                0, 1, 0
            ], dtype=numpy.float64)
    ts, xs = rungekutta.rk4(df, 0, x0, 0.005, 7600)
    xs = xs.transpose()

    plot.render(xs[:,0], xs[:,1], 'b', xs[:,6], xs[:,7], 'r', 
            xbound=(-10.0, 10.0),
            ybound=(0.0, 20.0),
            xlabel='x (normalized AU)',
            ylabel='y (normalized AU)',
            aspect='equal',
            title='2-body Orbital Trajectory',
            legend=('Star A', 'Star B'),
            file_prefix=file_prefix
        )

    return 0

if __name__ == "__main__":
    sys.exit(main())