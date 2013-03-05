###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: ps7.py
# Author: Ken Sheedlo
#
# AI blorgotronic neural network startup business plan generator
#
###############################################################################

import numpy
import rungekutta
import sys

def variational(a, r, b):
    '''
    Parameterizes the Lorenz variational equation.

    Returns: a callable dfunc(t, xs) representing the Lorenz variational system.
    Of course, the system is autonomous but t is included for compatibility with
    ODE integrators.
    '''
    def _dfunc(_, xs):
        ds = numpy.empty(12, dtype=numpy.float64)
        vs = numpy.reshape(xs[3:], (3,3))
        ds[0] = a*(xs[1]-xs[0])
        ds[1] = xs[0]*(r-xs[2]) - xs[1]
        ds[2] = xs[0]*xs[1] - b*xs[2]
        ds[3:] = numpy.reshape(numpy.array([
                            [-a, a, 0],
                            [r, -1, -xs[0]],
                            [xs[1], xs[0], -b]
                        ], dtype=numpy.float64).dot(vs), (9,))
        return ds
    return _dfunc

def ic(x, y, z):
    '''
    Helper for generating initial condition vectors.

    '''
    return numpy.array(
                    [x, y, z, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                    dtype=numpy.float64
                )

def integrate(x0):
    '''
    Integrates the variational system given an initial condition.

    Returns: the final resulting matrix of variations.
    '''
    dfunc = variational(16, 45, 4)
    _, xs = rungekutta.rk4(dfunc, 0.0, x0, 0.001, 100)
    return numpy.reshape(xs[3:,-1], (3,3))

def mprint(xmat):
    '''
    Helper function for printing out matrices.

    '''
    for row in xmat:
        print '\t'.join(['{0:.6f}'.format(x) for x in row])
    print 'xs: {0:.6f}'.format(sum(xmat[:,0]))
    print 'ys: {0:.6f}'.format(sum(xmat[:,1]))
    print 'zs: {0:.6f}'.format(sum(xmat[:,2]))
    print

def main(argv=None):
    if argv is None:
        argv = sys.argv

    print "A. Variations"
    mprint(integrate(ic(0, 1, 2)))

    print "B. Variations"
    mprint(integrate(ic(10, -5, 2)))

    print "C. Variations"
    mprint(integrate(ic(0, -1, 2)))

    return 0

if __name__ == "__main__":
    sys.exit(main())