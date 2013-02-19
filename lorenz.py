###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: lorenz.py
# Author: Ken Sheedlo
#
# Lorenz equations, solutions to PSet 5.
#
###############################################################################

from __future__ import division

import getopt
import matplotlib.pyplot
import mpl_toolkits.mplot3d
import numpy
import plot
import rungekutta
import sys

from utils import split_dict

def lorenz(a, r, b):
    '''
    Parameterizes a Lorenz system.

    Params: a, r, b for the new Lorenz system.

    Returns: a callable F(t, x) where
        t   is not used in the Lorenz system, but included for compatibility
            with ODE integrators.
        x   the current state vector of the system.
    '''
    return lambda _, x: numpy.array([
                                    a * (x[1]-x[0]),
                                    r*x[0] - x[1] - x[0]*x[2],
                                    x[0]*x[1] - b*x[2]
                                ], dtype=numpy.float64)

def plot_dtol(tstep, **kwargs):
    '''
    Makes a plot with a parameterized tolerance.

    '''
    lfunc = lorenz(16.0, 45.0, 4.0)
    x0 = numpy.array([-13, -12, 52], dtype=numpy.float64)
    _, xs = rungekutta.ark4(lfunc, 0.0, x0, 20.0, tstep)
    plot_args = dict(kwargs)
    plot_args.update({
            'xlabel': 'x',
            'ylabel': 'y',
            'zlabel': 'z',
            'title': 'Lorenz Attractor (Tol = {0})'.format(tstep),
        })
    plot.render3d(xs[0,:], xs[1,:], xs[2,:], **plot_args)

def main(argv=None):
    if argv is None:
        argv=sys.argv        

    file_prefix = None
    a = 16.0
    r = 45.0
    b = 4.0

    suffixed = lambda s, suf: None if s is None else '{0}{1}'.format(s, suf)

    try:
        options, args = getopt.getopt(argv[1:], 'a:r:b:f:')
        for opt, arg in options:
            if opt == '-a':
                a = float(arg)
            elif opt == '-r':
                r = float(arg)
            elif opt == '-b':
                b = float(arg)
            elif opt == '-f':
                file_prefix = arg
    except getopt.GetoptError as err:
        print str(err)
        return 2

    x0 = numpy.array([-13, -12, 52], dtype=numpy.float64)
    lfunc = lorenz(a, r, b)
    ts, xs = rungekutta.ark4(lfunc, 0.0, x0, 20000.0, 0.00001)
    plot.render3d(
                xs[0,:], xs[1,:], xs[2,:], 'b.',
                xlabel='x', 
                ylabel='y', 
                zlabel='z', 
                markersize=0.2,
                title='Lorenz Attractor',
                file_prefix=suffixed(file_prefix, '_2a')
            )

    ts1, xs1 = rungekutta.ark4(lfunc, 0.0, x0, 2.0, 0.01)
    ts2, xs2 = rungekutta.rk4(lfunc, 0.0, x0, 0.001, 2000)
    def _lorenz_2b_callback(axes):
        axes.plot(xs1[0,:], xs1[1,:], xs1[2,:], 'b', label='ARK4')
        axes.plot(xs2[0,:], xs2[1,:], xs2[2,:], 'r', label='RK4')
        axes.legend()
    plot.render3d(
                xlabel='x', 
                ylabel='y', 
                zlabel='z', 
                title='RK4 vs. ARK4 Overlay',
                ax_callback=_lorenz_2b_callback,
                file_prefix=suffixed(file_prefix, '_2b')
            )

    return 0

if __name__ == "__main__":
    sys.exit(main())