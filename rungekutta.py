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

import chaostest
import numpy
import unittest

from numpy.linalg import norm

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
        xs[:,i] = _rk4_step(dfunc, xs[:,i-1], ts[i-1], dt, *f_args)

    return ts, xs

def _rk4_step(dfunc, xn, tn, dt, *args):
    '''
    Runs one step of Runge-Kutta 4th order and returns the result.

    '''
    k1 = dfunc(tn, xn, *args)
    k2 = dfunc(tn + (dt/2), xn + (k1*dt/2), *args)
    k3 = dfunc(tn + (dt/2), xn + (k2*dt/2), *args)
    k4 = dfunc(tn + dt, xn + k3*dt, *args)
    return xn + dt*((k1 + 2*k2 + 2*k3 + k4) / 6)

ARK4_SAFETY_SCALE_FACTOR = numpy.float64(0.98)

def ark4(dfunc, t0, x0, t_final, tol, **kwargs):
    '''
    Adaptive 4th-order Runge-Kutta ODE integrator.

    '''
    dt = numpy.float64(0.01)
    f_args = kwargs.get('f_args', tuple())

    # Take a guess at the number of data points we'll need, and reshape data
    # arrays as necessary.
    npoints = int(150*(t_final-t0))
    xs = numpy.empty((npoints, len(x0)), dtype=numpy.float64)
    ts = numpy.empty(npoints, dtype=numpy.float64)
    xs[0,:] = x0
    ts[0] = t0

    def _step_until_nonzero_error(xn, tn, hn, count):
        if count == 10:
            return (hn, tol)
        x1 = _rk4_step(dfunc, xn, tn, hn, *f_args)
        x2 = _rk4_step(
                    dfunc, 
                    _rk4_step(dfunc, xn, tn, hn/2, *f_args), 
                    tn + (hn/2), 
                    hn/2, 
                    *f_args
                )
        delta = norm(x1-x2, ord=numpy.inf) 
        return (hn, delta) if delta != 0.0 else _step_until_nonzero_error(
                                                                    xn, 
                                                                    tn, 
                                                                    2*hn,
                                                                    count+1
                                                                )

    p_i = 0
    while ts[p_i] < t_final:
        (dt, delta) = _step_until_nonzero_error(xs[p_i,:], ts[p_i], dt, 0)
        dt = ARK4_SAFETY_SCALE_FACTOR * dt * (
                    abs(tol/delta) ** (0.2 if tol >=delta else 0.25)
                ) 

        dt = min(dt, t_final - ts[p_i])
        p_i = p_i + 1

        # Check p_i against the size of data arrays. Resize if necessary
        if p_i >= npoints:
            npoints *= 2
            xs = numpy.resize(xs, (npoints, len(x0)))
            ts = numpy.resize(ts, (npoints,))

        xs[p_i,:] = _rk4_step(dfunc, xs[p_i-1,:], ts[p_i-1], dt, *f_args)
        ts[p_i] = ts[p_i-1] + dt

    return ts[:p_i+1], numpy.transpose(xs[:p_i+1])

class TestRungeKutta(chaostest.TestCase):
    '''
    Test suite for Runge-Kutta ODE solvers.

    '''
    def setUp(self):
        '''
        Sets up tests. Divide by zero should always raise an exception.

        '''
        numpy.seterr(divide='raise')

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

    def test_ark4_x_squared(self):
        df = lambda t, x: 2*t
        ts, xs = ark4(df, 0.0, numpy.array([1], dtype=numpy.float64), 4.0, 0.01)
        self.assertAlmostEqual(ts[-1], 4.0, delta=0.01)
        self.assertDataFits(ts, xs, lambda t: 1.0 + (t ** 2), delta=0.01)

    def test_ark4_exp(self):
        df = lambda t, x: x
        ts, xs = ark4(df, 0, numpy.array([1], dtype=numpy.float64), 16.0, 0.01)
        self.assertDataFits(ts, xs, lambda t: numpy.exp(t), delta=0.01)

    def test_pendulum(self):
        '''
        Tests for agreement between RK4 and ARK4.

        '''
        pfunc = lambda t, x: numpy.array([
                                        x[1],
                                        numpy.cos(7.4246*t) - 0.025*x[1] - 
                                        0.98*numpy.sin(x[0]),
                                    ], dtype=numpy.float64)
        t0 = 0.0
        x0 = numpy.array([3.0, 0.1], dtype=numpy.float64)
        ts1, xs1 = rk4(pfunc, t0, x0, 0.01, 1000)
        ts2, xs2 = ark4(pfunc, t0, x0, 10.0, 0.001)
        self.assertAlmostEqual(xs1[0,-1], xs2[0,-1], delta=0.01)

if __name__ == "__main__":
    unittest.main()