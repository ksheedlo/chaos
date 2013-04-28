###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
# File: rkperf.py
# Author: Ken Sheedlo
#
# Runge-Kutta profiling and performance analysis.
#
###############################################################################

from __future__ import division

import cProfile
import getopt
import lorenz
import numpy
import rungekutta
import sys

def runit():
    lfunc = lorenz.lorenz(16, 45, 4)
    ts, xxs = rungekutta.rk4(
                            lfunc, 
                            0.0, 
                            numpy.array([-13.0, -12.0, 52.0], dtype=numpy.float64),
                            0.0001,
                            100000
                        )

def main(argv=None):
    if argv is None:
        argv = sys.argv

    filename = None
    sort = None

    try:
        options, args = getopt.getopt(argv[1:], 'o:s:')
        for opt, arg in options:
            if opt == '-o':
                filename = arg 
            if opt == '-s':
                sort = arg
    except getopt.GetoptError as err:
        print str(err)
        return 2

    if sort is None:
        cProfile.run(runit.func_code, filename)
    else:
        cProfile.run(runit.func_code, filename, sort)

    return 0

if __name__ == "__main__":
    sys.exit(main())
