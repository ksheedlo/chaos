###############################################################################
#
# CSCI 4446 - Chaotic Dynamics
#
# File: rungekutta.py
# Author: Ken Sheedlo
#
# Runge-Kutta ODE solver.
#
###############################################################################

from __future__ import division

import numpy
import unittest

def rk4(dfunc, t0, x0, dt, nsteps, **kwargs):
    '''
    Runge-Kutta ODE integrator.

    Params:
        dfunc   The derivative function to integrate, passed as a callable
                dfunc(t, x, *f_args). t is a scalar, x is a vector of the same
                shape as x0.
        t0      Initial t-value for the integrator.
        x0      Initial x-value.
        dt      Time step.
        nsteps  Number of steps to run the integrator.

    Returns: a tuple (ts, xs) where
        ts      A vector (1 x nsteps) of time values.
        xs      The results (len(x0) x nsteps). 
    '''
    ts = t0 + (numpy.array(range(nsteps+1), dtype=numpy.float64) * dt)
    xs = numpy.empty((len(x0), nsteps+1), dtype=numpy.float64)
    xs[:,0] = x0
    f_args = kwargs.get('f_args', tuple())

    for i in xrange(1, nsteps+1):
        k1 = dfunc(ts[i-1], xs[:,i-1], *f_args)
        k2 = dfunc(ts[i-1] + (dt/2), xs[:,i-1] + (k1*dt/2), *f_args)
        k3 = dfunc(ts[i-1] + (dt/2), xs[:,i-1] + (k2*dt/2), *f_args)
        k4 = dfunc(ts[i-1] + dt, xs[:,i-1] + dt*k3, *f_args)
        xs[:,i] = xs[:,i-1] + dt * ((k1 + 2*k2 + 2*k3 + k4) / 6)

    return ts, xs

class TestRungeKutta(unittest.TestCase):
    '''
    Test suite for Runge-Kutta ODE solvers.

    '''
    def test_1d_ode(self):
        '''
        Test runs on a simple ODE case.

        '''
        df = lambda t, x: 2*t
        _, xs = rk4(df, 0, numpy.array([1], dtype=numpy.float64), 0.01, 400)
        final = xs[0,-1]
        self.assertEqual(xs.shape, (1, 401))
        self.assertAlmostEqual(final, 17.0, delta=0.01)

    def test_exp_ode(self):
        '''
        Test runs the exponential function.

        '''
        df = lambda t, x: x
        _, xs = rk4(df, 0, numpy.array([1], dtype=numpy.float64), 0.01, 400)
        final = xs[0,-1]
        self.assertAlmostEqual(final, numpy.exp(4), delta=0.01)

if __name__ == "__main__":
    unittest.main()