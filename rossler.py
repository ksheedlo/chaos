###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: rossler.py
# Author: Ken Sheedlo
#
# Rossler system parameterizers/PS5 stuff.
#
###############################################################################

from __future__ import division

import getopt
import numpy
import plot
import rungekutta
import sys

def rossler(a, b, c):
    '''
    Parameterizes a Rossler system.

    Params: a, b, c for the new Rossler system.

    Returns: a callable F(t, x) where 
        t   is not used in the Rossler system, but included for compatibility 
            with ODE integrators.
        x   the current state vector of the system.
    '''
    return lambda _, x: numpy.array([
                                    -(x[1]+x[2]),
                                    x[0] + a*x[1],
                                    b + x[2]*(x[0]-c)
                                ], dtype=numpy.float64)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    file_prefix = None
    x = 0.0001
    y = 0.0001
    z = 0.0001

    a = 0.398
    b = 2.0
    c = 4.0

    try:
        options, args = getopt.getopt(argv[1:], 'f:x:y:z:a:b:c:')
        for opt, arg in options:
            if opt == '-f':
                file_prefix = arg
            elif opt == '-x':
                x = float(arg)
            elif opt == '-y':
                y = float(arg)
            elif opt == '-z':
                z = float(arg)
            elif opt == '-a':
                a = float(arg)
            elif opt == '-b':
                b = float(arg)
            elif opt == '-c':
                c = float(arg)
    except getopt.GetoptError as err:
        print str(err)
        return 2

    rfunc = rossler(a, b, c)
    x0 = numpy.array([x, y, z], numpy.float64)
    _, xs = rungekutta.ark4(rfunc, 0.0, x0, 20000.0, 0.00001)
    plot.render3d(xs[0,:], xs[1,:], xs[2,:], 'r.', 
                xlabel='x',
                ylabel='y',
                zlabel='z',
                markersize=0.2,
                title='Rossler Attractor',
                file_prefix=file_prefix
            )
    return 0

if __name__ == "__main__":
    sys.exit(main())